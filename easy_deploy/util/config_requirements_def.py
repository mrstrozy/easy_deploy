'''
This file specifies all requirements for each easy_deploy config command
'''

COMMANDS = {
    'installDebianPackage': {
        'mandatory': ['source'],
    },
    'installFile': {
        'mandatory': ['localSource', 'remoteSource'],
        'optional': {
            'group': 'root',
            'mode': '0644',
            'owner': 'root',
        }
    },
    'removeDebianPackage': {
        'mandatory': ['source'],
    },
}

UNIVERSAL_OPTIONS = ['command', 'restarts']
