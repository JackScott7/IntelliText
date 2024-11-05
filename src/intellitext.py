import json
import os.path
import subprocess
import sys
import pyperclip as clipboard
import subprocess as sp
from pynput.keyboard import Controller, Key, Listener
from random import choice


class IntelliText:
    """
    IntelliText (it) is a powerful, customizable keyboard macro and text expansion tool

    * ! are used for words

    * # are used for actions

    * extensions can be called via @ and ending with $
    example: @ip$

    *** #cb is predefined, types clipboard content
    *** #ite is predefined, exits it (IntelliText)
    """

    def __init__(self):
        self.controller = Controller()
        try:
            self.__it_path = f"{os.environ['USERPROFILE']}\\.intellitext"

            if not os.path.isdir(self.__it_path):
                os.mkdir(self.__it_path)

            self.setting: dict = json.load(open(f"{self.__it_path}\\it_macros.json", 'r'))
        except FileNotFoundError:
            with open(f"{self.__it_path}\\it_macros.json", 'w') as f:
                obj = {
                    '$schema': 'https://raw.githubusercontent.com/JackScott7/IntelliText/refs/heads/main/schema.json',
                    'macros': {
                        'word': {},
                        'action': {
                            "#ite": "",
                            "#cb": ""
                        }
                    },
                    'macro_settings': {
                        'shuffle': {
                            'enabled': 'false',
                            'shuffle_macros': []
                        }
                    },
                    'extension_settings': {
                        'enabled': 'false',
                        'extensions': []
                    }
                }
                f.write(json.dumps(obj, indent=4))
                self.setting: dict = obj
        self.__specifiers = ['!', '#', '@']
        self.__shuffle_macros = self.__get_shuffle_settings()
        self.__extensions_path = f'{self.__it_path}\\extensions'
        self.__setup_extensions()
        self.__macro = ''

    def __setup_extensions(self) -> None:
        if not os.path.isdir(self.__extensions_path):
            print('[-] Extensions directory does not exist, created directory...')
            os.mkdir(self.__extensions_path)

    def __get_shuffle_settings(self):
        shuffle = self.setting.get('macro_settings').get('shuffle')
        # using eval(str.title()) to convert the json string to python boolean
        # the str.title just capitalizes only the first letter of each word which in this case
        # it's only the true or false in lowercase
        enabled = shuffle.get('enabled')
        if enabled is not bool:
            enabled = eval(enabled.title())
        return shuffle.get('shuffle_macros') if enabled else None

    @property
    def __extension_enabled(self) -> bool:
        enabled = self.setting.get('extension_settings').get('enabled')
        if enabled is not bool:
            enabled = eval(enabled.title())
        return enabled

    def __untype_macro(self) -> None:
        [self.controller.tap(Key.backspace) for _ in range(len(self.__macro))]

    def __type_macro(self, macro: str, shuffle=False) -> None:
        self.__untype_macro()

        macro_value = self.setting.get('macros').get('word').get(macro)

        if ',' in macro_value:
            macro_values = macro_value.split(',')
        else:
            macro_values = [macro_value]

        if shuffle:
            selected_value = choice(macro_values)
        else:
            selected_value = macro_values[0]

        self.controller.type(selected_value)

        self.__macro = ''

    def __process_word_macro(self) -> None:
        if self.__macro in self.setting.get('macros').get('word'):
            # if the macro is defined in the it_macros.json, process the value
            if self.__shuffle_macros:
                # shuffle macro if in shuffle list
                self.__type_macro(self.__macro, self.__macro in self.__shuffle_macros)

    def __process_action_macro(self) -> None:
        action: dict = self.setting.get('macros').get('action')

        if self.__macro in action:
            # if the macro is defined in the it_macros.json, process the value
            # macros that start with #r are run actions,
            #  meaning a process with that name would run
            try:
                if self.__macro.startswith('#r'):
                    self.__untype_macro()
                    sp.Popen(action.get(self.__macro))

                # macros that start with #c are run actions too,
                #  meaning the defined command would execute
                elif self.__macro == "#ite":
                    self.__untype_macro()
                    exit(0)

                elif self.__macro == '#cb':
                    self.__untype_macro()
                    self.controller.type(clipboard.paste())

                self.__macro = ''
            except OSError as ose:
                sys.stderr.write(f"err on running: `{self.__macro}`"
                                 f"\n{action.get(self.__macro)}\n{ose.strerror}")

    def __on_press(self, key) -> None:
        try:
            # register space if the macro is an extension
            if key == Key.space:
                self.__macro += ' '

            # update macro with backspace to remove the last character
            if key == Key.backspace:
                self.__macro = self.__macro[:-1]
                return

            if key.char in self.__specifiers:
                self.__macro = key.char
            else:
                # only add the key if the macro starts with a specifier
                if any([self.__macro.startswith(specifier) for specifier in self.__specifiers]):
                    # add actual value of key to macro
                    if key.char is not None:
                        self.__macro += key.char
            # word macros start with !
            if self.__macro and self.__macro.startswith('!'):
                self.__process_word_macro()
            # process macros start with #
            elif self.__macro and self.__macro.startswith('#'):
                self.__process_action_macro()
            # process extensions
            elif self.__macro and self.__macro.startswith('@') and self.__macro.endswith('$'):
                extensions: dict = self.setting.get('extension_settings').get('extensions')
                if self.__extension_enabled:
                    self.__process_extension(extensions)
        except AttributeError or TypeError:
            pass

    def listen(self):
        try:
            with Listener(on_press=self.__on_press) as listener:
                listener.join()
        finally:
            listener.stop()

    def __extension__exist(self, ext, macro) -> (str, bool):
        """
        Checks the extension existence.

        :param ext: Extension name in it_macros.json to check if it exists or not
        :return: a tuple, (str: extension path, bool: state of extension existence)
        """
        ext_path = ext.get(macro)
        if os.path.isdir("\\".join(ext_path.split('\\')[:-1])):
            return ext_path, os.path.isfile(ext_path)
        else:
            relative_ext_path = rf"{self.__extensions_path}\{ext_path}"
            return relative_ext_path, os.path.isfile(relative_ext_path)

    def __macro_has_args(self) -> (bool, list[str]):
        macro = self.__macro.strip().split()
        has_args = False
        macro = [x for x in macro if x != ' ' or x != '']
        if not macro[-1] == '$': # indicates that the last element is attached to the % specifier
            macro[-1] = macro[-1][:-1] # only grap the arg and not the % char
            if len(macro) > 1:
                has_args = True
        else:
            macro = macro[:-1]
        return has_args, macro


    def __process_extension(self, extensions) -> None:
        if not extensions:
            return

        for extension in extensions:
            has_args, macro_args = self.__macro_has_args()
            if macro_args[0] in extension:
                extension_exist = self.__extension__exist(extension, macro_args[0])
                if extension_exist[1]:
                    self.__run_extension(extension, extension_exist, macro_args)
                    break

    def __run_extension(self, extension, extension_exist, macro_args) -> None:
        extension_args = extension.get('args')
        # if the extension has predefined args
        # execute the extension immediately
        # otherwise wait for the ending # to execute it
        extension_run_cmd = [extension.get('cmd'), extension_exist[0]]
        if len(macro_args) > 1:
            extension_run_cmd.extend([*macro_args[1:]])
        elif extension_args:
            extension_run_cmd.extend([*extension_args])
        try:
            extension_type = extension.get('type')
            if extension_type == 'print':
                output = sp.run(extension_run_cmd, check=True, text=True, capture_output=True)
                if output.returncode == 0:
                    self.__untype_macro()
                    self.controller.type(output.stdout.strip())
            elif extension_type == 'action':
                self.__untype_macro()
                sp.Popen(extension_run_cmd)
        except subprocess.CalledProcessError as cpe:
            self.__untype_macro()
            self.controller.type(f"{self.__macro[1:-1]} err output: {cpe.output.strip()}")
