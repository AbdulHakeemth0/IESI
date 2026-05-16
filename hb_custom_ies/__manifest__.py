# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Customized IES ",
    "version": "18.0.1.0",
    "category": "",
    "summary": "Custom IES",
    "license": "LGPL-3",
    "author": "Abdul Hakeem",
    "description": """""",
    "website": "",
    "depends": [
        "base", "crm","sale_management",
        "account", "purchase"
    ],
    "data": [
        "data/ir_sequence.xml",
        "data/data.xml",
        "security/ir.model.access.csv",
        "reports/quotation_reports.xml",
        "reports/report_action.xml",
        "wizard/sale_return_wizard_view.xml",
        "views/inherit_crm_lead.xml",
        # "views/electrical.xml",
        # "views/hvac.xml",
        # "views/mep.xml",
        # "views/plumbing.xml",
        # "views/water_supply.xml",
        # "views/drainage_views.xml",
        # "views/civil_views.xml",
        # "views/elv_views.xml",
        # "views/fire_fighting_views.xml",
        # "views/fire_alarm_views.xml",
        "views/product_template.xml",
        "views/inherit_sale_order.xml",
        "views/project_discipline.xml",
    ],
    "demo": [],
    "css": [],
    "installable": True,
    "auto_install": False,
    "application": False,
}