'''
Entrypoint for running the deployment. This contains instructions
for successfully running through a deployment (run_deployment function).
'''

import logging
import sys

from easy_deploy.util.cmd_runner import Runner
from easy_deploy.util.connection import Connection
from easy_deploy.util.constants import DEFAULT_FILE_DIRNAME
from easy_deploy.util.parser import EasyDeployParser
from easy_deploy.util.verify import Verifier


class Deployment:
    def __init__(self,
                 baseDir: str,
                 identityFile: str,
                 instructionFile: str,
                 remoteHost: str,
                 username: str,
                 ):
        '''
        Args:
          baseDir::str
            Directory containing needed files (files to use in config)
          identityFile::str
            Filepath to use when authenticating with the remote host
          instructionFile::str
            Filepath to file specifying deployment steps
          remoteHost::str
            Identifier to use to connect to remote host
          username::str
            Username to authorize with remoteHost as
        '''
        self.logger = logging.getLogger()
        self.baseDir = baseDir
        self.instructionFile = instructionFile
        self.remoteHost = remoteHost
        self.parser = EasyDeployParser()
        self.connection = Connection(hostname=remoteHost,
                                     identityFile=identityFile,
                                     username=username,
                                     )
        self.runner = Runner(baseDir=baseDir,
                             hostname=remoteHost,
                             identity=identityFile,
                             username=username,
                             )
        self.verifier = Verifier(baseDir)

    def run(self,
            ) -> bool:
        '''
        Run a deployment job.

        Returns::bool
          True/False based on success of run.
        '''
        runlist = self._build_runlist()
        missing_files = self.verifier.verify_files(runlist)

        if missing_files:
            for filename in missing_files:
                err = 'File missing: %s/%s/%s' % (self.baseDir,
                                                  DEFAULT_FILE_DIRNAME,
                                                  filename)
                self.logger.error(err)
            return

   
        if not self.connection.verify_connection():
            err = 'Unable to establish connection with '\
                  '%s. Exiting..' % (self.remoteHost)
            self.logger.error(err)
            return
        else:
            msg = 'Successfully connected to %s' % self.remoteHost
            self.logger.info(msg)

        # TODO
        #      Loop through and run instructions
        #
        for instruction in runlist:
            # Run through command body first
            command = instruction.get('command')
            if command == 'installFile':
                success = self.runner.installFile(instruction)
            elif command == 'installDebianPackage':
                success = self.runner.debianPackage(instruction, 'install')
            elif command == 'removeDebianPackage':
                success = self.runner.debianPackage(instruction, 'remove')
            else:
                err = 'Unrecognized command: %s' % command
                self.logger.error(err)
                success = False
            
            if not success:
                return False


            # Run service restart after configuration if specified
            if 'restarts' in instruction:
                service = instruction.get('restarts')
                success = self.runner.restart_service(service)
                if not success:
                    err = 'Unable to restart service "%s"' % service
                    self.logger.error(err)
                    return False
        # If all instructions are executed and we are here, it is a success
        return True

        
    def _build_runlist(self,
                       ) -> list:
        '''
        Build the runlist for the job.

        Program exits on failed build.

        Returns::list
          Build runlist for the job
        '''
        self.logger.debug('Parsing config')
        runlist, errors = self.parser.build(self.instructionFile)
    
        if errors:
            errMsg = '\n' + '\n\n'.join(errors)
            self.logger.error(errMsg)
            sys.exit(-1)

        self.logger.debug('Config verified. Runlist built.')
        return runlist
