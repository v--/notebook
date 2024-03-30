from abc import ABC, abstractmethod
from enum import Flag, auto

from .tokens import TokenEnum


class Whitespace(TokenEnum):
    line_break = '\n'
    tab = '\t'
    space = ' '
