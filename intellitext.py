import json
import sys
import pyperclip as clipboard
from pynput.keyboard import Controller, Key, Listener
from random import choice


class IntelliText:
    """
    IntelliText listens to keyboard input and performs actions based on the input.

    * ! are used for words

    * # are used for actions

    *** #cb is predefined

    more macro support will be added in the future
    """

    def __init__(self):
        self.controller = Controller()
        try:
            self.setting: dict = json.load(open(f'{get_cur_file_dir()}\\macros.json', 'r'))
        except FileNotFoundError:
            with open(f'{get_cur_file_dir()}\\macros.json', 'w') as f:
                ojb = {
                    'macros': {
                        'word': {},
                        'action': {
                            '#cb': ''
                        }
                    },
                    'macro_settings': {
                        'shuffle': {
                            'enabled': False,
                            'shuffle_macros': []
                        }
                    }
                }
                f.write(json.dumps(ojb, indent=4))
                self.setting: dict = ojb
        self.__specifiers = ['!', '#']
        self.__shuffle_macros = self.__get_shuffle_settings()
        self.__macro = ''

    def __get_shuffle_settings(self):
        shuffle = self.setting.get('macro_settings').get('shuffle')
        return shuffle.get('shuffle_macros') if shuffle.get('enabled') else None

    def __type_macro(self, macro: str, shuffle=False) -> None:
        for _ in range(len(macro)):
            self.controller.tap(Key.backspace)

        if shuffle:
            self.controller.type(choice(self.setting.get('macros').get('word').get(macro).split(',')))
        else:
            self.controller.type(self.setting.get('macros').get('word').get(macro))

        self.__macro = ''

    def __process_word_macro(self) -> None:
        if self.__macro in self.setting.get('macros').get('word'):
            # if the macro is defined in the macros.json, process the value
            if self.__shuffle_macros and self.__macro in self.__shuffle_macros:
                # if the macro is in the shuffle list, shuffle the value
                self.__type_macro(self.__macro, True)
            else:
                self.__type_macro(self.__macro)

    def __process_action_macro(self) -> None:
        if self.__macro in self.setting.get('macros').get('action'):
            # if the macro is defined in the macros.json, process the value
            # macros that start with #r are run actions,
            #  meaning a process with that name would run

            # macros that start with #c are run actions too,
            #  meaning the defined command would execute
            if self.__macro == '#cb':
                for _ in range(len(self.__macro)):
                    self.controller.tap(Key.backspace)
                self.controller.type(clipboard.paste())

            self.__macro = ''

    def __on_press(self, key) -> None:
        try:
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
        except AttributeError or TypeError:
            pass

    def listen(self):
        try:
            with Listener(on_press=self.__on_press) as listener:
                listener.join()
        finally:
            listener.stop()


def get_cur_file_dir():
    # sys.argv[0] is the path of the script
    path = sys.argv[0]
    strip_file_name = path.split('\\')[:-1] or path.split('/')[:-1]
    return "\\".join(strip_file_name)


def main():
    intellitext = IntelliText()
    intellitext.listen()


if __name__ == '__main__':
    main()
