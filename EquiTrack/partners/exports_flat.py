from rest_framework_csv import renderers as r


class BaseCSVFlatRenderer(r.CSVRenderer):
    format = 'csv_flat'


class InterventionCSVFlatRenderer(BaseCSVFlatRenderer):
    header = [
            "id",
            "status",
            "agreement_number",
            "country_programme",
            "document_type",
            "number",
            "title",
            "start",
            "end",
            "offices",
            "unicef_focal_points",
            "partner_focal_points",
            "population_focus",
            "fr_numbers",
            "partner_contribution",
            "partner_contribution_local",
            "unicef_cash",
            "unicef_cash_local",
            "in_kind_amount",
            "in_kind_amount_local",
            "currency",
            "total",
            "planned_visits",
            "submission_date",
            "submission_date_prc",
            "review_date_prc",
            "prc_review_document",
            "partner_authorized_officer_signatory",
            "signed_by_partner_date",
            "unicef_signatory",
            "signed_by_unicef_date",
            "signed_pd_document",
            "attachments",
            "created",
            "modified",
    ]

    labels = {
            "id": "Id",
            "status": "Status",
            "agreement_number": "Agreement",
            "country_programme": "Country Programme",
            "document_type": "Document Type",
            "number": "Reference Number",
            "title": "Document Title",
            "start": "Start Date",
            "end": "End Date",
            "offices": "UNICEF Office",
            "unicef_focal_points": "UNICEF Focal Points",
            "partner_focal_points": "CSO Authorized Officials",
            "population_focus": "Population Focus",
            "fr_numbers": "FR Number(s)",
            "partner_contribution": "CSO Contribution",
            "partner_contribution_local": "CSO Contribution (Local)",
            "unicef_cash": "UNICEF Cash",
            "unicef_cash_local": "UNICEF Cash (Local)",
            "in_kind_amount": "In Kind Amount",
            "in_kind_amount_local": "In Kind Amount (Local)",
            "currency": "Currency",
            "total": "Total",
            "planned_visits": "Planned Visits",
            "submission_date": "Document Submission Date by CSO",
            "submission_date_prc": "Submission Date to PRC",
            "review_date_prc": "Review Date by PRC",
            "prc_review_document": "Review Document by PRC",
            "partner_authorized_officer_signatory": "Signed by Partner",
            "signed_by_partner_date": "Signed by Partner Date",
            "unicef_signatory": "Signed by UNICEF",
            "signed_by_unicef_date": "Signed by UNICEF Date",
            "signed_pd_document": "Signed PD Document",
            "attachments": "Attachments",
            "created": "Created",
            "modified": "Modified",
    }


class InterventionAmendmentCSVFlatRenderer(BaseCSVFlatRenderer):
    header = [
        "id",
        "intervention",
        "amendment_number",
        "types",
        "other_description",
        "signed_amendment",
        "signed_date",
        "created",
        "modified",
    ]

    labels = {
        "id": "Id",
        "intervention": "Reference Number",
        "amendment_number": "Number",
        "types": "Types",
        "other_description": "Description",
        "signed_amendment": "Amendment File",
        "signed_date": "Signed Date",
        "created": "Created",
        "modified": "Modified",
    }


class InterventionResultCSVFlatRenderer(BaseCSVFlatRenderer):
    header = [
        "id",
        "intervention",
        "country_programme",
        "result_type",
        "sector",
        "name",
        "code",
        "from_date",
        "to_date",
        "parent",
        "humanitarian_tag",
        "wbs",
        "vision_id",
        "gic_code",
        "gic_name",
        "sic_code",
        "sic_name",
        "activity_focus_code",
        "activity_focus_name",
        "hidden",
        "ram",
    ]

    labels = {
        "id": "Id",
        "intervention": "Reference Number",
        "country_programme": "Country Programme",
        "result_type": "Result Type",
        "sector": "Section",
        "name": "Name",
        "code": "Code",
        "from_date": "From Date",
        "to_date": "To Date",
        "parent": "Parent",
        "humanitarian_tag": "Humanitarian Tag",
        "wbs": "WBS",
        "vision_id": "VISION Id",
        "gic_code": "GIC Code",
        "gic_name": "GIC Name",
        "sic_code": "SIC Code",
        "sic_name": "SIC Name",
        "activity_focus_code": "Activity Focus Code",
        "activity_focus_name": "Activity Focus Name",
        "hidden": "Hidden",
        "ram": "RAM",
    }


class InterventionIndicatorCSVFlatRenderer(BaseCSVFlatRenderer):
    header = [
        "id",
        "intervention",
        "sector",
        "result",
        "name",
        "code",
        "unit",
        "total",
        "sector_total",
        "current",
        "sector_current",
        "assumptions",
        "target",
        "baseline",
        "ram_indicator",
        "active",
        "view_on_dashboard",
    ]

    labels = {
        "id": "Id",
        "intervention": "Reference Number",
        "sector": "Sector",
        "result": "Result",
        "name": "Name",
        "code": "Code",
        "unit": "Unit",
        "total": "UNICEF Target",
        "sector_total": "Sector Target",
        "current": "Current",
        "sector_current": "Sector Current",
        "assumptions": "Assumptions",
        "target": "Target",
        "baseline": "Baseline",
        "ram_indicator": "RAM Indicator",
        "active": "Active",
        "view_on_dashboard": "View on Dashboard",
    }


class InterventionSectorLocationLinkCSVFlatRenderer(BaseCSVFlatRenderer):
    header = [
        "id",
        "intervention",
        "sector",
        "name",
        "location_type",
        "p_code",
        "geom",
        "point",
        "latitude",
        "longitude",
    ]

    labels = {
        "id": "Id",
        "intervention": "Reference Number",
        "sector": "Sector",
        "name": "Name",
        "location_type": "Location Type",
        "p_code": "P Code",
        "geom": "Geo Point",
        "point": "Point",
        "latitude": "Latitude",
        "longitude": "Longitude",
    }
