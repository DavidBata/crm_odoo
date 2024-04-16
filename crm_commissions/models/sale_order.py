from datetime import datetime
from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'sale', 'done', 'cancel','payment'}
}
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'sale', 'done', 'cancel','payment'}
    }

    state = fields.Selection(
        selection=[
            ('draft', "Quotation"),
            ('sent', "Quotation Sent"),
            ('sale', "Sales Order"),
            ('done', "Locked"),
            ('cancel', "Cancelled"),
            ('payment', "Pagado"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
     
    
    payment_sale_ids = fields.One2many('account.payment.register.commission', 'sale_order_id', string='payment_sale')
    total_payments = fields.Float(
        string='Total Pagados' ,compute="_compute_total_payments"   )
    
    def _compute_total_payments (self):
        for rec in self: 
            objeto_payments = self.env['account.payment.register.commission'].search([('sale_order_id', '=', rec.id)])
            total_pagado  = sum(map(lambda p: p.amount, objeto_payments))

            rec.sudo().write({
                    'total_payments':total_pagado if total_pagado else 0.0
                })
            if total_pagado >= rec.amount_total:
                rec.sudo().write({'state':'payment'})

    def create_payment_sale(self):
        objeto_payments = self.env['account.payment.register.commission'].search([('sale_order_id', '=', self.id)])
        total_pagado  = sum(map(lambda p: p.amount, objeto_payments))
        if total_pagado >= self.amount_total:
            self.state= 'payment'
        else:
            return {
                'name': _('Registar Pago de Venta'),
                'res_model': 'account.payment.register.commission',
                'view_mode': 'form',
                'context': {
                    'default_sale_order_id': self.id,
                    'default_catidad': self.amount_total,
                    'default_communication': self.display_name,
                    'default_is_payment_sale':True
                },
                'target': 'new',
                'type': 'ir.actions.act_window',
            }