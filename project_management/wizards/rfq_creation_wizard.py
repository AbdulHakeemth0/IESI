from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class RfqCreationWizard(models.TransientModel):
    """Rfq Creation Wizard"""
    _name = "rfq.creation.wizard"
    _description = "Purchase RFQ Creation Wizard"

    supplier_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Suppliers",
        context={"res_partner_search_mode": "supplier"},
    )
    partner_id = fields.Many2one('res.partner', string="Supplier")
    project_id = fields.Many2one('project.project', string="Project", readonly=1)
    item_ids = fields.One2many(
        comodel_name="rfq.creation.wizard.lines",
        inverse_name="rfq_wizard_id",
        string="Items",
    )
    picking_type_id = fields.Many2one('stock.picking.type', string="Delivery Location", domain="[('code', 'in', ('incoming', 'dropship')), ('company_id', '=', company_id)]")
    company_id = fields.Many2one('res.company', string="Company")
    po_bool = fields.Boolean(string="PO Bool", default=False)
    dn_bool = fields.Boolean(string="DN Bool", default=False)


    def action_create_delivery_order(self):
        print()
        self.ensure_one()  # Make sure this is a single record
        if not self.item_ids:
            raise UserError(_("Please select material lines."))
        warehouse_id = self.project_id.sale_line_id.order_id.warehouse_id
        picking = self.env['stock.picking'].sudo().create({
            'partner_id': self.project_id.partner_id.id,
            'picking_type_id': warehouse_id.out_type_id.id,
            'project_id': self.project_id.id,
            'origin': f"{self.project_id.name} - {self.mr_id.task_id.name}"
        })
        picking.mr_id = self.mr_id.id
        from_loc = warehouse_id.out_type_id.default_location_src_id
        dest_loc_id = warehouse_id.out_type_id.default_location_dest_id
        for line in self.item_ids:
            move = self.env['stock.move'].sudo().create({
                'product_id': line.product_id.id,
                'name': line.product_id.display_name,
                'product_uom_qty': line.quantity,
                'product_uom': line.uom_id.id,
                'picking_id': picking.id,
                'location_id': from_loc.id,
                'location_dest_id': dest_loc_id.id,
            })
            line.mr_line_id.status = 'dn'
            line.mr_line_id.done_quantity = line.quantity
        return {
            "domain": [("id", "in", picking.ids)],
            "name": _("Delivery Orders"),
            "view_mode": "list,form",
            "res_model": "stock.picking",
            "view_id": False,
            "context": self.env.context,
            "type": "ir.actions.act_window",
        }



    def action_create_purchase_order(self):
        """Create purchase orders for selected suppliers and items."""
        if not self.partner_id:
            raise UserError(_("Please select a supplier to create the RFQ."))
        if not self.item_ids:
            raise UserError(_("Please add at least one item to create the RFQ."))
        if not self.picking_type_id:
            raise UserError(_("Please select Receipt(To Stock) or Dropship(To Customer) to create the RFQ."))
        if self.picking_type_id.code == 'dropship':
            if not self.project_id.partner_id:
                raise ValidationError(_("Please add customer in project to create the RFQ."))
            purchase = self.env["purchase.order"].sudo().create({
                "origin": self.project_id.name,
                "partner_id": self.partner_id.id,
                "payment_term_id": self.partner_id.property_supplier_payment_term_id.id,
                "fiscal_position_id": self.partner_id.property_account_position_id.id if self.partner_id.property_account_position_id else False,
                "company_id": self.project_id.company_id.id,
                "project_id": self.project_id.id,
                "currency_id": self.project_id.currency_id.id,
                "state": "draft",
                "picking_type_id": self.picking_type_id.id,
                "dest_address_id": self.project_id.partner_id.id,
            })
        else:
            purchase = self.env["purchase.order"].sudo().create({
                "origin": self.project_id.name,
                "partner_id": self.partner_id.id,
                "payment_term_id": self.partner_id.property_supplier_payment_term_id.id,
                "fiscal_position_id": self.partner_id.property_account_position_id.id if self.partner_id.property_account_position_id else False,
                "company_id": self.project_id.company_id.id,
                "project_id": self.project_id.id,
                "currency_id": self.project_id.currency_id.id,
                "state": "draft",
            })
        purchase.mr_id = self.mr_id.id
        for item in self.item_ids:
            self.env["purchase.order.line"].sudo().create({
                "product_id": item.product_id.id,
                "name": item.product_id.display_name,
                "product_qty": item.quantity,
                "product_uom": item.uom_id.id,
                "company_id": self.project_id.company_id.id,
                "order_id": purchase.id,
            })
            item.mr_line_id.status = 'po'
            item.mr_line_id.done_quantity = item.quantity
        return {
            "domain": [("id", "in", purchase.ids)],
            "name": _("RFQ"),
            "view_mode": "list,form",
            "res_model": "purchase.order",
            "view_id": False,
            "context": self.env.context,
            "type": "ir.actions.act_window",
        }

    def _prepare_purchase_order_line(self, item):
        """Prepare purchase order line data."""
        return {
            "product_id": item.product_id.id,
            "name": item.product_id.display_name,
            "product_qty": item.quantity,
            "product_uom": item.uom_id.id,
            "company_id": self.project_id.company_id.id,
        }

    def _prepare_purchase_order(self, company, origin, supplier_id):
        """Prepare purchase order header data."""
        if not supplier_id:
            raise UserError(_("Enter a supplier."))
        data = {
            "origin": origin,
            "partner_id": supplier_id.id,
            "payment_term_id": supplier_id.property_supplier_payment_term_id.id,
            "fiscal_position_id": supplier_id.property_account_position_id.id if supplier_id.property_account_position_id else False,
            "company_id": company.id,
            "project_id": self.project_id.id,
            "currency_id": self.project_id.currency_id.id,
            "state": "draft",
        }
        return data
class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    def _compute_display_name(self):
        super()._compute_display_name()
        if self.env.context.get('active_model') == 'project.material.request':
            for rec in self:
                if rec.code == 'dropship':
                    rec.display_name = 'Store'
                elif rec.code == 'incoming':
                    rec.display_name = 'Site'
