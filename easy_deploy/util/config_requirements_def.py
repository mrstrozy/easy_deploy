'''
This file specifies all requirements for each easy_deploy config command
'''

COMMANDS = {
    'installFile': {
        'mandatory': ['localSource', 'remoteSource'],
        'optional': {
            'group': 'root',
            'mode': '0644',
            'owner': 'root',
        }
    },
}

UNIVERSAL_OPTIONS = ['restarts']
