'''
Module is used to run set defined commands for easy_deploy
'''


import logging
import os
import shutil
import sys

from time import time

from easy_deploy.util.connection import Connection
from easy_deploy.util.constants import DEFAULT_BUILD_DIR


class Runner:
    def __init__(self,
                 hostname: str,
                 identity: str,
                 username: str,
                 ):
        '''
        Args:
          hostname::str
            Name of host to interact with.
          identity::str
            Path of identity file for authenticating with host
          username::str
            Username to authenticate as
        '''
        self.connection = Connection(hostname=hostname,
                                     identityFile=identity,
                                     username=username,
                                     )
        self.logger = logging.getLogger()
        self.build_dir_path = '%s/%s' % (DEFAULT_BUILD_DIR,
                                         str(time()).split('.')[0])
        self._create_build_dir()

    def __del__(self,
                ):
        self._delete_build_dir()

    def _create_build_dir(self,
                          ):
        '''
        Creates the temporary build dir for building files
        '''
        try:
            os.makedirs(self.build_dir_path)
        except OSError:
            err = 'Unable to make build dir. Exiting.'
            self.logger.error(err)
            sys.exit(-1)            

    def _delete_build_dir(self,
                          ):
        '''
        Deletes the build directory
        '''
        shutil.rmtree(self.build_dir_path)

    def installFile(self,
                    config: dict,
                    ) -> bool:
        '''
        Install a file onto the instances remote host.

        Args:
          config::dict
            Dictionary containing the following keys:
              - localSource
              - remoteSource
              - group
              - mode
              - owner

        Returns::bool
          True if successfully installed file, False if not
        '''
        pass 

