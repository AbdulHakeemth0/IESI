from email.policy import default
from string import digits

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    extract_in_invoice_digitalization_mode = fields.Selection(
        [
            ('manual', 'Manual'),
            ('auto', 'Automatic'),
        ],
        string="Invoice Digitalization Mode",
        default='manual'
    )
    extract_out_invoice_digitalization_mode = fields.Selection(
        [('manual', 'Manual'), ('auto', 'Automatic')],
        default='manual'
    )
    extract_single_line_per_tax = fields.Boolean(default=False)


SALE_ORDER_STATE = [
    ('draft', 'Draft'),
    ('prepared', 'Prepared'),
    ('review', "Internal Review"),
    ('client_review', "Client Review"),
    ('approved', 'Approved'),
    ('sale', 'Open'),
    ('closed', 'Closed'),
    ('revised', 'Revised'),
    ('loss', 'Loss'),
]


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_discipline(self, xmlid):
        rec = self.env.ref(xmlid, raise_if_not_found=False)
        return rec.id if rec else False

    return_reason = fields.Text(string="Return Reason")
    is_returned = fields.Boolean(default=False)
    state = fields.Selection(selection_add=SALE_ORDER_STATE)
    remark = fields.Text(string='Remarks')
    sale_costing_lines = fields.One2many('sale.costing.line', 'sale_order_id',
                                         string="Costing Lines", copy=True)
    plumbing_costing_lines = fields.One2many('sale.costing.line', 'sale_plumbing_line_id',
                                             string="Costing Lines", copy=True)
    water_supply_costing_lines = fields.One2many('sale.costing.line', 'sale_water_supply_line_id',
                                                 string="Costing Lines", copy=True)
    fire_alarm_costing_lines = fields.One2many('sale.costing.line', 'sale_fire_alarm_line_id',
                                               string="Costing Lines", copy=True)
    fire_fighting_costing_lines = fields.One2many('sale.costing.line', 'sale_fire_fighting_line_id',
                                                  string="Costing Lines", copy=True)
    drainage_costing_lines = fields.One2many('sale.costing.line', 'sale_drainage_line_id',
                                             string="Costing Lines", copy=True)
    civil_costing_lines = fields.One2many('sale.costing.line', 'sale_civil_line_id',
                                          string="Costing Lines", copy=True)
    elv_costing_lines = fields.One2many('sale.costing.line', 'sale_elv_line_id',
                                        string="Costing Lines", copy=True)
    mep_costing_lines = fields.One2many('sale.costing.line', 'sale_mep_line_id',
                                        string="Costing Lines", copy=True)
    hvac_costing_lines = fields.One2many('sale.costing.line', 'sale_hvac_line_id',
                                         string="Costing Lines", copy=True)
    margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    margin_amount = fields.Float(
        string="Margin Amount",
        compute="_compute_sub_total",
        store=True,digits=(16, 3)
    )
    tax_id = fields.Many2one('account.tax', string='Tax')
    total_costing_amount = fields.Float(string="Total Amount(Exc Margin", digits=(16,3),
                                        compute="_compute_total_costing_amount", store=True)
    sub_total_costing = fields.Float(string="Sub Total(Inc Margin)", compute="_compute_sub_total",
                                     store=True)
    costing_total_amount = fields.Float(string="Costing Total", compute="_compute_costing_total",
                                        store=True)
    sub_total = fields.Float(string='Sub Total')
    sale_project_bool = fields.Boolean(string="Is Project")
    project_discipline_ids = fields.Many2many('project.discipline',
                                              'sale_project_discipline_ids_rel')
    plumbing_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                             default=lambda self: self._get_discipline(
                                                 'hb_custom_ies.project_discipline_plumbing'))
    electrical_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                               default=lambda self: self._get_discipline(
                                                   'hb_custom_ies.project_discipline_electrical'))
    water_supply_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                                 default=lambda self: self._get_discipline(
                                                     'hb_custom_ies.project_discipline_water_supply'))
    fire_alarm_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                               default=lambda self: self._get_discipline(
                                                   'hb_custom_ies.project_discipline_fire_alarm'))
    fire_fighting_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                                  default=lambda self: self._get_discipline(
                                                      'hb_custom_ies.project_discipline_fire_fighting'))
    drainage_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                             default=lambda self: self._get_discipline(
                                                 'hb_custom_ies.project_discipline_drinage'))
    civil_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                          default=lambda self: self._get_discipline(
                                              'hb_custom_ies.project_discipline_civil'))
    elv_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                        default=lambda self: self._get_discipline(
                                            'hb_custom_ies.project_discipline_elv'))
    mep_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                        default=lambda self: self._get_discipline(
                                            'hb_custom_ies.project_discipline_mep'))
    hvac_discipline_id = fields.Many2one('project.discipline', readonly=True,
                                         default=lambda self: self._get_discipline(
                                             'hb_custom_ies.project_discipline_hvac'))

    # Plumbing Related Fields
    total_plumbing_costing_amount = fields.Float(string="Total Amount(Exc Margin)",
                                                 compute="_compute_total_plumbing_costing_amount",
                                                 store=True)
    sub_total_plumbing_costing = fields.Float(string="Sub Total(Inc Margin)",
                                              compute="_compute_plumbing_sub_total",
                                              store=True)
    plumbing_margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    plumbing_margin_amount = fields.Float(
        string="Margin Amount",
        compute="_compute_plumbing_values",
        store=True,digits=(16, 3)
    )


    # water_supply Related Fields
    total_water_supply_costing_amount = fields.Float(string="Total Amount(Exc Margin)",
                                                     compute="_compute_water_supply_costing_amount",
                                                     store=True)
    sub_total_water_supply_costing = fields.Float(string="Sub Total(Inc Margin)",
                                                  compute="_compute_water_supply_sub_total",
                                                  store=True)
    water_supply_margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    water_supply_margin_amount = fields.Float(string="Margin Amount", digits=(16,3),compute="_compute_water_supply_sub_total",store=True,)

    # fire_alarm Related Fields
    fire_alarm_costing_amount = fields.Float(string="Total Amount(Exc Margin)",
                                             compute="_compute_fire_alarm_costing_amount",
                                             store=True)
    sub_total_fire_alarm_costing = fields.Float(string="Sub Total(Inc Margin)",
                                                compute="_compute_fire_alarm_sub_total",
                                                store=True)
    fire_alarm_margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    fire_alarm_margin_amount = fields.Float(string="Margin Amount",compute="_compute_fire_alarm_sub_total",store=True,
        digits=(16, 3))

    # fire_fighting Related Fields
    fire_fighting_costing_amount = fields.Float(string="Total Amount(Exc Margin)",
                                                compute="_compute_fire_fighting_costing_amount",
                                                store=True)
    sub_total_fire_fighting_costing = fields.Float(string="Sub Total(Inc Margin)",
                                                   compute="_compute_fire_fighting_sub_total",
                                                   store=True)
    fire_fighting_margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    fire_fighting_margin_amount= fields.Float(string="Margin Amount",compute="_compute_fire_fighting_sub_total",
        store=True,
        digits=(16, 3))

    # drainage Related Fields
    drainage_costing_amount = fields.Float(string="Total Amount(Exc Margin)",
                                           compute="_compute_drainage_costing_amount",
                                           store=True)
    sub_total_drainage_costing = fields.Float(string="Sub Total(Inc Margin)",
                                              compute="_compute_drainage_sub_total",
                                              store=True)
    drainage_margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    drainage_margin_amount = fields.Float(
        string="Margin Amount",
        compute="_compute_drainage_sub_total",
        store=True,
        digits=(16, 3)
    )

    # civil Related Fields
    civil_costing_amount = fields.Float(string="Total Amount(Exc Margin)",
                                        compute="_compute_civil_costing_amount",
                                        store=True)
    sub_total_civil_costing = fields.Float(string="Sub Total(Inc Margin)",
                                           compute="_compute_civil_sub_total",
                                           store=True)
    civil_margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    civil_margin_amount = fields.Float(
        string="Margin Amount",
        compute="_compute_civil_sub_total",
        store=True,
        digits=(16, 3)
    )

    # elv Related Fields
    elv_costing_amount = fields.Float(string="Total Amount(Exc Margin)",
                                      compute="_compute_elv_costing_amount",
                                      store=True)
    sub_total_elv_costing = fields.Float(string="Sub Total(Inc Margin)",
                                         compute="_compute_elv_sub_total",
                                         store=True)
    elv_margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    elv_margin_percentage_amount = fields.Float(
        string="Margin Amount",
        compute="_compute_elv_sub_total",
        store=True,
        digits=(16, 3)
    )

    # mep Related Fields
    mep_costing_amount = fields.Float(string="Total Amount(Exc Margin)",
                                      compute="_compute_mep_costing_amount",
                                      store=True)
    sub_total_mep_costing = fields.Float(string="Sub Total(Inc Margin)",
                                         compute="_compute_mep_sub_total",
                                         store=True)
    mep_margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    mep_margin_percentage_amount = fields.Float(
        string="Margin Amount",
        compute="_compute_mep_sub_total",
        store=True,
        digits=(16, 3)
    )

    # hvac Related Fields
    hvac_costing_amount = fields.Float(string="Total Amount(Exc Margin)",
                                       compute="_compute_hvac_costing_amount",
                                       store=True)
    sub_total_hvac_costing = fields.Float(string="Sub Total(Inc Margin)",
                                          compute="_compute_hvac_sub_total",
                                          store=True)
    hvac_margin_percentage = fields.Float(string="Margin (%)", digits=(16, 3))
    hvac_margin_percentage_amount = fields.Float(
        string="Margin Amount",
        compute="_compute_hvac_sub_total",
        store=True,
        digits=(16, 3)
    )

    revision_no = fields.Integer(string="Revision Number", default=0)
    revision_name = fields.Char(string="Revision", compute="_compute_revision_name", store=True)

    parent_revision_id = fields.Many2one('sale.order', string="Original Order")
    child_revision_ids = fields.One2many('sale.order', 'parent_revision_id', string="Revisions")
    is_revised = fields.Boolean(default=False)
    root_revision_id = fields.Many2one('sale.order', string="Root Order")

    def action_view_revisions(self):
        print('action_view_revisions')
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Revisions',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('parent_revision_id', '=', self.id)],
        }

    def action_prepare(self):
        self.state = 'prepared'

    def action_submit_quote(self):
        self.state = 'client_review'

    def action_revise_quote(self):
        if self.state == 'review':
            self.state = 'prepared'
        if self.state == 'client_review':
            root = self.root_revision_id or self
            new_order = self.copy({
                'revision_no': self.revision_no + 1,
                'parent_revision_id': self.id,
                'root_revision_id': root.id,
                'name': f"{root.name}/R{self.revision_no + 1}",
            })
            self.write({
                'state': 'revised',
                'is_revised': True,
            })
            root.write({
                'child_revision_ids': [new_order.id],
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': new_order.id,
                'view_mode': 'form',
                'target': 'current',
            }

    def action_reject_quote(self):
        self.state = 'loss'

    @api.depends('revision_no')
    def _compute_revision_name(self):
        for rec in self:
            rec.revision_name = f"R{rec.revision_no or 0}"

    def action_print_sale_quotation(self):
        print('action_print_sale_quotation')

    @api.depends('sub_total_costing', 'sub_total_plumbing_costing', 'sub_total_water_supply_costing',
                 'sub_total_fire_alarm_costing', 'sub_total_fire_fighting_costing',
                 'sub_total_drainage_costing', 'sub_total_civil_costing', 'sub_total_elv_costing',
                 'sub_total_mep_costing', 'sub_total_hvac_costing')
    def _compute_costing_total(self):
        for order in self:
            order.costing_total_amount = order.costing_total_amount = sum([
                order.sub_total_costing,
                order.sub_total_plumbing_costing,
                order.sub_total_water_supply_costing,
                order.sub_total_fire_alarm_costing,
                order.sub_total_fire_fighting_costing,
                order.sub_total_drainage_costing,
                order.sub_total_civil_costing,
                order.sub_total_elv_costing,
                order.sub_total_mep_costing,
                order.sub_total_hvac_costing
            ])

    def action_rfq_printout(self):
        self.ensure_one()
        return self.env.ref('bi_request_printout.action_report_custom_print').report_action(self)

    # hvac Supply Calculations
    @api.depends('hvac_costing_amount', 'hvac_margin_percentage')
    def _compute_hvac_sub_total(self):
        for order in self:
            total = order.hvac_costing_amount or 0.0
            margin_pct = order.hvac_margin_percentage or 0.0
            # ✅ Margin Amount calculation
            order.hvac_margin_percentage_amount = total * margin_pct / 100.0
            # ✅ Sub Total calculation
            order.sub_total_hvac_costing = total + order.hvac_margin_percentage_amount

    @api.depends('hvac_costing_lines.total_price')
    def _compute_hvac_costing_amount(self):
        for order in self:
            order.hvac_costing_amount = sum(order.hvac_costing_lines.mapped('total_price'))

    # mep Calculations
    @api.depends('mep_costing_amount', 'mep_margin_percentage')
    def _compute_mep_sub_total(self):
        for order in self:
            total = order.mep_costing_amount or 0.0
            margin_pct = order.mep_margin_percentage or 0.0
            # ✅ Margin Amount
            order.mep_margin_percentage_amount = total * margin_pct / 100.0
            # ✅ Sub Total
            order.sub_total_mep_costing = total + order.mep_margin_percentage_amount

    @api.depends('mep_costing_lines.total_price')
    def _compute_mep_costing_amount(self):
        for order in self:
            order.mep_costing_amount = sum(order.mep_costing_lines.mapped('total_price'))

    # elv Supply Calculations
    @api.depends('elv_costing_amount', 'elv_margin_percentage')
    def _compute_elv_sub_total(self):
        for order in self:
            total = order.elv_costing_amount or 0.0
            margin_pct = order.elv_margin_percentage or 0.0
            # ✅ Margin Amount
            order.elv_margin_percentage_amount = total * margin_pct / 100.0
            # ✅ Sub Total
            order.sub_total_elv_costing = total + order.elv_margin_percentage_amount

    @api.depends('elv_costing_lines.total_price')
    def _compute_elv_costing_amount(self):
        for order in self:
            order.elv_costing_amount = sum(order.elv_costing_lines.mapped('total_price'))

    # civil Supply Calculations
    @api.depends('civil_costing_amount', 'civil_margin_percentage')
    def _compute_civil_sub_total(self):
        for order in self:
            total = order.civil_costing_amount or 0.0
            margin_pct = order.civil_margin_percentage or 0.0
            # ✅ Margin Amount
            order.civil_margin_amount = total * margin_pct / 100.0
            # ✅ Sub Total
            order.sub_total_civil_costing = total + order.civil_margin_amount

    @api.depends('civil_costing_lines.total_price')
    def _compute_civil_costing_amount(self):
        for order in self:
            order.civil_costing_amount = sum(order.civil_costing_lines.mapped('total_price'))

    # drainage Supply Calculations
    @api.depends('drainage_costing_amount', 'drainage_margin_percentage')
    def _compute_drainage_sub_total(self):
        for order in self:
            total = order.drainage_costing_amount or 0.0
            margin_pct = order.drainage_margin_percentage or 0.0
            order.drainage_margin_amount = total * margin_pct / 100.0
            order.sub_total_drainage_costing = total + order.drainage_margin_amount


    @api.depends('drainage_costing_lines.total_price')
    def _compute_drainage_costing_amount(self):
        for order in self:
            order.drainage_costing_amount = sum(order.drainage_costing_lines.mapped('total_price'))

    # fire_fighting Supply Calculations
    @api.depends('fire_fighting_costing_amount', 'fire_fighting_margin_percentage')
    def _compute_fire_fighting_sub_total(self):
        for order in self:
            total = order.fire_fighting_costing_amount or 0.0
            margin_pct = order.fire_fighting_margin_percentage or 0.0
            # ✅ Calculate margin amount
            order.fire_fighting_margin_amount = total * margin_pct / 100.0

            # ✅ Calculate subtotal
            order.sub_total_fire_fighting_costing = total + order.fire_fighting_margin_amount
    @api.depends('fire_fighting_costing_lines.total_price')
    def _compute_fire_fighting_costing_amount(self):
        for order in self:
            order.fire_fighting_costing_amount = sum(
                order.fire_fighting_costing_lines.mapped('total_price'))

    # fire_alarm Supply Calculations
    @api.depends('fire_alarm_costing_amount', 'fire_alarm_margin_percentage')
    def _compute_fire_alarm_sub_total(self):
        for order in self:
            total = order.fire_alarm_costing_amount or 0.0
            margin_pct = order.fire_alarm_margin_percentage or 0.0
            order.fire_alarm_margin_amount = total * margin_pct / 100.0
            order.sub_total_fire_alarm_costing = total + order.fire_alarm_margin_amount

    @api.depends('fire_alarm_costing_lines.total_price')
    def _compute_fire_alarm_costing_amount(self):
        for order in self:
            order.fire_alarm_costing_amount = sum(
                order.fire_alarm_costing_lines.mapped('total_price'))

    # Water Supply Calculations
    @api.depends('total_water_supply_costing_amount', 'water_supply_margin_percentage')
    def _compute_water_supply_sub_total(self):
        for order in self:
            total = order.total_water_supply_costing_amount or 0.0
            margin_pct = order.water_supply_margin_percentage or 0.0
            order.water_supply_margin_amount = total * margin_pct / 100.0
            order.sub_total_water_supply_costing = total + order.water_supply_margin_amount

    @api.depends('water_supply_costing_lines.total_price')
    def _compute_water_supply_costing_amount(self):
        for order in self:
            order.total_water_supply_costing_amount = sum(
                order.water_supply_costing_lines.mapped('total_price'))

    # Plumbing Calculations
    @api.depends('total_plumbing_costing_amount', 'plumbing_margin_percentage')
    def _compute_plumbing_values(self):
        for order in self:
            base = order.total_plumbing_costing_amount or 0.0
            margin = (base * order.plumbing_margin_percentage) / 100.0

            order.plumbing_margin_amount = margin
            order.sub_total_plumbing_costing = base + margin

    @api.depends('plumbing_costing_lines.total_price')
    def _compute_total_plumbing_costing_amount(self):
        for order in self:
            order.total_plumbing_costing_amount = sum(
                order.plumbing_costing_lines.mapped('total_price'))

    # Electrical Calculations
    @api.depends('sale_costing_lines.total_price')
    def _compute_total_costing_amount(self):
        for order in self:
            order.total_costing_amount = sum(order.sale_costing_lines.mapped('total_price'))

    # @api.depends('total_costing_amount', 'margin_percentage')
    # def _compute_sub_total(self):
    #     for order in self:
    #         order.sub_total_costing = order.total_costing_amount + (
    #                 order.total_costing_amount * order.margin_percentage / 100.0) if order.total_costing_amount else 0.0

    @api.depends('total_costing_amount', 'margin_percentage')
    def _compute_sub_total(self):
        for rec in self:
            if rec.total_costing_amount:
                rec.margin_amount = (
                        rec.total_costing_amount * rec.margin_percentage / 100.0
                )
                rec.sub_total_costing = rec.total_costing_amount + rec.margin_amount
            else:
                rec.margin_amount = 0.0
                rec.sub_total_costing = 0.0
    def action_review(self):
        for rec in self:
            if rec.is_fire_alarm:
                if rec.sub_total_costing != rec.amount_untaxed:
                    raise ValidationError(
                        _("Total with Margin for Fire Alarm must be equal to the Untaxed Amount."))
            rec.state = 'review'

    def action_approve(self):
        for rec in self:
            rec.action_confirm_custom()

    def action_close(self):
        for rec in self:
            rec.state = 'closed'

    def action_return(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Return Reason',
            'res_model': 'sale.return.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id}
        }

    def action_confirm_custom(self):
        self.state = 'draft'  # Reset to draft before confirming to trigger workflow
        print('state', self.state)
        self.action_confirm()

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        default_html = """
            <div style="font-size:12px; line-height:1.6;">

                <b><u>Electrical Light Points:</u></b><br/>
                Supply, Installation, Testing &amp; Commissioning of light points with PVC conduits,
                GI trunking, 2.5 Sqmm wires, light fittings installation and associated accessories.
                <b>(Light supply by the main fit-out contractor / Client).</b>

                <div style="margin-left:18px; margin-top:6px;">
                    Light Points – Dining Area : <b>28 Nos</b><br/>
                    Light Points – Landscape &amp; External : <b>22 Nos</b><br/>
                    Light Points – Kitchen &amp; Office : <b>14 Nos</b>
                </div>

                <br/>

                <b><u>Electrical Power:</u></b><br/>
                Supply, Installation, Testing &amp; Commissioning of power points with PVC conduits,
                wires (4 Sqmm &amp; 6 Sqmm depending on the load), GI trunking, SMDB, DBs,
                armored cabling, sockets, isolators, fittings, supports and associated accessories.
                <b>(Make: Schneider / ABB / SCAME).</b>

                <div style="margin-left:18px; margin-top:6px;">
                    Power Points – Dining Area : <b>10 Nos</b><br/>
                    Power Points – Landscape &amp; External : <b>6 Nos</b><br/>
                    Power Points – Kitchen &amp; Office : <b>11 Nos</b><br/>
                    DB, Cabling, Tray &amp; Trunking : <b>1 Item</b>
                </div>

                <br/>

                <b><u>Drainage &amp; Water Supply:</u></b><br/>
                Supply, Installation, Testing &amp; Commissioning of drainage network with UPVC piping,
                water pipe network with PPR pipes, water heater, associated fittings and accessories.

                <div style="margin-left:18px; margin-top:6px;">
                    Drainage &amp; Water Supply Works : <b>1 Item</b>
                </div>

            </div>
            """

        res.setdefault('note', default_html)
        return res

    @api.depends('order_line.price_subtotal', 'order_line.price_tax')
    def _amount_all(self):
        """
        Compute SO totals from order lines.
        """
        for order in self:
            order.amount_untaxed = sum(order.order_line.mapped('price_subtotal'))
            order.amount_tax = sum(order.order_line.mapped('price_tax'))
            order.amount_total = order.amount_untaxed + order.amount_tax

    def _get_roman_month(self, month):
        roman = {
            1: 'I', 2: 'II', 3: 'III', 4: 'IV',
            5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII',
            9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
        }
        return roman.get(month)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            seq = self.env['ir.sequence'].next_by_code('sale.custom.seq')
            if seq:
                today = fields.Date.today()
                roman_month = self._get_roman_month(today.month)

                seq = seq.replace(
                    today.strftime('%y') + '/',
                    today.strftime('%y') + '/' + roman_month + '/'
                )

                vals['name'] = seq

        return super(SaleOrder, self).create(vals)

    project_name = fields.Many2one(
        "crm.lead", string="Project Name"
    )
    project_type = fields.Selection(
        related='project_name.project_type',
        string="Project Type",
        readonly=True
    )
    scope_work = fields.Char(
        related='project_name.scope_title',
        string="Scope of Work",
        readonly=True
    )

    is_electrical = fields.Boolean(
        string="Is Electrical",
        default=False
    )

    electrical_line_ids = fields.One2many(
        comodel_name='sale.electrical.line',
        inverse_name='line_id',
        string='Electrical Lines',

    )
    amount_electric = fields.Float(
        string="Amount",
        store=True,
        digits="Product Unit of Measure",
    )
    # subtotal_amount_electric = fields.Float(
    #     string="Total Amount Electric",
    #     compute='_compute_subtotal_amount_electric',
    #     store=True,
    #     digits="Product Unit of Measure",
    # )
    margin_percentage_electric = fields.Float(
        string="Margin Electric (%)",
        digits=(16, 2)
    )
    margin_amount_electric = fields.Float(
        string='Margin Amount Electric',
        compute="_compute_margin_amount_electric",
        store=True
    )
    subtotal_amount_electric = fields.Float(
        string="Total Amount Electric",
        compute="_compute_subtotal_amount_electric",
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('electrical_line_ids.total_price')
    def _compute_subtotal_amount_electric(self):
        for order in self:
            order.subtotal_amount_electric = sum(
                order.electrical_line_ids.mapped('total_price')

            )

        # 🔹 NEW: compute margin amount

    @api.depends('subtotal_amount_electric', 'margin_percentage_electric')
    def _compute_margin_amount_electric(self):
        for order in self:
            if order.subtotal_amount_electric and order.margin_percentage_electric:
                order.margin_amount_electric = (
                        order.subtotal_amount_electric * order.margin_percentage_electric / 100.0
                )
            else:
                order.margin_amount_electric = 0.0

    total_with_margin_electric = fields.Float(
        string="Total With Margin Electric",
        compute="_compute_total_with_margin_electric",
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('subtotal_amount_electric', 'margin_amount_electric')
    def _compute_total_with_margin_electric(self):
        for order in self:
            if order.subtotal_amount_electric:
                order.total_with_margin_electric = (
                        order.subtotal_amount_electric + order.margin_amount_electric
                )
            else:
                order.total_with_margin_electric = 0.0

    # @api.depends('subtotal_amount_electric', 'margin_percentage_electric')
    # def _compute_total_with_margin_electric(self):
    #     for order in self:
    #         if order.subtotal_amount_electric:
    #             order.total_with_margin_electric = (
    #                     order.subtotal_amount_electric
    #                     + (order.subtotal_amount_electric * order.margin_percentage_electric / 100)
    #             )
    #         else:
    #             order.total_with_margin_electric = 0.0
    ##########################HVAC######################################
    is_hvac = fields.Boolean(
        string="Is Hvac",
        default=False
    )

    hvac_line_ids = fields.One2many(
        comodel_name='sale.hvac.line',
        inverse_name='line_id',
        string='HVAC Lines',

    )
    amount_hvac = fields.Float(
        string="Amount",
        store=True,
        digits="Product Unit of Measure",
    )
    subtotal_amount_hvac = fields.Float(
        string="Total Amount",
        compute='_compute_subtotal_amount_hvac',
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('hvac_line_ids.total_price')
    def _compute_subtotal_amount_hvac(self):
        for order in self:
            order.subtotal_amount_hvac = sum(
                order.hvac_line_ids.mapped('total_price')
            )

    margin_percentage_hvac = fields.Float(
        string="Margin (%)",
        digits=(16, 2)
    )
    margin_amount_hvac = fields.Float(
        string='Margin Amount Hvac',
        compute="_compute_margin_amount_hvac",
        store=True
    )
    total_with_margin_hvac = fields.Float(
        string="Total With Margin Hvac",
        compute="_compute_total_with_margin_hvac",
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('subtotal_amount_hvac', 'margin_percentage_hvac')
    def _compute_margin_amount_hvac(self):
        for order in self:
            if order.subtotal_amount_hvac and order.margin_percentage_hvac:
                order.margin_amount_hvac = (
                        order.subtotal_amount_hvac * order.margin_percentage_hvac / 100.0
                )
            else:
                order.margin_amount_hvac = 0.0

    @api.depends('subtotal_amount_hvac', 'margin_amount_hvac')
    def _compute_total_with_margin_hvac(self):
        for order in self:
            if order.subtotal_amount_hvac:
                order.total_with_margin_hvac = (
                        order.subtotal_amount_hvac + order.margin_amount_hvac
                )
            else:
                order.total_with_margin_hvac = 0.0

    ##################Sundering########################################

    sun_line_ids = fields.One2many('sun.items', 'line_id', string="Item")

    # def action_creating_costing(self):
    #     """Generate Costing Action"""
    #     costing_product = self.env['product.product'].search([
    #         ('is_costing_charge', '=', True),
    #     ], limit=1)
    #
    #     if not costing_product:
    #         raise ValidationError("No service product with costing charge found!")
    #     unit_price = (
    #             (self.subtotal_amount_hvac or 0.0)
    #             + (self.subtotal_amount_electric or 0.0)
    #             + (getattr(self, 'subtotal_amount_mep', 0.0) or 0.0)
    #             + (self.subtotal_amount_plumbing or 0.0)
    #             + (self.subtotal_amount_water_supply or 0.0)
    #     )
    #     self.env['sale.order.line'].create({
    #         'order_id': self.id,
    #         'product_id': costing_product.id,
    #         'product_uom_qty': 1.0,
    #         'product_uom': costing_product.uom_id.id,
    #         'price_unit': unit_price,
    #         'tax_id': [(6, 0, costing_product.taxes_id.ids)],
    #     })

    ############################General####################
    general_line_ids = fields.One2many('sale.general', 'line_id', string="General Item")

    ################Depath Measurement#############################

    measurement_line_ids = fields.One2many('sale.measurement', 'line_id', string="Measurement Item")
    ######################## Measurement######################################
    new_line_ids = fields.One2many(
        'mesurement.measurement',
        'line_id',
        string="Measurements"
    )

    ####################MEP##########################

    is_mep = fields.Boolean(
        string="Is MEP",
        default=False
    )
    mep_line_ids = fields.One2many(
        comodel_name='sale.mep.line',
        inverse_name='line_id',
        string='MEP Lines',

    )
    amount_mep = fields.Float(
        string="Amount",
        store=True,
        digits="Product Unit of Measure",
    )
    subtotal_amount_mep = fields.Float(
        string="Total Amount",
        compute='_compute_subtotal_amount_mep',
        store=True,
        digits="Product Unit of Measure",
    )
    margin_percentage_mep = fields.Float(
        string="Margin (%)",
        digits=(16, 2)
    )

    margin_amount_mep = fields.Float(
        string='Margin Amount Mep',
        compute="_compute_margin_amount_mep",
        store=True
    )

    @api.depends('mep_line_ids.total_price')
    def _compute_subtotal_amount_mep(self):
        for order in self:
            order.subtotal_amount_mep = sum(
                order.mep_line_ids.mapped('total_price')
            )

    total_with_margin_mep = fields.Float(
        string="Total With Margin Mep",
        compute="_compute_total_with_margin_mep",
        store=True,
        digits="Product Unit of Measure",
    )

    # 🔹 NEW: compute margin amount
    @api.depends('subtotal_amount_mep', 'margin_percentage_mep')
    def _compute_margin_amount_mep(self):
        for order in self:
            if order.subtotal_amount_mep and order.margin_percentage_mep:
                order.margin_amount_mep = (
                        order.subtotal_amount_mep * order.margin_percentage_mep / 100.0
                )
            else:
                order.margin_amount_mep = 0.0

    @api.depends('subtotal_amount_mep', 'margin_amount_mep')
    def _compute_total_with_margin_mep(self):
        for order in self:
            if order.subtotal_amount_mep:
                order.total_with_margin_mep = (
                        order.subtotal_amount_mep + order.margin_amount_mep
                )
            else:
                order.total_with_margin_mep = 0.0

    ####################PLUMBING##########################
    is_plumbing = fields.Boolean(
        string="Is PLUMBING",
        default=False
    )
    plumbing_line_ids = fields.One2many(
        comodel_name='sale.plumbing.line',
        inverse_name='line_id',
        string='Plumbing Lines',

    )
    amount_plumbing = fields.Float(
        string="Amount",
        store=True,
        digits="Product Unit of Measure",
    )
    margin_percentage_plumbing = fields.Float(
        string="Margin (%)",
        digits=(16, 2)
    )

    margin_amount_plumbing = fields.Float(
        string='Margin Amount Plumbing',
        compute="_compute_margin_amount_plumbing",
        store=True
    )

    subtotal_amount_plumbing = fields.Float(
        string="Total Amount Plumbing",
        compute="_compute_subtotal_amount_plumbing",
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('plumbing_line_ids.total_price')
    def _compute_subtotal_amount_plumbing(self):
        for order in self:
            order.subtotal_amount_plumbing = sum(
                order.plumbing_line_ids.mapped('total_price')
            )

    # 🔹 NEW: compute margin amount
    @api.depends('subtotal_amount_plumbing', 'margin_percentage_plumbing')
    def _compute_margin_amount_plumbing(self):
        for order in self:
            if order.subtotal_amount_plumbing and order.margin_percentage_plumbing:
                order.margin_amount_plumbing = (
                        order.subtotal_amount_plumbing * order.margin_percentage_plumbing / 100.0
                )
            else:
                order.margin_amount_plumbing = 0.0

    total_with_margin_plumbing = fields.Float(
        string="Total With Margin Plumbing",
        compute="_compute_total_with_margin_plumbing",
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('subtotal_amount_plumbing', 'margin_amount_plumbing')
    def _compute_total_with_margin_plumbing(self):
        for order in self:
            if order.subtotal_amount_plumbing:
                order.total_with_margin_plumbing = (
                        order.subtotal_amount_plumbing + order.margin_amount_plumbing
                )
            else:
                order.total_with_margin_plumbing = 0.0

    # @api.depends('plumbing_line_ids.total_price')
    # def _compute_subtotal_amount_plumbing(self):
    #     for order in self:
    #         order.subtotal_amount_plumbing = sum(
    #             order.plumbing_line_ids.mapped('total_price')
    #
    #         )

    ##############################Water Supply#########################

    is_water_supply = fields.Boolean(
        string="Is Water Supply",
        default=False
    )
    water_supply_line_ids = fields.One2many(
        comodel_name='sale.water.supply.line',
        inverse_name='line_id',
        string='Water Supply Lines',

    )
    amount_water_supply = fields.Float(
        string="Amount",
        store=True,
        digits=(16, 3)
    )
    subtotal_amount_water_supply = fields.Float(
        string="Total Amount",
        compute='_compute_subtotal_amount_water_supply',
        store=True,
        digits=(16, 3)
    )
    margin_percentage_water = fields.Float(
        string="Margin (%)",
        digits=(16, 2)
    )
    margin_amount_water = fields.Float(
        string='Margin Amount Water',
        compute="_compute_margin_amount_water_supply",
        store=True
    )

    @api.depends('water_supply_line_ids.total_price')
    def _compute_subtotal_amount_water_supply(self):
        for order in self:
            order.subtotal_amount_water_supply = sum(
                order.water_supply_line_ids.mapped('total_price')

            )

    total_with_margin_water = fields.Float(
        string="Total With Margin Water",
        compute="_compute_total_with_margin_water",
        store=True,
        digits="Product Unit of Measure",
    )

    # 🔹 NEW: compute margin amount
    @api.depends('subtotal_amount_water_supply', 'margin_percentage_water')
    def _compute_margin_amount_water_supply(self):
        for order in self:
            if order.subtotal_amount_water_supply and order.margin_percentage_water:
                order.margin_amount_water = (
                        order.subtotal_amount_water_supply * order.margin_percentage_water / 100.0
                )
            else:
                order.margin_amount_water = 0.0

    @api.depends('subtotal_amount_water_supply', 'margin_amount_water')
    def _compute_total_with_margin_water(self):
        for order in self:
            if order.subtotal_amount_water_supply:
                order.total_with_margin_water = (
                        order.subtotal_amount_water_supply + order.margin_amount_water
                )
            else:
                order.total_with_margin_water = 0.0

    ##############################Drainage#########################

    is_drainage = fields.Boolean(
        string="Is Drainage",
        default=False
    )
    drainage_line_ids = fields.One2many(
        comodel_name='sale.drainage.line',
        inverse_name='line_id',
        string='Water Supply Lines',

    )
    amount_drainage = fields.Float(
        string="Amount",
        store=True,
        digits=(16, 3)
    )
    subtotal_amount_drainage = fields.Float(
        string="Total Amount",
        compute='_compute_subtotal_amount_drainage',
        store=True,
        digits=(16, 3)
    )

    @api.depends('drainage_line_ids.total_price')
    def _compute_subtotal_amount_drainage(self):
        for order in self:
            order.subtotal_amount_drainage = sum(
                order.drainage_line_ids.mapped('total_price')

            )

    margin_percentage_drainage = fields.Float(
        string="Margin (%)",
        digits=(16, 2)
    )
    margin_amount_drainage = fields.Float(
        string='Margin Amount Drainage',
        compute="_compute_margin_amount_drainage",
        store=True
    )

    total_with_margin_drainage = fields.Float(
        string="Total With Margin Drainage",
        compute="_compute_total_with_margin_drainage",
        store=True,
        digits="Product Unit of Measure",
    )

    # 🔹 NEW: compute margin amount
    @api.depends('subtotal_amount_drainage', 'margin_percentage_drainage')
    def _compute_margin_amount_drainage(self):
        for order in self:
            if order.subtotal_amount_drainage and order.margin_percentage_drainage:
                order.margin_amount_drainage = (
                        order.subtotal_amount_drainage * order.margin_percentage_drainage / 100.0
                )
            else:
                order.margin_amount_drainage = 0.0

    @api.depends('subtotal_amount_drainage', 'margin_amount_drainage')
    def _compute_total_with_margin_drainage(self):
        for order in self:
            if order.subtotal_amount_drainage:
                order.total_with_margin_drainage = (
                        order.subtotal_amount_water_drainage + order.margin_amount_drainage
                )
            else:
                order.total_with_margin_drainage = 0.0

    ##############################Civil#########################

    is_civil = fields.Boolean(
        string="Is Civil",
        default=False
    )
    civil_line_ids = fields.One2many(
        comodel_name='sale.civil.line',
        inverse_name='line_id',
        string='Civil Lines',

    )
    amount_civil = fields.Float(
        string="Amount",
        store=True,
        digits="Product Unit of Measure",
    )
    subtotal_amount_civil = fields.Float(
        string="Total Amount",
        compute='_compute_subtotal_amount_civil',
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('civil_line_ids.total_price')
    def _compute_subtotal_amount_civil(self):
        for order in self:
            order.subtotal_amount_civil = sum(
                order.civil_line_ids.mapped('total_price')

            )

    margin_percentage_civil = fields.Float(
        string="Margin (%)",
        digits=(16, 2)
    )

    total_with_margin_civil = fields.Float(
        string="Total With Margin Civil",
        compute="_compute_total_with_margin_civil",
        store=True,
        digits="Product Unit of Measure",
    )
    margin_amount_civil = fields.Float(
        string='Margin Amount Civil',
        compute="_compute_margin_amount_civil",
        store=True
    )

    # 🔹 NEW: compute margin amount
    @api.depends('subtotal_amount_civil', 'margin_percentage_civil')
    def _compute_margin_amount_civil(self):
        for order in self:
            if order.subtotal_amount_civil and order.margin_percentage_civil:
                order.margin_amount_civil = (
                        order.subtotal_amount_civil * order.margin_percentage_civil / 100.0
                )
            else:
                order.margin_amount_civil = 0.0

    @api.depends('subtotal_amount_civil', 'margin_amount_civil')
    def _compute_total_with_margin_civil(self):
        for order in self:
            if order.subtotal_amount_civil:
                order.total_with_margin_civil = (
                        order.subtotal_amount_civil + order.margin_amount_civil
                )
            else:
                order.total_with_margin_civil = 0.0

    ##############################Civil#########################

    is_elv = fields.Boolean(
        string="Is ELV",
        default=False
    )
    elv_line_ids = fields.One2many(
        comodel_name='sale.elv.line',
        inverse_name='line_id',
        string='ELV Lines',

    )
    amount_elv = fields.Float(
        string="Amount",
        store=True,
        digits="Product Unit of Measure",
    )
    subtotal_amount_elv = fields.Float(
        string="Total Amount",
        compute='_compute_subtotal_amount_elv',
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('elv_line_ids.total_price')
    def _compute_subtotal_amount_elv(self):
        for order in self:
            order.subtotal_amount_elv = sum(
                order.elv_line_ids.mapped('total_price')

            )

    margin_percentage_elv = fields.Float(
        string="Margin (%)",
        digits=(16, 2)
    )

    total_with_margin_elv = fields.Float(
        string="Total With Margin Elv",
        compute="_compute_total_with_margin_elv",
        store=True,
        digits="Product Unit of Measure",
    )
    margin_amount_elv = fields.Float(
        string='Margin Amount Elv',
        compute="_compute_margin_amount_elv",
        store=True
    )

    # 🔹 NEW: compute margin amount
    @api.depends('subtotal_amount_elv', 'margin_percentage_elv')
    def _compute_margin_amount_elv(self):
        for order in self:
            if order.subtotal_amount_elv and order.margin_percentage_elv:
                order.margin_amount_elv = (
                        order.subtotal_amount_elv * order.margin_percentage_elv / 100.0
                )
            else:
                order.margin_amount_elv = 0.0

    @api.depends('subtotal_amount_elv', 'margin_amount_elv')
    def _compute_total_with_margin_elv(self):
        for order in self:
            if order.subtotal_amount_elv:
                order.total_with_margin_elv = (
                        order.subtotal_amount_elv + order.margin_amount_elv
                )
            else:
                order.total_with_margin_elv = 0.0

    ##############################Civil65#########################

    is_fire_fighting = fields.Boolean(
        string="Is Fire fighting",
        default=False
    )
    fire_fighting_line_ids = fields.One2many(
        comodel_name='sale.fire.fighting.line',
        inverse_name='line_id',
        string='Fire fighting Lines',

    )
    amount_fire_fighting = fields.Float(
        string="Amount",
        store=True,
        digits="Product Unit of Measure",
    )
    subtotal_amount_fire_fighting = fields.Float(
        string="Total Amount",
        compute='_compute_subtotal_amount_fire_fighting',
        store=True,
        digits="Product Unit of Measure",
    )

    @api.depends('fire_fighting_line_ids.total_price')
    def _compute_subtotal_amount_fire_fighting(self):
        for order in self:
            order.subtotal_amount_fire_fighting = sum(
                order.fire_fighting_line_ids.mapped('total_price')
            )

    margin_percentage_fire_fighting = fields.Float(
        string="Margin (%)",
        digits=(16, 2)
    )

    total_with_margin_fire_fighting = fields.Float(
        string="Total With Margin Fire Fighting",
        compute="_compute_total_with_margin_fire_fighting",
        store=True,
        digits="Product Unit of Measure",
    )
    margin_amount_fire_fighting = fields.Float(
        string='Margin Amount Fire Fighting',
        compute="_compute_margin_amount_fire_fighting",
        store=True
    )

    # 🔹 NEW: compute margin amount
    @api.depends('subtotal_amount_fire_fighting', 'margin_percentage_fire_fighting')
    def _compute_margin_amount_fire_fighting(self):
        for order in self:
            if order.subtotal_amount_fire_fighting and order.margin_percentage_fire_fighting:
                order.margin_amount_fire_fighting = (
                        order.subtotal_amount_fire_fighting * order.margin_percentage_fire_fighting / 100.0
                )
            else:
                order.margin_amount_fire_fighting = 0.0

    @api.depends('subtotal_amount_fire_fighting', 'margin_amount_fire_fighting')
    def _compute_total_with_margin_fire_fighting(self):
        for order in self:
            if order.subtotal_amount_fire_fighting:
                order.total_with_margin_fire_fighting = (
                        order.subtotal_amount_fire_fighting + order.margin_amount_fire_fighting
                )
            else:
                order.total_with_margin_fire_fighting = 0.0

    ##############################Civil#########################

    is_fire_alarm = fields.Boolean(
        string="Is Fire alarm",
        default=False
    )
    fire_alarm_line_ids = fields.One2many(
        comodel_name='sale.fire.alarm.line',
        inverse_name='line_id',
        string='Fire alarm Lines',

    )
    amount_fire_alarm = fields.Float(
        string="Amount",
        store=True,
        digits="Product Unit of Measure",
    )
    subtotal_amount_fire_alarm = fields.Float(
        string="Total Amount",
        compute='_compute_subtotal_amount_fire_alarm',
        store=True,
        digits="Product Unit of Measure",
    )
    margin_percentage_fire_alarm = fields.Float(
        string="Margin (%)",
        digits=(16, 2)
    )

    total_with_margin_fire_alarm = fields.Float(
        string="Total With Margin Fire Fighting",
        compute="_compute_total_with_margin_fire_alarm",
        store=True,
        digits="Product Unit of Measure",
    )
    margin_amount_fire_alarm = fields.Float(
        string='Margin Amount Fire Alarm',
        compute="_compute_margin_amount_fire_alarm",
        store=True
    )

    # 🔹 NEW: compute margin amount
    @api.depends('subtotal_amount_fire_alarm', 'margin_percentage_fire_alarm')
    def _compute_margin_amount_fire_alarm(self):
        for order in self:
            if order.subtotal_amount_fire_alarm and order.margin_percentage_fire_alarm:
                order.margin_amount_fire_alarm = (
                        order.subtotal_amount_fire_alarm * order.margin_percentage_fire_alarm / 100.0
                )
            else:
                order.margin_amount_fire_alarm = 0.0

    @api.depends('subtotal_amount_fire_alarm', 'margin_amount_fire_alarm')
    def _compute_total_with_margin_fire_alarm(self):
        for order in self:
            if order.subtotal_amount_fire_alarm:
                order.total_with_margin_fire_alarm = (
                        order.subtotal_amount_fire_alarm + order.margin_amount_fire_alarm
                )
            else:

                order.total_with_margin_fire_alarm = 0.0

    @api.depends('fire_alarm_line_ids.total_price')
    def _compute_subtotal_amount_fire_alarm(self):
        for order in self:
            order.subtotal_amount_fire_alarm = sum(
                order.fire_alarm_line_ids.mapped('total_price')
            )

    @api.depends(
        'order_line.price_subtotal',
        'order_line.price_tax'
    )
    def _amount_all(self):
        for order in self:
            amount_untaxed = sum(order.order_line.mapped('price_subtotal'))
            amount_tax = sum(order.order_line.mapped('price_tax'))

            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_amount = fields.Float(string='Margin Amount', digits=(16, 3))
    note = fields.Text(string='Description')
    unit = fields.Selection(
        selection=[
            ('item', 'Item'),
            ('nos', 'Nos'),
            ('meter', 'Meter'),
            ('ls', 'Ls'),
        ],
        string='Unit',
        default='item'
    )
    # # discount = fields.Float(string="Discount (%)", digits="Discount", default=0.0)
    #
    # @api.depends('product_uom_qty', 'price_unit', 'margin_amount', 'tax_id')
    # def _compute_amount(self):
    #     """
    #     Subtotal = (price_unit + margin_amount) * quantity
    #     """
    #     for line in self:
    #         price = (line.price_unit or 0.0) + (line.margin_amount or 0.0)
    #
    #         taxes = line.tax_id.compute_all(
    #             price,
    #             line.order_id.currency_id,
    #             line.product_uom_qty,
    #             product=line.product_id,
    #             partner=line.order_id.partner_id,
    #         )
    #
    #         line.price_subtotal = taxes['total_excluded']
    #         line.price_tax = taxes['total_included'] - taxes['total_excluded']
    #         line.price_total = taxes['total_included']

    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'margin_amount')
    # def _compute_amount(self):
    #     super()._compute_amount()
    #     for line in self:
    #         margin = line.product_uom_qty * line.margin_amount
    #         print("margin",margin)
    #         line.price_subtotal += margin
    #         line.price_total += margin
    #         print("nnnnnnnnnnnnnn")
    #         line.price_tax += line.price_total - line.price_subtotal

    product_electric_id = fields.Many2one(
        'electrical.item',
        string='Electrical'
    )

    qty_electric = fields.Float(
        string="Quantity",
        default=1.0,
        digits=(16, 3)
    )

    unit_price_electric = fields.Float(
        string="Unit Price",
        readonly=True,
        digits=(16, 3)
    )

    m_unit_measures = fields.Selection(
        [
            ('m', 'Meter'),
            ('cm', 'Centimeter'),
            ('mm', 'Millimeter')
        ],
        string="Unit Measure",
        default='m'
    )

    amount_electric = fields.Float(
        string="Amount",
        compute='_compute_amount_electric',
        store=True,
        digits=(16, 3)
    )

    @api.onchange('product_electric_id')
    def _onchange_product_electric_id(self):
        for line in self:
            if line.product_electric_id:
                line.unit_price_electric = line.product_electric_id.unit_rate
                line.price_unit = line.product_electric_id.unit_rate

    @api.depends('qty_electric', 'unit_price_electric')
    def _compute_amount_electric(self):
        for line in self:
            line.amount_electric = (line.qty_electric or 0.00) * (line.unit_price_electric or 0.00)

    #################HVAC###################################

    product_hvac_id = fields.Many2one(
        'hvac.item',
        string='HVAC'
    )

    qty_hvac = fields.Float(
        string="Quantity",
        default=1.0,
        digits=(16, 3)
    )

    unit_price_hvac = fields.Float(
        string="Unit Price",
        readonly=True,
        digits=(16, 3)
    )

    h_unit_measures = fields.Selection(
        [
            ('m', 'Meter'),
            ('cm', 'Centimeter'),
            ('mm', 'Millimeter')
        ],
        string="Unit Measure",
        default='m'
    )

    amount_hvac = fields.Float(
        string="Amount",
        compute='_compute_amount_hvac',
        store=True,
        digits=(16, 3)
    )

    @api.onchange('product_hvac_id')
    def _onchange_product_hvac(self):
        for line in self:
            if line.product_hvac_id:
                line.unit_price_hvac = line.product_hvac_id.hv_unit_rate
                line.price_unit = line.product_hvac_id.hv_unit_rate

    # @api.onchange('product_hvac_id')
    # def _onchange_product_hvac_id(self):
    #     for line in self:
    #         if line.product_hvac_id:
    #             line.unit_price_hvac = line.product_hvac_id.hv_unit_rate
    #             line.price_unit = line.product_hvac_id.hv_unit_rate
    #
    # # @api.onchange('product_hvac_id')
    # # def _onchange_product_hvac_id(self):
    # #     if self.product_hvac_id:
    # #         self.unit_price_hvac = self.product_hvac_id.hv_unit_rate or 0.0
    #
    @api.depends('qty_hvac', 'unit_price_hvac')
    def _compute_amount_hvac(self):
        for line in self:
            line.amount_hvac = (line.qty_hvac or 0.00) * (line.unit_price_hvac or 0.00)

    ###############################MEP##################################

    product_mep_id = fields.Many2one(
        'mep.item',
        string='MEP'
    )

    qty_mep = fields.Float(
        string="Quantity",
        default=1.0,
        digits=(16, 3)
    )

    unit_price_mep = fields.Float(
        string="Unit Price",
        readonly=True,
        digits=(16, 3)
    )

    mep_unit_measures = fields.Selection(
        [
            ('m', 'Meter'),
            ('cm', 'Centimeter'),
            ('mm', 'Millimeter')
        ],
        string="Unit Measure",
        default='m'
    )

    amount_mep = fields.Float(
        string="Amount",
        compute='_compute_amount_mep',
        store=True,
        digits=(16, 3)
    )

    @api.onchange('product_mep_id')
    def _onchange_product_mep_id(self):
        for line in self:
            if line.product_mep_id:
                line.unit_price_mep = line.product_mep_id.mep_unit_rate
                line.price_unit = line.product_mep_id.mep_unit_rate

    @api.depends('qty_mep', 'unit_price_mep')
    def _compute_amount_mep(self):
        for line in self:
            line.amount_mep = (line.qty_mep or 0.00) * (line.unit_price_mep or 0.00)

    ####################PLUMBING###########################

    product_plumbing_id = fields.Many2one(
        'plumbing',
        string='Plumbing'
    )

    qty_plumbing = fields.Float(
        string="Quantity",
        default=1.0,
        digits=(16, 3)
    )

    unit_price_plumbing = fields.Float(
        string="Unit Price",
        readonly=True,
        digits=(16, 3)
    )

    plumbing_unit_measures = fields.Selection(
        [
            ('m', 'Meter'),
            ('cm', 'Centimeter'),
            ('mm', 'Millimeter')
        ],
        string="Unit Measure",
        default='m'
    )

    amount_plumbing = fields.Float(
        string="Amount",
        compute='_compute_amount_plumbing',
        store=True,
        digits=(16, 3)
    )

    @api.onchange('product_plumbing_id')
    def _onchange_product_plumbing_id(self):
        for line in self:
            if line.product_plumbing_id:
                line.unit_price_plumbing = line.product_plumbing_id.plumbing_unit_rate
                line.price_unit = line.product_plumbing_id.plumbing_unit_rate

    @api.depends('qty_plumbing', 'unit_price_plumbing')
    def _compute_amount_plumbing(self):
        for line in self:
            line.amount_plumbing = (line.qty_plumbing or 0.00) * (line.unit_price_plumbing or 0.00)

    ######################Water Supply##################################

    product_water_supply_id = fields.Many2one(
        'water.supply',
        string='Water Supply'
    )

    qty_water_supply = fields.Float(
        string="Quantity",
        default=1.0,
        digits=(16, 3)
    )

    unit_price_water_supply = fields.Float(
        string="Unit Price",
        readonly=True,
        digits=(16, 3)
    )

    water_supply_unit_measures = fields.Selection(
        [
            ('m', 'Meter'),
            ('cm', 'Centimeter'),
            ('mm', 'Millimeter')
        ],
        string="Unit Measure",
        default='m'
    )

    amount_water_supply = fields.Float(
        string="Amount",
        compute='_compute_amount_water_supply',
        store=True,
        digits=(16, 3)
    )

    @api.onchange('product_water_supply_id')
    def _onchange_product_water_supply_id(self):
        for line in self:
            if line.product_water_supply_id:
                line.unit_price_water_supply = line.product_water_supply_id.water_unit_rate
                line.price_unit = line.product_water_supply_id.water_unit_rate

    @api.depends('qty_water_supply', 'unit_price_water_supply')
    def _compute_amount_water_supply(self):
        for line in self:
            line.amount_water_supply = (line.qty_water_supply or 0.00) * (
                    line.unit_price_water_supply or 0.00)
