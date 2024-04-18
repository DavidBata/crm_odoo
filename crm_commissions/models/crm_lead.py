from datetime import datetime
from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CrmLeadIherit(models.Model):
    _inherit = 'crm.lead'

    commission = fields.Float('Comisión', tracking=True)


    accounts_payable_crm_ids = fields.One2many(
        string='Cuentas por pagar',
        comodel_name='accounts.payable.crm',
        inverse_name='oprtunity_id',
    )
    
    company_id = fields.Many2one(
        string='Company', 
        comodel_name='res.company', 
        required=True, 
        default=lambda self: self.env.user.company_id
    )
    
    
    state = fields.Selection(
        string='state',
        selection=[('borrador', 'Borrador'), ('confirmado', 'confirmado')],
        default='borrador',
    )
    
    


    def confirmar_aoportunity (self):
        for rec in self:
            if rec.commission > 0 and  rec.commission < rec.expected_revenue:
                self.register_account_payable()


    def register_account_payable(self):
        x = self.env['accounts.payable.crm'].sudo().create({'oprtunity_id' : self.id,
                                                            'contact_name' : self.name,
                                                            'user_id' : self.user_id.id})
        