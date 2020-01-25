'''
Entrypoint for running the deployment. This contains instructions
for successfully running through a deployment (run_deployment function).
'''

import logging

def run_deployment(baseDir: str,
                   identityFile: str,
                   instructionFile: str,
                   remoteHost: str,
                   ):
    '''
    Run a deployment job.

    Args:
      baseDir::str
        Directory containing needed files (files to use in config)

      identityFile::str
        Filepath to use when authenticating with the remote host

      instructionFile::str
        Filepath to file specifying deployment steps

      remoteHost::str
        Identifier to use to connect to remote host
    '''
    logger = logging.getLogger()
    logger.info('Starting deployment')

    # TODO Confirm structure of instructionFile
    #      - This requires a yaml parser & enforcing requirements
    #      
    #      Load Instructions (once file is verified)
    #
    #      Test connection to host w/identityFile
    #      - Can we ssh?
    #
    #      Loop through and run instructions
    #
    #
