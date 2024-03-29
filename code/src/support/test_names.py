from .names import new_var_name


def test_new_var_name():
    assert new_var_name('test', set()) == 'test'
    assert new_var_name('test', {'test'}) == 'test₀'
    assert new_var_name('test', {'test', 'test₀'}) == 'test₁'
    assert new_var_name('test', {'test', 'test₀', 'test₁'}) == 'test₂'
    assert new_var_name('test', {'test', 'test₀suffix'}) == 'test₀'

    assert new_var_name('test₉₃', {'test₉₃'}) == 'test₉₄'
