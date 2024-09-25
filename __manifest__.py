{
    'name': 'Invoice Due Date Reminder',

    'summary': " The Invoice Due Date Reminder module is designed for Odoo to automatically send email reminders to customers regarding upcoming invoice due dates",
    'author': "Amzsys",
    'website': "https://www.amzsys.com",

    'version': '1.0',
    'category': 'Accounting',
    'author': 'Aslam',
    'depends': ['account', 'mail', 'base_setup'], 
    'data': [
        'views/settings_view.xml',
    'views/email_template.xml',
    ],
    'installable': True,
    'application': True,
}
