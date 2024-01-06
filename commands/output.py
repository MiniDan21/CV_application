'''Модуль для вывода интерфейса'''
print_red = lambda msg: print(f"\x1B[31m{msg}\033[0m\t\t")
print_blue = lambda msg: print(f"\x1B[36m{msg}\033[0m\t\t")
print_green = lambda msg: print(f"\x1B[32m{msg}\033[0m\t\t")
print_yellow = lambda msg: print(f"\x1B[33m{msg}\033[0m\t\t")


first_choose = True

def _welcome_msg(msg: str = "\nДобро пожаловать! Укажите одну из команд, чтобы начать или нажмите Ctrl+C, чтобы завершить") -> None:
    print_blue(msg)

def _remember_msg(msg: str = "\nУкажите одну из команд, чтобы начать, или нажмите Ctrl+C, чтобы завершить"):
    print_blue(msg)

def _print_commands(commands):
    for cmd in commands:
        print_green(cmd)

def print_menu(menu):
    global first_choose

    if first_choose:
        _welcome_msg()
        first_choose &= False
    else:
        _remember_msg()
    _print_commands(menu)

def print_finished(msg: str = "\nЗавершение программы..."):
    print_blue(msg)

def print_input_error(msg: str = "\nНеверно указан номер!"):
    print_red(msg)

def print_error(msg: str = "\nПроизошла ошибка!"):
    print_red(msg)
