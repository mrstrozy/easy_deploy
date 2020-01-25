'''
Module for handling all connections with remote hosts.
'''

import logging
import subprocess

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

    def verify_connection(self,
                          ) -> bool:
        '''
        Verifies that a connection can be established with the host.
        '''
        cmd = 'ssh -i %s %s@%s "ls"' % (self.identity,
                                        self.username,
                                        self.hostname)
        _, returncode = self._run_cmd(cmd, timeout=5)
        return returncode == 0

    def _run_cmd(self,
                 cmd: str,
                 suppressOutput: bool=True,
                 timeout: int=30,
                 ) -> (str, int):
        '''
        Run a command with a timeout.

        Args:
          cmd::str
            Command to be run
          timeout::int
            Time in seconds to allow cmd to run

        Returns::(str, int)
          String of the output (if enabled, else empty string)
          Int of the return code
        '''
        stdout = subprocess.STDOUT
        if suppressOutput:
            stdout = subprocess.DEVNULL

        try:
            response = subprocess.run(cmd.split(),
                                      stdout=stdout,
                                      timeout=timeout)
        except subprocess.TimeoutExpired as e:
            err = 'Timeout exceeded for command "%s"' % cmd
            self.logger.error(err)
            output = ''
            returncode = -1
        else:
            output = '' if suppressOutput else response.stdout.decode('utf-8')
            returncode = response.returncode

        return output, returncode
