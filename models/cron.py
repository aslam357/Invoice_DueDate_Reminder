from odoo import models, fields, api

class IrCron(models.Model):
    _inherit = 'ir.cron'

    @api.model
    def create_invoice_reminder_cron(self):
        self.create({
            'name': 'Send Invoice Due Date Reminder',
            'model_id': self.env.ref('account.model_account_move').id,
            'state': 'code',
            'code': 'model.send_invoice_reminder()',
            'active': True,
            'interval_number': 1,
            'interval_type': 'days',
            'nextcall': fields.Datetime.now(),
            'numbercall': -1,
        })