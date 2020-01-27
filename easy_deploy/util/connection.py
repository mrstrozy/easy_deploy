'''
Module for handling all connections with remote hosts.
'''

import logging
import subprocess

from functools import wraps


def singleton(classkey: str):
    '''
    Singleton Decorator
    '''
    def _singleton(cls):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            if classkey not in wrapper.instances:
                wrapper.instances[classkey] = cls(*args, **kwargs)
            return wrapper.instances.get(classkey)
        wrapper.instances = {}
        return wrapper
    return _singleton

@singleton('Connection')
class Connection:
    def __init__(self,
                 hostname: str,
                 identityFile: str,
                 username: str,
                 ):
        '''
        Args:
          hostname::str
            Host identifier for connection
          identityFile::str
            Path of identity file to use for authentication with host
          username::str
            Username to login as
        '''
        self.hostname = hostname
        self.identity = identityFile
        self.username = username
        self.logger = logging.getLogger()

    def copy_file_to_remote_host(self,
                                 localSource: str,
                                 remoteSource: str,
                                 ) -> bool:
        '''
        Copy a local file to a remote location

        Args:
          localSource::str
            Filepath of the local file to copy
          remoteSource::str
            Filepath to copy file to

        Returns::bool
          True/False of copy success
        '''
        cmd = 'rsync -p -e "ssh -i %s" %s %s@%s:%s/' % (self.identity,
                                                        localSource,
                                                        self.username,
                                                        self.hostname,
                                                        remoteSource)
        _, returncode = self.run_cmd(cmd,
                                    shell=True,
                                    timeout=10)
        return returncode == 0

    def verify_connection(self,
                          ) -> bool:
        '''
        Verifies that a connection can be established with the host.
        '''
        #cmd = 'ssh -i %s %s@%s "ls"' % (self.identity,
        #                                self.username,
        #                                self.hostname)
        _, returncode = self.run_remote_cmd("ls", splitCmd=True, timeout=5)
        return returncode == 0

    def run_cmd(self,
                cmd: (str, list),
                shell: bool=False,
                suppressOutput: bool=True,
                timeout: int=30,
                ) -> (str, int):
        '''
        Run a command with a timeout.

        Args:
          cmd::str
            Command to be run
          shell:bool
            Specify whether or not to use a shell during the call
          suppressOutput::bool
            Specify whether or not to print output to stdout
          timeout::int
            Time in seconds to allow cmd to run

        Returns::(str, int)
          String of the output (if enabled, else empty string)
          Int of the return code
        '''
        stdout = subprocess.DEVNULL if suppressOutput else subprocess.STDOUT

        self.logger.debug('Running Command: %s' % cmd)
        try:
            response = subprocess.run(cmd,
                                      shell=shell,
                                      stdout=stdout,
                                      stderr=subprocess.PIPE,
                                      timeout=timeout)
        except subprocess.TimeoutExpired as e:
            err = 'Timeout exceeded for command "%s"' % cmd
            self.logger.error(err)
            output = ''
            returncode = -1
        else:
            output = '' if suppressOutput else response.stdout.decode('utf-8')
            returncode = response.returncode

            if response.stderr:
                self.logger.error(response.stderr.decode('utf-8'))

        return output, returncode

    def run_remote_cmd(self,
                       cmd: (str, list),
                       shell: bool=False,
                       splitCmd: bool=False,
                       suppressOutput: bool=True,
                       timeout: int=30,
                       ) -> (str, int):
        '''
        Run a command on the remote host.

        Args:
          cmd::str
            Command to be run
          shell:bool
            Specify whether or not to use a shell during the call
          splitCmd::bool
            Specify to split command before running or not
          suppressOutput::bool
            Specify whether or not to print output to stdout
          timeout::int
            Time in seconds to allow cmd to run
        '''
        if type(cmd) is list:
            cmd = ' '.join(cmd)

        fullCmd = 'ssh -i %s %s@%s "%s"' % (self.identity,
                                            self.username,
                                            self.hostname,
                                            cmd)
        if splitCmd:
            fullCmd = fullCmd.split()

        return self.run_cmd(fullCmd,
                            shell=shell,
                            suppressOutput=suppressOutput,
                            timeout=timeout)
