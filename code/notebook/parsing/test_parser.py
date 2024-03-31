from dataclasses import dataclass

from .parser import Parser


def test_error_basic():
    parser = Parser('test')
    parser.advance()
    msg = parser.get_error_message('Error', precede=0, succeed=0)
    assert msg == '''Error
test
 ↑
'''


def test_error_on_eot():
    parser = Parser('test')
    parser.advance(4)
    msg = parser.get_error_message('Error', precede=0, succeed=0)
    assert msg == '''Error
test⌁
    ↑
'''


def test_error_multiline_basic():
    parser = Parser('test1\ntest2\ntest3')
    parser.advance(7)
    msg = parser.get_error_message('Error', precede=0, succeed=0)
    assert msg == '''Error
test2
 ↑
'''


def test_error_multiline_precede():
    parser = Parser('test1\ntest2\ntest3')
    parser.advance(7)
    msg = parser.get_error_message('Error', precede=3, succeed=0)
    assert msg == '''Error
test1
test2
 ↑
'''


def test_error_multiline_succeed():
    parser = Parser('test1\ntest2\ntest3')
    parser.advance(7)
    msg = parser.get_error_message('Error', precede=0, succeed=10)
    assert msg == '''Error
test2
 ↑
test3'''


def test_error_on_line_break():
    parser = Parser('test1\ntest2\ntest3')
    parser.advance(11)
    msg = parser.get_error_message('Error', precede=0, succeed=1)
    assert msg == '''Error
test2↵
     ↑
test3'''


@dataclass
class StringWrapper:
    payload: str

    def __str__(self):
        return self.payload


def test_string_wrapper_basic():
    parser = Parser([
        StringWrapper('test1')
    ])

    msg = parser.get_error_message('Error', precede=0, succeed=0)
    assert msg == '''Error
test1
↑↑↑↑↑
'''


def test_string_wrapper_on_line_break():
    parser = Parser([
        StringWrapper('test1\n'),
        StringWrapper('test2\n'),
        StringWrapper('test3')
    ])

    parser.advance(1)
    msg = parser.get_error_message('Error', precede=0, succeed=0)
    assert msg == '''Error
test2↵
↑↑↑↑↑↑
'''
