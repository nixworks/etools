from rest_framework_csv import renderers as r


class PartnerOrganizationCSVRenderer(r.CSVRenderer):
    header = ['vendor_number', 'organization_full_name',
              'short_name', 'alternate_name', 'partner_type', 'shared_with', 'address',
              'phone_number', 'email_address', 'risk_rating', 'date_last_assessment_against_core_values',
              'actual_cash_transfer_for_cp', 'actual_cash_transfer_for_current_year', 'marked_for_deletion', 'blocked',
              'type_of_assessment', 'date_assessed', 'assessments', 'staff_members', 'url', ]

    labels = {
        'vendor_number': 'Vendor Number',
        'organization_full_name': 'Organizations Full Name',
        'short_name': 'Short Name',
        'alternate_name': 'Alternate Name',
        'partner_type': 'Partner Type',
        'shared_with': 'Shared Partner',
        'address': 'Address',
        'phone_number': 'Phone Number',
        'email_address': 'Email Address',
        'risk_rating': 'Risk Rating',
        'date_last_assessment_against_core_values': 'Date Last Assessed Against Core Values',
        'actual_cash_transfer_for_cp': 'Actual Cash Transfer for CP (USD)',
        'actual_cash_transfer_for_current_year': 'Actual Cash Transfer for Current Year (USD)',
        'marked_for_deletion': 'Marked for Deletion',
        'blocked': 'Blocked',
        'type_of_assessment': 'Assessment Type',
        'date_assessed': 'Date Assessed',
        'assessments': 'Assessment Type (Date Assessed)',
        'staff_members': 'Staff Members',
        'url': 'URL',
    }


class PartnerOrganizationHactCsvRenderer(r.CSVRenderer):

    header = [
        'name',
        'vendor_number',
        'partner_type',
        'shared_with',
        'type_of_assessment',
        # 'total_ct_cp',
        'total_ct_cy',
        'net_ct_cy',
        'reported_cy',
        'total_ct_ytd',
        'rating',
        'expiring_assessment_flag',
        'approaching_threshold_flag',
        'hact_values.programmatic_visits.planned.q1',
        'hact_values.programmatic_visits.planned.q2',
        'hact_values.programmatic_visits.planned.q3',
        'hact_values.programmatic_visits.planned.q4',
        'hact_min_requirements.programme_visits',
        'hact_values.programmatic_visits.completed.q1',
        'hact_values.programmatic_visits.completed.q2',
        'hact_values.programmatic_visits.completed.q3',
        'hact_values.programmatic_visits.completed.q4',
        'hact_values.spot_checks.planned.q1',
        'hact_values.spot_checks.planned.q2',
        'hact_values.spot_checks.planned.q3',
        'hact_values.spot_checks.planned.q4',
        'hact_min_requirements.spot_checks',
        'hact_values.spot_checks.follow_up_required',
        'hact_values.spot_checks.completed.q1',
        'hact_values.spot_checks.completed.q2',
        'hact_values.spot_checks.completed.q3',
        'hact_values.spot_checks.completed.q4',
        'hact_values.audits.minimum_requirements',
        'hact_values.audits.completed',
        'hact_values.outstanding_findings',
    ]

    labels = {
        'name': 'Implementing Partner',
        'vendor_number': 'Vendor Number',
        'partner_type': 'Partner Type',
        'shared_with': 'Shared IP',
        'type_of_assessment': 'Assessment Type',
        # 'total_ct_cp': 'TOTAL for current CP cycle',
        'total_ct_cy': 'Cash Transfer 1 OCT - 30 SEP',
        'net_ct_cy': 'Net Cash Transferred per Current Year',
        'reported_cy': 'Liquidations 1 OCT - 30 SEP',
        'total_ct_ytd': 'Cash Transfers Jan - Dec',
        'rating': 'Risk Rating',
        'expiring_assessment_flag': 'Expiring Threshold',
        'approaching_threshold_flag': 'Approach Threshold',
        # TODO change with q1 after prp-refactoring
        'hact_values.programmatic_visits.planned.total': 'Programmatic Visits Planned Q1',
        'hact_values.programmatic_visits.planned.q2': 'Q2',
        'hact_values.programmatic_visits.planned.q3': 'Q3',
        'hact_values.programmatic_visits.planned.q4': 'Q4',
        'hact_min_requirements.programme_visits': 'Programmatic Visits M.R',
        'hact_values.programmatic_visits.completed.q1': 'Programmatic Visits Completed Q1',
        'hact_values.programmatic_visits.completed.q2': 'Q2',
        'hact_values.programmatic_visits.completed.q3': 'Q3',
        'hact_values.programmatic_visits.completed.q4': 'Q4',
        'hact_values.spot_checks.planned.q1': 'Spot Checks Planned Q1',
        'hact_values.spot_checks.planned.q2': 'Q2',
        'hact_values.spot_checks.planned.q3': 'Q3',
        'hact_values.spot_checks.planned.q4': 'Q4',
        'hact_min_requirements.spot_checks': 'Spot Checks M.R',
        'hact_values.spot_checks.follow_up_required': 'Follow up Required',
        'hact_values.spot_checks.completed.q1': 'Spot Checks Completed Q1',
        'hact_values.spot_checks.completed.q2': 'Q2',
        'hact_values.spot_checks.completed.q3': 'Q3',
        'hact_values.spot_checks.completed.q4': 'Q4',
        'hact_values.audits.minimum_requirements': 'Audits M.R',
        'hact_values.audits.completed': 'Audit Completed',
        'hact_values.outstanding_findings': 'Audits Outstanding Findings',
    }


