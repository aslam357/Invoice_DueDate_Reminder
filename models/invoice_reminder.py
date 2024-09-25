from odoo import models, fields
from odoo.exceptions import UserError

class InvoiceReminder(models.Model):
    _inherit = 'account.move'


class InvoiceReminder(models.Model):
    _inherit = 'account.move'

    def send_invoice_reminder(self):
        today = fields.Date.context_today(self)
        reminder_days = self._get_reminder_days()
        reminder_date = fields.Date.add(today, days=reminder_days)

        invoices = self._get_due_invoices(today, reminder_date)

        if invoices:
            template = self._get_reminder_template()
            email_dict = {}

            for invoice in invoices:
                email = invoice.partner_id.email
                if email:
                    if email not in email_dict:
                        email_dict[email] = []
                    email_dict[email].append(invoice)

            for email, invoice_list in email_dict.items():
                self._send_bulk_reminder(email, template, invoice_list)

    def _get_reminder_days(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('due_date_reminder.days', default=7))

    def _get_due_invoices(self, today, reminder_date):
        return self.search([
            ('state', '=', 'posted'),
            ('invoice_date_due', '>=', today),
            ('invoice_date_due', '<=', reminder_date),
            ('payment_state', 'not in', ['paid', 'in_payment']),
            ('invoice_payment_term_id', '!=', False)
        ])

    def _get_reminder_template(self):
        template_id = self.env['ir.config_parameter'].sudo().get_param('due_date_reminder.template_id')
        template = self.env.ref('due_date_reminder.email_template_invoice_reminder', raise_if_not_found=False)
        if not template:
            raise UserError("The email template for the invoice reminder is missing.")
        return template

    def _send_bulk_reminder(self, email, template, invoices):
        try:
            for invoice in invoices:
                template.send_mail(invoice.id, force_send=True)
        except Exception as e:
            raise UserError(f"Failed to send reminders for invoices to {email}. Error: {str(e)}")