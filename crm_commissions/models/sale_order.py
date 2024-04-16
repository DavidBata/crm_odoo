from datetime import datetime
from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    def create_payment_sale(self):
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