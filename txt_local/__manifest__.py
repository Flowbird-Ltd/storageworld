# -*- coding: utf-8 -*-
{
    'name': "Txt Local Integration",
    'summary': """
        The ability to send and receive messages from Odoo using txt local as a provider
    """,
    'description': """
        The ability to send and receive messages from Odoo using txt local as a provider
    """,
    'author': "Jack Dane",
    'website': "https://www.flowbird.co.uk",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'contacts', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/txt_local_messages.xml',
        'views/txt_local_groups.xml',
        'views/txt_local_group_tags.xml',
        'views/contact.xml',
        'views/res_config_settings.xml',
        'views/menu_items.xml',
        'views/crm.xml',
        'data/txt_local_message_sequence.xml',
    ],
    "application": True
}
