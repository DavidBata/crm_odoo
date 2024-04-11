from datetime import datetime
from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class CrmLeadIherit(models.Model):
    _inherit = 'crm.lead'

    
    commission = fields.Float(
        string='Compicion',
    )
    
    

   
    accounts_payable_crm_ids = fields.One2many(
        string='Cuentas por pagar',
        comodel_name='accounts.payable.crm',
        inverse_name='oprtunity_id',
    )
    

