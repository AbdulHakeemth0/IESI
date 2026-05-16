from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_print_sale_quotation(self):
        self.ensure_one()
        return self.env.ref('ies_pdf_reports.action_report_iesi_quotation').report_action(self)

    def _get_default_boq_remarks(self):
        return """
            <div style="line-height: 1.1; font-family: Helvetica, sans-serif;">
                <div style="margin-bottom: 4px;"><strong>Assumptions &amp; Considerations</strong></div>

                <div style="margin: 0; padding: 0;">1) We have considered GI Tray and Trunking for the Electrical &amp; Data works</div>
                <div style="margin: 0; padding: 0;">2) Ducted Type Dx AC units will be supplied by the Client.</div>
                <div style="margin: 0; padding: 0;">3) Ducts considered for AC works are PI</div>
                <div style="margin: 0; padding: 0;">4) Main Electrical source and its cabling to be arranged by the Client</div>
                <div style="margin: 0; padding: 0;">5) DB Components shall be from Schneider/ABB</div>
                <div style="margin: 0; padding: 0;">6) FOH switches and sockets shall be of SS/Chrome finish</div>
                <div style="margin: 0; padding: 0;">7) All BOH switches, sockets, isolators shall be from Schneider/Legrand</div>
                <div style="margin: 0; padding: 0;">8) MEP provisions are considered only for normal café. Provision and pricing to be revised based on the final Kitchen Equipment Layout and Schedules</div>

                <div style="margin-top: 8px; margin-bottom: 4px;"><strong>Exclusions:</strong></div>
                <div style="margin: 0; padding: 0;">1) Treated Fresh air handling unit</div>
                <div style="margin: 0; padding: 0;">2) Kitchen Hood Design, Kitchen Hood, Kitchen Hood Ventilation Fan and Ducting</div>
                <div style="margin: 0; padding: 0;">3) Supply of AC Units</div>
                <div style="margin: 0; padding: 0;">4) Any Civil Works and Core cutting.</div>
                <div style="margin: 0; padding: 0;">5) Annual Maintenance Contract</div>
                <div style="margin: 0; padding: 0;">6) Third Party Inspections, Reports, Commissioning</div>
                <div style="margin: 0; padding: 0;">7) Authority Approvals and Fees for Authority Inspections</div>
                <div style="margin: 0; padding: 0;">8) Any Other Services or Scope Mentioned in the Scope Description</div>
                <div style="margin: 0; padding: 0;">9) Temporary Electrical power and water for the works.</div>
                <div style="margin: 0; padding: 0;">10) Restroom, Drinking Water, Washrooms for the Workers</div>
                <div style="margin: 0; padding: 0;">11) Lighting Control Wiring &amp; Light Control System</div>
                <div style="margin: 0; padding: 0;">12) Main Electrical Cable from Nama feeder and its Installation. If required, cabling and laying shall be done at <strong>a rate of OMR 50/- per metre.</strong></div>
                <div style="margin: 0; padding: 0;">13) Any Data, Wifi, CCTV, Fire Alarm, Fire Fighting Related Works</div>

                <div style="margin-top: 8px; margin-bottom: 4px;"><strong>Payment Terms:</strong></div>
                <div style="margin: 0; padding: 0;">50% Advance</div>
                <div style="margin: 0; padding: 0;">30% On Completion of Above Ceiling &amp; Below Floor Works</div>
                <div style="margin: 0; padding: 0;">10% On Completion of Final Fixtures</div>
                <div style="margin: 0; padding: 0;">10% On Completion of Testing &amp; Commissioning</div>

                <div style="margin-top: 8px; margin-bottom: 4px;"><strong>Duration Considered:</strong></div>
                <div style="margin: 0; padding: 0;">To be discussed and agreed as per site condition.</div>
                <div style="margin: 0; padding: 0;">Quote Validity: 15 Days</div>
            </div>
        """

    boq_remarks = fields.Html(string='Terms and Condition', default=_get_default_boq_remarks)