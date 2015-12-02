"""
Project wide mixins for models and classes
"""
__author__ = 'jcranwellward'
from django import forms

from django.conf import settings
from django.db import connection
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from rest_framework.exceptions import PermissionDenied

from tenant_schemas.middleware import TenantMiddleware
from tenant_schemas.utils import get_public_schema_name
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import  DefaultAccountAdapter
from allauth.account.utils import (perform_login, complete_signup,
                                   user_username)


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.rel.to is User:
            if connection.tenant:
                kwargs["queryset"] = User.objects.filter(profile__country=connection.tenant)

        return super(CountryUsersAdminMixin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if db_field.rel.to is User:
            if connection.tenant:
                kwargs["queryset"] = User.objects.filter(profile__country=connection.tenant)

        return super(CountryUsersAdminMixin, self).formfield_for_manytomany(db_field, request, **kwargs)


class EToolsTenantMiddleware(TenantMiddleware):
    """
    Routes user to their correct schema based on country
    """
    def process_request(self, request):
        # Connection needs first to be at the public schema, as this is where
        # the tenant metadata is stored.
        connection.set_schema_to_public()

        if any(x in request.path for x in [
            u'api',
            u'login',
            u'saml',
            u'accounts',
        ]):
            return None
        elif request.user.is_anonymous():
            return HttpResponseRedirect(settings.LOGIN_URL)
        elif request.user.is_superuser and not request.user.profile.country:
            return None

        try:
            request.tenant = request.user.profile.country
            connection.set_tenant(request.tenant)

        except Exception as exp:
            messages.info(
                request,
                'Your country instance is not yet configured, '
                'probably because eTools has not been rolled in your office yet. '
                'Please contact a member of the eTools team for more information.')
            raise self.TENANT_NOT_FOUND_EXCEPTION(
                'No country found for user {}'.format(request.user))

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


class EToolsTenantJWTAuthentication(JSONWebTokenAuthentication):
    """
    Handles setting the tenant after a JWT successful authentication
    """
    def authenticate(self, request):

        try:
            user, jwt_value = super(EToolsTenantJWTAuthentication, self).authenticate(request)
        except TypeError as exp:
            raise PermissionDenied(detail='No valid authentication provided')
        if not user.profile.country:
            raise PermissionDenied(detail='No country found for user')

        if user.profile.country_override and user.profile.country != user.profile.country_override:
            user.profile.country = user.profile.country_override
            user.profile.save()

        connection.set_tenant(user.profile.country)
        request.tenant = user.profile.country

        return user, jwt_value


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):


    def authentication_error(self,
                             request,
                             provider_id,
                             error=None,
                             exception=None,
                             extra_context=None):
        print "authentication_error"

    def new_user(self, request, sociallogin):
        """
        Instantiates a new User instance.
        """
        print "new_user"
        #sociallogin.state['process'] = 'connect'
        #return user
        return super(CustomSocialAccountAdapter, self).new_user(request, sociallogin)

    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        # print "populate user"
        # print data
        # try:
        #     user = User.objects.filter(email=data['email']).get()
        # except:
        #     raise Exception("no user found")
        #sociallogin.user = user
        #return user
        return super(CustomSocialAccountAdapter, self).populate_user(request, sociallogin, data)

    def pre_social_login(self, request, sociallogin):
        # TODO: make sure that the partnership is still in good standing or valid or whatever
        if sociallogin.user.pk:
            return
        try:
            new_login_user = User.objects.get(email=sociallogin.user.email)  # if user exists, connect the account to the existing account and login
            if not new_login_user.is_active:
                new_login_user.is_active=True
                new_login_user.save()

            sociallogin.connect(request, new_login_user)
            perform_login(request,
                          new_login_user,
                          'none',
                          redirect_url=sociallogin.get_redirect_url(request),
                          signal_kwargs={"sociallogin": sociallogin})

        except User.DoesNotExist:
           raise Exception("no user found")

        #return super(CustomSocialAccountAdapter, self).pre_social_login(request, sociallogin)

    def save_user(self, request, sociallogin, form=None):
        print "save user"
        return super(CustomSocialAccountAdapter, self).save_user(request,sociallogin,form)


class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # quick way of disabling signups.
        return False


