from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def print_custom_po(self):
        return self.env.ref('ies_pdf_reports.action_report_iesi_purchase_order').report_action(self)

    boq_terms_conditions = fields.Html(
        string="Quote Terms & Conditions",
        translate=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super(PurchaseOrder, self).default_get(fields_list)
        if 'boq_terms_conditions' in fields_list or not fields_list:
            res['boq_terms_conditions'] = """
                <div style="font-family: 'Times New Roman', Times, serif; font-size: 13px;">
                    <h4 style="font-weight:700; margin-bottom:8px; font-size: 14px;">Terms:</h4>
                    <ul>
                        <li>Samples must be approved before production.</li>
                        <li>Work starts only after written confirmation.</li>
                    </ul>
                </div>
            """
        return res