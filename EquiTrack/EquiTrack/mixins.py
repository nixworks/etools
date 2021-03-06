"""
Project wide mixins for models and classes
"""
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import connection
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse
from django.utils.http import urlsafe_base64_encode

import jwt
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import perform_login
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_payload_handler
from tenant_schemas.middleware import TenantMiddleware
from tenant_schemas.utils import get_public_schema_name

from EquiTrack.utils import set_country

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
logger = logging.getLogger(__name__)


class AdminURLMixin(object):
    """
    Provides a method to get the admin link for the mixed in model
    """
    admin_url_name = 'admin:{app_label}_{model_name}_{action}'

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(self.admin_url_name.format(
            app_label=content_type.app_label,
            model_name=content_type.model,
            action='change'
        ), args=(self.id,))


class CountryUsersAdminMixin(object):

    staff_only = True

    def filter_users(self, kwargs):

        filters = {}
        if connection.tenant:
            filters['profile__country'] = connection.tenant
        if self.staff_only:
            filters['is_staff'] = True

        if filters:
            # preserve existing filters if any
            queryset = kwargs.get("queryset", get_user_model().objects)
            kwargs["queryset"] = queryset.filter(**filters)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.rel.to is get_user_model():
            self.filter_users(kwargs)

        return super(CountryUsersAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if db_field.rel.to is get_user_model():
            self.filter_users(kwargs)

        return super(CountryUsersAdminMixin, self).formfield_for_manytomany(db_field, request, **kwargs)


class EToolsTenantMiddleware(TenantMiddleware):
    """
    Routes user to their correct schema based on country
    """
    def process_request(self, request):
        # Connection needs first to be at the public schema, as this is where
        # the tenant metadata is stored.
        connection.set_schema_to_public()

        if not request.user:
            return

        if any(x in request.path for x in [
                u'workspace_inactive']):
            return None

        if request.user.is_anonymous():
            # check if user is trying to reach an authentication endpoint
            if any(x in request.path for x in [
                u'api',
                u'login',
                u'saml',
                u'accounts',
                u'monitoring',
            ]):
                return None  # let them pass
            else:
                return HttpResponseRedirect(settings.LOGIN_URL)

        if request.user.is_superuser and not request.user.profile.country:
            return None

        if not request.user.is_superuser and \
                (not request.user.profile.country or
                 request.user.profile.country.business_area_code in settings.INACTIVE_BUSINESS_AREAS):
            return HttpResponseRedirect("/workspace_inactive/")
        try:
            set_country(request.user, request)

        except Exception:
            logger.info('No country found for user {}'.format(request.user))
            return SimpleTemplateResponse('no_country_found.html', {'user': request.user})

        # Content type can no longer be cached as public and tenant schemas
        # have different models. If someone wants to change this, the cache
        # needs to be separated between public and shared schemas. If this
        # cache isn't cleared, this can cause permission problems. For example,
        # on public, a particular model has id 14, but on the tenants it has
        # the id 15. if 14 is cached instead of 15, the permissions for the
        # wrong model will be fetched.
        ContentType.objects.clear_cache()

        # Do we have a public-specific urlconf?
        if hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and request.tenant.schema_name == get_public_schema_name():
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF


class DRFBasicAuthMixin(BasicAuthentication):
    def authenticate(self, request):
        super_return = super(DRFBasicAuthMixin, self).authenticate(request)
        if not super_return:
            return None

        user, token = super_return
        set_country(user, request)
        return user, token


class EtoolsTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        super_return = super(EtoolsTokenAuthentication, self).authenticate(request)
        if not super_return:
            return None

        user, token = super_return
        set_country(user, request)
        return user, token


class EToolsTenantJWTAuthentication(JSONWebTokenAuthentication):
    """
    Handles setting the tenant after a JWT successful authentication
    """
    def authenticate(self, request):

        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            # no JWT token return to skip this authentication mechanism
            return None

        try:
            user, jwt_value = super(EToolsTenantJWTAuthentication, self).authenticate(request)
        except TypeError:
            raise PermissionDenied(detail='No valid authentication provided')
        except AuthenticationFailed:
            # Try again
            if getattr(settings, 'JWT_ALLOW_NON_EXISTENT_USERS', False):
                try:
                    # try and see if the token is valid
                    payload = jwt_decode_handler(jwt_value)
                except (jwt.ExpiredSignature, jwt.DecodeError):
                    raise PermissionDenied(detail='Authentication Failed')
                else:
                    # signature is valid user does not exist... setting default authenticated user
                    user = get_user_model().objects.get(username=settings.DEFAULT_UNICEF_USER)
                    setattr(user, 'jwt_payload', payload)
            else:
                raise PermissionDenied(detail='Authentication Failed')

        if not user.profile.country:
            raise PermissionDenied(detail='No country found for user')

        if user.profile.country_override and user.profile.country != user.profile.country_override:
            user.profile.country = user.profile.country_override
            user.profile.save()

        set_country(user, request)
        return user, jwt_value


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        User = get_user_model()

        # TODO: make sure that the partnership is still in good standing or valid or whatever
        if sociallogin.user.pk:
            set_country(sociallogin.user, request)
            logger.info("setting connection to {}".format(sociallogin.user.profile.country))
            return
        try:
            # if user exists, connect the account to the existing account and login
            new_login_user = User.objects.get(email=sociallogin.user.email)
        except User.DoesNotExist:
            url = reverse('sociallogin_notamember', kwargs={'email': urlsafe_base64_encode(sociallogin.user.email)})
            raise ImmediateHttpResponse(HttpResponseRedirect(url))

        sociallogin.connect(request, new_login_user)
        set_country(new_login_user, request)
        perform_login(
            request,
            new_login_user,
            'none',
            redirect_url=sociallogin.get_redirect_url(request),
            signal_kwargs={"sociallogin": sociallogin}
        )


class CustomAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        # quick way of disabling signups.
        return False

    def login(self, request, user):
        # if we need to add any other login validation, here would be the place.
        return super(CustomAccountAdapter, self).login(request, user)


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class ExportModelMixin(object):
    def set_labels(self, serializer_fields, model):
        labels = {}
        model_labels = {}
        for f in model._meta.fields:
            model_labels[f.name] = f.verbose_name
        for f in serializer_fields:
            if model_labels.get(f, False):
                labels[f] = model_labels.get(f)
            elif serializer_fields.get(f) and serializer_fields[f].label:
                labels[f] = serializer_fields[f].label
            else:
                labels[f] = f.replace("_", " ").title()
        return labels

    def get_renderer_context(self):
        context = super(ExportModelMixin, self).get_renderer_context()
        if hasattr(self, "get_serializer_class"):
            serializer_class = self.get_serializer_class()
            serializer = serializer_class()
            serializer_fields = serializer.get_fields()
            model = getattr(serializer.Meta, "model")
            context["labels"] = self.set_labels(
                serializer_fields,
                model
            )
        return context


class QueryStringFilterMixin(object):

    def filter_params(self, filters):
        queries = []
        for param_filter, query_filter in filters:
            if param_filter in self.request.query_params:
                value = self.request.query_params.get(param_filter)
                if query_filter.endswith(('__in')):
                    value = value.split(',')
                queries.append(Q(**{query_filter: value}))
        return queries

    def search_params(self, filters, param_name='search'):
        search_term = self.request.query_params.get(param_name)
        search_query = Q()
        if param_name in self.request.query_params:
            for param_filter in filters:
                q = Q(**{param_filter: search_term})
                search_query = search_query | q
        return search_query


def custom_jwt_payload_handler(user):
    payload = jwt_payload_handler(user)
    payload['groups'] = list(user.groups.values_list('name', flat=True))
    return payload
