'''
Module used to run any content verifications necessary for 
the easy_deploy program.
'''

import os

from easy_deploy.util.constants import DEFAULT_FILE_DIRNAME

class Verifier:
    def __init__(self,
                 baseDir: str,
                 ):
        '''
        Args:
          baseDir::str
            The base directory in which the content resides.
        '''
        self.baseDir = baseDir

    def verify_files(self,
                     runlist: list,
                     ) -> list:
        '''
        Verifies that the files in the runlist are present.

        Args:
          runlist::list(dict)
            List of dictionaries specifiying the content used.

        Returns::list
          List of any files missing, empty list if none
        '''
        missing_files = []
        for step_definition in runlist:
            command = step_definition.get('command', '')
            if command == 'installFile':
                filename = step_definition.get('localSource', '')
                filepath = '%s/%s/%s' % (self.baseDir,
                                         DEFAULT_FILE_DIRNAME,
                                         filename)
                if not os.path.isfile(filepath):
                    missing_files.append(filename)
        return missing_files