class AgreementCSVRenderer(r.CSVRenderer):
    header = [
        "agreement_number",
        "status",
        "partner_name",
        "agreement_type",
        "start",
        "end",
        "partner_manager_name",
        "signed_by_partner_date",
        "signed_by_name",
        "signed_by_unicef_date",
        "staff_members",
        "amendments",
        "url",
    ]

    labels = {
        "agreement_number": 'Reference Number',
        "status": 'Status',
        "partner_name": 'Partner Name',
        "agreement_type": 'Agreement Type',
        "start": 'Start Date',
        "end": 'End Date',
        "partner_manager_name": 'Signed By Partner',
        "signed_by_partner_date": 'Signed By Partner Date',
        "signed_by_name": 'Signed By UNICEF',
        "signed_by_unicef_date": 'Signed By UNICEF Date',
        "staff_members": 'Partner Authorized Officer',
        "amendments": 'Amendments',
        "url": "URL",
    }


class InterventionCSVRenderer(r.CSVRenderer):
    header = [
        "partner_name", "vendor_number", "status", "partner_type", "agreement_number", "country_programme",
        "document_type", "number", "title", "start", "end", "offices", "sectors", "locations", "contingency_pd",
        "intervention_clusters", "unicef_focal_points", "partner_focal_points", "budget_currency", "cso_contribution",
        "unicef_budget", "unicef_supply", "total_planned_budget", "fr_numbers", "fr_currency", "fr_posting_date",
        "fr_amount", "fr_actual_amount", "fr_outstanding_amt", "planned_visits", "submission_date",
        "submission_date_prc", "review_date_prc", "partner_authorized_officer_signatory", "signed_by_partner_date",
        "unicef_signatory", "signed_by_unicef_date", "days_from_submission_to_signed", "days_from_review_to_signed",
        "amendment_sum", "last_amendment_date", "attachment_type", "total_attachments", "cp_outputs", "url",
    ]

    labels = {
        "partner_name": "Partner",
        "vendor_number": "Vendor no.",
        "status": "Status",
        "partner_type": "Partner Type",
        "agreement_number": "Agreement",
        "country_programme": "Country Programme",
        "document_type": "Document Type",
        "number": "Reference Number",
        "title": "Document Title",
        "start": "Start Date",
        "end": "End Date",
        "offices": "UNICEF Office",
        "sectors": "Sections",
        "locations": "Locations",
        "contingency_pd": "Contingency PD?",
        "intervention_clusters": "Cluster",
        "unicef_focal_points": "UNICEF Focal Points",
        "partner_focal_points": "CSO Authorized Officials",
        "budget_currency": "Budget Currency",
        "cso_contribution": "Total CSO Budget (USD)",
        "unicef_budget": "UNICEF Cash (USD)",
        "unicef_supply": "UNICEF Supply (USD)",
        "total_planned_budget": "Total PD/SSFA Budget (USD)",
        "fr_numbers": "FR Number(s)",
        "fr_currency": "FR Currency",
        "fr_posting_date": "FR Posting Date",
        "fr_amount": "FR Amount",
        "fr_actual_amount": "FR Actual CT",
        "fr_outstanding_amt": "Outstanding DCT",
        "planned_visits": "Planned Programmatic Visits",
        "spot_checks": "Planned Spot Checks",
        "audit": "Planned Audits",
        "submission_date": "Document Submission Date by CSO",
        "submission_date_prc": "Submission Date to PRC",
        "review_date_prc": "Review Date by PRC",
        "partner_authorized_officer_signatory": "Signed by Partner",
        "signed_by_partner_date": "Signed by Partner Date",
        "unicef_signatory": "Signed by UNICEF",
        "signed_by_unicef_date": "Signed by UNICEF Date",
        "days_from_submission_to_signed": "Days from Submission to Signed",
        "days_from_review_to_signed": "Days from Review to Signed",
        "amendment_sum": "Total no. of amendments",
        "last_amendment_date": "Last amendment date",
        "attachment_type": "Attachment Type",
        "total_attachments": "# of attachments",
        "cp_outputs": "CP Outputs",
        "url": "URL",
    }


class PartnershipDashCSVRenderer(r.CSVRenderer):
    header = [
        'partner_name', 'partner_vendor_number',
        'number',
        'sections',
        'offices_names',
        'status',
        'start',
        'end',
        'budget_currency',
        'cso_contribution',
        'unicef_supplies',
        'unicef_cash',
        'fr_currency',
        'frs_total_frs_amt',
        'disbursement',
        'outstanding_dct',
        'frs_total_frs_amt_usd',
        'disbursement_usd',
        'outstanding_dct_usd',
        'disbursement_percent',
        'days_last_pv'
    ]

    labels = {
        "partner_name": "IP Name",
        "partner_vendor_number": "Vendor Number",
        "number": "PD/SSFA Ref #",
        "sections": "Section",
        "offices_names": "Field Office",
        "status": "Status",
        "start": "Start Date",
        "end": "End Date",
        "budget_currency": "PD Currency",
        "cso_contribution": "CSO Contribution (PD Currency)",
        "unicef_supplies": "Total UNICEF Supplies (PD Currency)",
        "unicef_cash": "Total UNICEF Cash (PD Currency)",
        "fr_currency": "FR Currency",
        "frs_total_frs_amt": "FR Grand Total",
        "disbursement": "Actual Disbursements",
        "outstanding_dct": "Outstanding DCT",
        "frs_total_frs_amt_usd": "FR Grand Total (USD)",
        "disbursement_usd": "Actual Disbursement (USD)",
        "outstanding_dct_usd": "Outstanding DCT (USD)",
        "disbursement_percent": "Disbursement To Date (%)",
        "days_last_pv": "Days Since Last PV",
    }
