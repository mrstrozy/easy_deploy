'''
Module used to parse/verify an easy_deploy config.
'''

import yaml

from easy_deploy.util.options_menu import OptionMenu, CommandNotFoundError

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

    def build(self,
              filename: str,
              ) -> (list, list):
        '''
        Builds the command queue from a easy_deploy config file

        Args:
          filename::str
            Name of the config file to parse

        Returns::list(dict)
          List of built commands in dict form
        '''
        config = self._load(filename)
        runlist = []
        errors = self._parse(config)

        if not errors:
            runlist += self._build_with_optionals(config)

        return runlist, errors

    def _build_with_optionals(self,
                              config: list,
                              ) -> list:
        '''
        Appends any missing optional config options to the config

        Args:
          config::list
            List of config blocks of easy_deploy config

        Returns::list
          List of dictionaries containing the filled in options
        '''
        runlist = []
        for block in config:
            command = block.get('command')
            optional_dict = self.optionMenu.get_optional_options(command)
            for k, v in optional_dict.items():
                if k not in block:
                    block[k] = v
            runlist.append(block)
        return runlist

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

    def _parse(self,
              config: list,
              ) -> list:
        '''
        Parses an easy_deploy config list

        Args:
          config::list
            List of config blocks of easy_deploy config
        
        Returns::list
          List of any errors found. Empty if none.
        '''
        errors = []
        for block in config:
            err = self._verify_block(block)
            if err:
                errStr = "Block: %s\n  - %s" % (block, "\n  - ".join(err))
                errors.append(errStr)
        return errors

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
        else:
            try:
                self.optionMenu.verify_command(command)
            except CommandNotFoundError:
                err = '%s is not a valid command' % command
                errors.append(err)
            else:
                all_options = self.optionMenu.get_all_option_names(command)
                mand = self.optionMenu.get_mandatory_option_names(command)
                block_keys = block.keys()

                # Verify all mandatory options are set
                for option in mand:
                    if option not in block_keys:
                        errMsg = 'Mandatory option "%s" not set' % option
                        errors.append(errMsg)

                # Verify all options set are known options
                for key in block.keys():
                    if key not in all_options:
                        err = 'Option: "%s" not recognized' % key
                        errors.append(err)
        return errors

