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
    
    def action_set_won_rainbowman(self):
        self.register_account_payable()
        self.ensure_one()
        self.action_set_won()
        message = self._get_rainbowman_message()
        if message:
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': message,
                    'img_url': '/web/image/%s/%s/image_1024' % (self.team_id.user_id._name, self.team_id.user_id.id) if self.team_id.user_id.image_1024 else '/web/static/img/smile.svg',
                    'type': 'rainbow_man',
                }
            }
        return True


    def register_account_payable(self):
        x = self.env['accounts.payable.crm'].sudo().create({'oprtunity_id' : self.id,
                                                        'contact_name' : self.name})
        