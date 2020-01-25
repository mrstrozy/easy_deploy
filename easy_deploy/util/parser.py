'''
Module used to parse/verify an easy_deploy config.
'''

import yaml

from config_requirements import commands, universal_options 
from options_menu import OptionMenu 

class EasyDeployParserException(Exception):
    ''' General Parser Exception '''

class EasyDeployCommandNotFound(EasyDeployParserException):
    ''' Exception thrown when unable to find command in command list '''

class EasyDeployConfigError(EasyDeployParserException):
    ''' Exception thrown when unable to parse easy_deploy config '''

class EasyDeployParser:

    def __init__(self,
                 ):
        self.optionMenu = OptionMenu()

    def parse(self,
              filename: str,
              ) -> list:
        '''
        Parses an easy_deploy config file

        Args:
          filename::str
            Name of config file to parse
        
        Returns::list
          List of any errors found. Empty if none.
        '''
        errors = []
        config = self._load(filename)

        for block in config:
            err = self._verify_block(block)

    def _load(self,
             filename: str,
             ):
        '''
        Load filename (expected YAML format)

        Args:
          filename::str
            Name of YAML file to load

        Returns:
        '''
        with open(filename, 'r') as stream:
            try:
                contents = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise EasyDeployConfigError(exc)

        return contents


    def _verify_block(self,
                      block: dict,
                      ) -> str:
        '''
        Verifies a dictionary block in a easy_deploy config file.

        Args:
          block::dict{string:string}
            easy_deploy dictionary of step to be verified

        Returns::str
          String of any error found. If none, an empty string is returned.
        '''
        errors = []
        command = block.get('command')

        if not command:
            errors.append('No command specified')
            return errors

        if command not in commands:
            err = '%s is not a valid command' % command
            errors.append(err)
            return errors

        for key in block.keys():
        # TODO Look for errors with the block through optionmenu
