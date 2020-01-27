'''
Module used to interact with easy_deploy requirements.
'''

from easy_deploy.util.config_requirements_def import (COMMANDS,
                                                      UNIVERSAL_OPTIONS)

class OptionMenuException(Exception):
    ''' Base Exception for OptionMenu Class '''

class CommandNotFoundError(OptionMenuException):
    ''' Raised if a command name is not found in requirements '''

class OptionMenu:
    def get_all_option_names(self,
                             command: str,
                             ) -> list:
        '''
        Returns all available option names for the inputted command.

        Args:
          command::str
            Command name to retrieve all options for

        Returns::list
          List of option names available for the command

        Raises:
          CommandNotFoundException
            If no command definition is found
        '''
        options = UNIVERSAL_OPTIONS[:]
        
        # Will raise exception if command not found
        options += self.get_mandatory_option_names(command)
        options += self.get_optional_option_names(command)

        return options

    def get_mandatory_option_names(self,
                                   command: str,
                                   ) -> list:
        '''
        Returns all required option names for the inputted command

        Args:
          command::str
            Command name to retrieve required options for
        
        Returns::list
            List of required options for the command.

        Raises:
          CommandNotFoundException
            If no command definition is found
        '''
        command_entry = self.verify_command(command)
        return list(command_entry.get('mandatory'))

    def get_optional_options(self,
                             command: str,
                             ) -> dict:
        '''
        Returns optional dictionary listing options

        Args:
          command::str
            Name of command 

        Returns::dict
          Dict of optional options

        Raises:
          CommandNotFoundException
            If no command definition is found
        '''
        command_entry = self.verify_command(command)
        return dict(command_entry.get('optional', {}))
        
    def get_optional_option_names(self,
                                  command: str,
                                  ) -> list:
        '''
        Returns all optional option names for the inputted command.

        Args:
          command::str
            Command name to retrieve optional options for.

        Returns::list
            List of all optional options

        Raises:
          CommandNotFoundException
            If no command definition is found
        '''
        return self.get_optional_options(command).keys()

    def verify_command(self,
                        command: str,
                        ) -> dict:
        '''
        Verifies a command exists in specified commands.

        Args:
          command::str
            Command name to verify
        
        Returns::dict
          Entry that correlates to the command name

        Raises:
          CommandNotFoundException
            If no command definition is found
        '''
        command_entry = COMMANDS.get(command)

        if not command_entry:
            err = 'Command not found: %s' % command
            raise CommandNotFoundError(err)
        
        return command_entry
