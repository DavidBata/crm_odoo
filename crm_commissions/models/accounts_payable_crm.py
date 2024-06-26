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
        related='oprtunity_id.commission'
    )
    
    company_currency = fields.Many2one("res.currency", string='Currency',compute_sudo=True, compute="_compute_company_currency" )
    
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
    
    user_id = fields.Many2one(
        string='Usuario',
        comodel_name='res.users',
        ondelete='restrict',
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
        # object = self.env['account.payment.register.commission'].search([('accounts_payable_crm_id','=', self.id)])
        if self.total_amount >= self.commission:

            raise ValidationError("No puedes relaizar mas pagos a esta comisión")


        return {
            'name': _('Registar Pago Comicion'),
            'res_model': 'account.payment.register.commission',
            'view_mode': 'form',
            'context': {
                'default_accounts_payable_crm_id': self.id
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    
    def _compute_total_amount(self):

        for rec in self:
            object = self.env['account.payment.register.commission'].search([('accounts_payable_crm_id','=', rec.id)])
            total_importe = sum(map(lambda p: p.amount, object))
            rec.sudo().write({
                    'total_amount':total_importe if total_importe else 0.0
                })
            if rec.total_amount == rec.commission:
                rec.sudo().write({
                    'state': 'payment'
                })
            else:
                rec.sudo().write({
                    'state': 'no_payment'
                })
    
    def _compute_currency_id(self):
        for rec in self:
            rec.sudo().write({
            'currency_id': self.env.company.currency_id.id 
            }) 
                


    @api.depends('company_id')
    def _compute_company_currency(self):
        for rec in self:
            if not rec.company_id:
                rec.company_currency = rec.env.company.currency_id
            else:
                rec.company_currency = rec.company_id.currency_id