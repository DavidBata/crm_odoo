from datetime import datetime
from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountsPaymenteRegisterCrm(models.Model):
    _name = 'account.payment.register.commission'

    accounts_payable_crm_id = fields.Many2one(
        string='Cuenta por Pagar',
        comodel_name='accounts.payable.crm',
        ondelete='restrict',
    )

    
    catidad = fields.Float(
        string='Catidad a Pagar',
    )
    
    amount = fields.Float(
        string='Importe',
    )
    
    payment_date = fields.Date(
        string='Fecha de Pago',
        default=fields.Date.context_today,
    )
    
    
    communication = fields.Char(
        string='Memo',
        # compute de name de oportunity
    )
    
    payment_method_line_id = fields.Many2one(
        string='Metodo de Pago',
        comodel_name='account.payment.method.line',
        ondelete='restrict',
    )

    @api.onchange('accounts_payable_crm_id')
    def _onchange_importe_total(self):
        if self.accounts_payable_crm_id:
            object = self.env['account.payment.register.commission'].search([('accounts_payable_crm_id','=', self.accounts_payable_crm_id.id)])
            total_importe = sum(map(lambda p: p.amount, object))

            self.amount = (self.accounts_payable_crm_id.commission - total_importe) if total_importe else self.accounts_payable_crm_id.commission
