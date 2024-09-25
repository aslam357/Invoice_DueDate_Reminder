from odoo import models, fields, api
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_reminder_template_id = fields.Many2one(
        'mail.template', 
        string="Email Template", 
        domain="[('model', '=', 'account.move')]",  
        config_parameter='due_date_reminder.template_id'
    )

    invoice_reminder_days = fields.Integer(
        string="Set No.of Days", 
        config_parameter='due_date_reminder.days', 
        default=7
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update({
            'invoice_reminder_template_id': self.env['ir.config_parameter'].sudo().get_param('due_date_reminder.template_id'),
            'invoice_reminder_days': self.env['ir.config_parameter'].sudo().get_param('due_date_reminder.days', default=7),
        })
        return res

    @api.model
    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param('due_date_reminder.template_id', self.invoice_reminder_template_id.id)
        self.env['ir.config_parameter'].sudo().set_param('due_date_reminder.days', self.invoice_reminder_days)

