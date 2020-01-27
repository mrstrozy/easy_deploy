'''
Module is used to run set defined commands for easy_deploy
'''


import grp
import logging
import os
import pwd
import shutil
import sys

from time import time

from easy_deploy.util.connection import Connection
from easy_deploy.util.constants import (DEFAULT_BUILD_DIR,
                                       DEFAULT_FILE_DIRNAME)


class Runner:
    def __init__(self,
                 baseDir: str,
                 hostname: str,
                 identity: str,
                 username: str,
                 ):
        '''
        Args:
          baseDir::str
            Base directory where files live
          hostname::str
            Name of host to interact with.
          identity::str
            Path of identity file for authenticating with host
          username::str
            Username to authenticate as
        '''
        self.baseDir = baseDir
        self.fileDir = '%s/%s' % (baseDir, DEFAULT_FILE_DIRNAME)
        self.identity = identity
        self.hostname = hostname
        self.username = username
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

    def installDeb(self,
                   config: dict,
                   ) -> bool:
        pass

    def removeDeb(self,
                  config: dict,
                  ) -> bool:
        pass

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
        def get_uid(user: str) -> int:
            '''
            Returns UID (if found) for the associated user.
            '''
            uid = 0
            try:
                uid = pwd.getpwnam(user).pw_uid
            except KeyError:
                err = 'Error with %s: User "%s" not found' % (config, user)
                self.logger.error(err)
                sys.exit(-1)
            return uid

        def get_gid(group: str) -> int:
            '''
            Returns GUID (if found) for the associated user.
            '''
            gid = 0
            try:
                gid = grp.getgrnam(group).gr_gid
            except KeyError:
                err = 'Error with %s: Group "%s" not found' % (config, group)
                self.logger.error(err)
                sys.exit(-1)
            return gid

        ownerName = config.get('owner', '')
        groupName = config.get('group', '')
        mode = config.get('mode', '0644')
        fileLocalname = config.get('localSource')
        fileRemotePath = config.get('remoteSource')
        fileLocalPath = '%s/%s' % (self.fileDir, fileLocalname)

        ownerUid = get_uid(ownerName)
        groupUid = get_gid(groupName)
        modeOct = mode[0] + 'o' + mode[1:]
        filename = fileRemotePath.split('/')[-1]

        # Build remote directory
        fileRemoteDirList = fileRemotePath.split('/')
        fileRemoteDir = '/'.join(fileRemoteDirList[:len(fileRemoteDirList)-1])
        
        baseFileLoc = '%s/%s' % (self.build_dir_path, filename)

        # Copy file to build dir
        shutil.copyfile(fileLocalPath, baseFileLoc)

        # Change permissions, owner, group
        os.chown(baseFileLoc, ownerUid, groupUid)
        os.chmod(baseFileLoc, int(modeOct, 8))

        # Copy to remote host
        success = self.connection.copy_file_to_remote_host(baseFileLoc,
                                                           fileRemoteDir)

        if not success:
            err = 'Unable to install file: %s' % filename
            self.logger.error(err)
            return False
            
        msg = 'Successfully installed file: %s' % filename
        self.logger.info(msg)

        return True

    def restart_service(self,
                        service: str,
                        ) -> bool:
        '''
        Restart a service on the remote host.
        '''
        cmd = 'ssh -i %s %s@%s "service %s restart"' % (self.identity,
                                                        self.username,
                                                        self.hostname,
                                                        service)
        returncode = os.system(cmd)
        return returncode == 0
