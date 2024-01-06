from time import sleep

from .commands import *
from .output import *


class Executor:
    def __init__(self, states, *args, **kwargs) -> None:
        self.state = -1
        self._methods = dict()
        self._cout= ""
        self.main_states = states

    def _load_methods(self, func: list):
        last_index = len(self._methods)
        self._methods.update({last_index + index: func for index, func in enumerate(func)})

    def _reset(self):
        self.state = -1
        self._cout= ""
    
    def _execute(self, num, *args, **kwargs):
        self._cout = self._methods[num](*args, **kwargs)
    
    def _output(self):
        if self._cout:
            print_yellow(self._cout)
            self._reset()
        elif self.state == -1:
            sleep(1)
            print_menu(self.main_states)
        else:
            print_error()
            exit(-1)
    
    # Каждая команда реализует свой ввод
    def _input(self, r_str = "\nНомер команды\n>"):
        try:
            return input(r_str)
        except KeyboardInterrupt:
            print_finished()
            exit(0)

    def to_int(self, cmd):
        try:
            return int(cmd)
        except ValueError:
            print_input_error()
        return 0

    def run(self, *args, **kwargs):
        while True:
            if self.state == -1:
                self._output()
                res = self.to_int(self._input())
                if res:
                    self.state = res - 1
            if self.state != -1:
                try:
                    self._execute(self.state)
                except Exception:
                    pass
                self._output()
