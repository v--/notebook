from enum import Flag, auto


class TypingStyle(Flag):
    implicit = auto()
    explicit = auto()
    gradual = implicit | explicit
