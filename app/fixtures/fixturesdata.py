from app.settings import settings as s


crud =  ['create', 'read', 'update', 'delete']

# Default account
AccountGroup = {
    'profile': ['read', 'update'],
    'account': ['read', 'update'],
    'message': crud,
}
ContentGroup = {
    'content': crud
}

# For attachment
StaffGroup = {
    'user': ['create', 'read', 'update', 'ban', 'unban'],
    'group': crud + ['attach', 'detach'],
    'permission': crud + ['attach', 'detach'],
    'taxonomy': crud,
}
AdminGroup = {
    **ContentGroup,
    **AccountGroup,
    **StaffGroup,
    
    'staff': crud,
    'admin': [*crud, 'settings'],
}
NoaddGroup = {
    'foo': ['read', 'update', 'delete', 'hard_delete'],
    'user': ['create', 'delete', 'hard_delete'],
}

options_dict = {
    'site': {
        'sitename': s.SITE_NAME,
        'siteurl': s.SITE_URL,
        'author': 'DropkickDev',
        'last_update': '',
    },
    'admin': {
        'access_token': s.ACCESS_TOKEN_EXPIRE,
        'refresh_token': s.REFRESH_TOKEN_EXPIRE,
        'refresh_token_cutoff': s.REFRESH_TOKEN_CUTOFF,
        'verify_email': s.VERIFY_EMAIL
    },
    
    # Diff per user
    'account': {
        'theme': 'Light',
        'email_notifications': True,
        'language': 'en',
        
        'takeprofit': 0.12,
        'stoploss': 0.08,
        'rrr': 2.5,
        'max_PHP': 100_000,
        'max_USD': 2_000,
        'rate_USD': 50.0,
        
        # # Alerts
        # 'takeprofit': True,
        # 'stoploss': True,
    },
}


taxonomy_dict = {
    'exchange': [
        dict(description='Stock exchanges'),
        
        dict(name='PSE', label='Philippine Stock Exchange', is_locked=True),
        dict(name='SGX', label='Singapore Exchange', is_locked=True),
        dict(name='NYSE', label='New York Stock Exchange', is_locked=True),
        dict(name='NYSEP', label='NYSE Preferred Shares', is_locked=True),
        dict(name='NASDAQ', label='Nasdaq Stock Market', is_locked=True),
        dict(name='ARCA', label='ARCA & MKT', is_locked=True),
        dict(name='OTC', label='OTC Markets', is_locked=True),
        dict(name='FX', label='Forex', is_locked=True),
        dict(name='CRYPTO', label='Cryptocurrency', is_locked=True),
    ],
    'groups': [
        dict(label='Equity groups'),
        
        dict(name='Watchlist', is_locked=True),
        dict(name='Undecided', is_locked=True),
    ],
    'stages': {
        'buy_stage': [
            dict(label='Buying', is_locked=True, description='The buying process'),
            
            dict(name='Shortlist', is_locked=True, sort=1,
                 description='Potential stock to BUY'),
            dict(name='Getting close', description='Stock is approaching your entry point',
                 is_locked=True, sort=2),
            dict(name='Ready to BUY', description='Stock is just above your entry point',
                 is_locked=True, sort=3),
            dict(name='BUY now', is_locked=True, sort=4,
                 description='Waiting for the right moment to BUY'),
        ],
        'sell_stage': [
            dict(label='Selling', is_locked=True, description='The selling process'),
            
            dict(name='Shortlist', is_locked=True, sort=1,
                 description='Potential stock to SELL'),
            dict(name='Getting close', description='Stock is approaching your entry point',
                 is_locked=True, sort=2),
            dict(name='Ready to SELL', description='Stock is just above your entry point',
                 is_locked=True, sort=3),
            dict(name='SELL now', is_locked=True, sort=4,
                 description='Waiting for the right moment to SELL'),
        ],
    },
    'trade_tags': [
        dict(description='Tags for trading use'),
        
        dict(name='trash', is_locked=True),
        dict(name='recommended', is_locked=True),
        dict(name='not-now', is_locked=True),
        dict(name='invest-soon', is_locked=True),
    ],
    'brokers': [
        dict(description='Brokers list')
    ],
}