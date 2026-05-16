{
    "name": "Analytic Account Customisations",
    "summary": """Customizations to the account module.""",
    "description": """ 
       Analytic account customisations
    """,
    'author': 'Abdul Hakeem TH',
    "website": 'https://hornbill-bs.com',
    "support": 'https://hornbill-bs.com',
    "license": "OPL-1",
    "category": "Account",
    "version": "18.0.2.3.0",
    "depends": ['account', "accountant","base","sale","purchase","sale_management","project","website"],
    "data": [
        "data/server_action.xml",
        "data/ir_sequence.xml",
        # "data/scheduled_action.xml",
        "views/analytic_account.xml",
        "views/account_move.xml",
        "views/account_journal.xml",
        "views/sale_order.xml",
        # "views/purchase_order.xml"

    ],
}
