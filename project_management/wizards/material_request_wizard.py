from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class MaterialRequestWizard(models.TransientModel):
    """Material Request Wizard"""
    _name = "material.request.wizard"
    _description = "Material Request Wizard"

    # partner_id = fields.Many2one('res.partner', string="Supplier")
    project_id = fields.Many2one('project.project', string="Project", readonly=1)
    material_ids = fields.One2many(
        comodel_name="material.wizard.lines",
        inverse_name="wizard_id",
        string="Materials",
    )
    task_id = fields.Many2one('project.task', string="Task")

    # def action_create_purchase_order(self):
    #     """
    #     Create purchase orders for selected suppliers and items.
    #     """
    #     if not self.partner_id:
    #         raise UserError(_("Please select a supplier to create the RFQ."))
    #     if not self.item_ids:
    #         raise UserError(_("Please add at least one item to create the RFQ."))
    #     purchase = self.env["purchase.order"].create({
    #         "origin": self.project_id.name,
    #         "partner_id": self.partner_id.id,
    #         "payment_term_id": self.partner_id.property_supplier_payment_term_id.id,
    #         "fiscal_position_id": self.partner_id.property_account_position_id.id if self.partner_id.property_account_position_id else False,
    #         "company_id": self.project_id.company_id.id,
    #         "project_id": self.project_id.id,
    #         "currency_id": self.project_id.currency_id.id,
    #         "state": "draft",
    #     })
    #     for item in self.item_ids:
    #         self.env["purchase.order.line"].create({
    #             "product_id": item.product_id.id,
    #             "name": item.product_id.display_name,
    #             "product_qty": item.quantity,
    #             "product_uom": item.uom_id.id,
    #             "company_id": self.project_id.company_id.id,
    #             "order_id": purchase.id,
    #         })
    #     return {
    #         "domain": [("id", "in", purchase.ids)],
    #         "name": _("RFQ"),
    #         "view_mode": "list,form",
    #         "res_model": "purchase.order",
    #         "view_id": False,
    #         "context": self.env.context,
    #         "type": "ir.actions.act_window",
    #     }
    #
    # def _prepare_purchase_order_line(self, item):
    #     """
    #     Prepare purchase order line data.
    #     """
    #     return {
    #         "product_id": item.product_id.id,
    #         "name": item.product_id.display_name,
    #         "product_qty": item.quantity,
    #         "product_uom": item.uom_id.id,
    #         "company_id": self.project_id.company_id.id,
    #     }
    #
    # def _prepare_purchase_order(self, company, origin, supplier_id):
    #     """
    #     Prepare purchase order header data.
    #     """
    #     if not supplier_id:
    #         raise UserError(_("Enter a supplier."))
    #
    #     data = {
    #         "origin": origin,
    #         "partner_id": supplier_id.id,
    #         "payment_term_id": supplier_id.property_supplier_payment_term_id.id,
    #         "fiscal_position_id": supplier_id.property_account_position_id.id if supplier_id.property_account_position_id else False,
    #         "company_id": company.id,
    #         "project_id": self.project_id.id,
    #         "currency_id": self.project_id.currency_id.id,
    #         "state": "draft",
    #     }
    #     return data

    def action_create_mr(self):
        print('action_create_mr')

    def action_create_delivery_not(self):
        if not self.material_ids:
            raise UserError(_("Please select material lines."))
        warehouse_id = self.project_id.sale_line_id.order_id.warehouse_id
        picking = self.env['stock.picking'].sudo().create({
            'partner_id': self.project_id.partner_id.id,
            'picking_type_id': warehouse_id.out_type_id.id,
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'origin': f"{self.project_id.name} - {self.task_id.name}"
        })
        from_loc = warehouse_id.out_type_id.default_location_src_id
        dest_loc_id = warehouse_id.out_type_id.default_location_dest_id
        for line in self.material_ids:
            move = self.env['stock.move'].sudo().create({
                'product_id': line.product_id.id,
                'name': line.product_id.display_name,
                'product_uom_qty': line.quantity,
                'product_uom': line.uom_id.id,
                'picking_id': picking.id,
                'location_id': from_loc.id,
                'location_dest_id': dest_loc_id.id,
            })
            line.line_id.move_ids = [(4, move.id)]
