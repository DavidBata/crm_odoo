from datetime import datetime
from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountsPayableCrm(models.Model):
    _name = 'accounts.payable.crm'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    
    oprtunity_id = fields.Many2one(
        string='Oportunidad',
        comodel_name='crm.lead',
        ondelete='restrict',
    )
    contact_name = fields.Char(
        string='Nombre del Contacto',
        related='oprtunity_id.contact_name'
    )
    commission = fields.Float(
        string="Comicion",
        compute = '_compute_commission'
        # related='oprtunity_id.commission',
    )

    
    
    company_id = fields.Many2one(
        string='Company', 
        comodel_name='res.company', 
        default=lambda self: self.env.user.company_id
    )
    
    state = fields.Selection(
        string='state',
        selection=[('no_payment', 'No Pagado'), ('payment', 'Pagado')],
        default="no_payment"
    )

    total_amount = fields.Float(
        string='Total Pagado',
        compute = '_compute_total_amount'
    )
    
    account_payment_commission_ids = fields.One2many('account.payment.register.commission', 'accounts_payable_crm_id', string='Pagos de comicion')
    
    # order_ids = fields.One2many(
    #     related='oprtunity_id.order_ids'
    # )
    def action_register_payment_crm(self):
        ''' Open the account.payment.register wizard to pay the selected journal entries.
        :return: An action opening the account.payment.register wizard.
        '''
        return {
            'name': _('Registar Pago Comicion'),
            'res_model': 'account.payment.register.commission',
            'view_mode': 'form',
            'context': {
                'active_model': 'accounts.payable.crm',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    def _compute_commission(self):
        for rec in self:
            rec.commission= float(rec.oprtunity_id.commission)
    
    
    def _compute_total_amount(self):
        object = self.env['account.payment.register.commission'].search([('accounts_payable_crm_id','=', self.id)])
        total_importe = sum(map(lambda p: p.amount, object))
        self.total_amount = total_importe if total_importe else 0.0

    