'''Пакет для реализации пользовательского интерфейса'''
from .commands import commands
from .executor import Executor


executor = Executor(commands)
executor._load_methods(commands.values())