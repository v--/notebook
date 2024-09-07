from .author import BibAuthor


def test_author_get_shortened_string() -> None:
    author = BibAuthor(
        main_name='Main',
        other_names='Other',
        title='Title',
        display_name='Display'
    )

    assert author.get_shortened_string() == 'Display'


def test_author_get_shortened_string_no_display() -> None:
    author = BibAuthor(
        main_name='Main',
        other_names='Other',
        title='Title'
    )

    assert author.get_shortened_string() == 'Other Main'


def test_author_get_shortened_string_only_main() -> None:
    author = BibAuthor(
        main_name='Main',
        title='Title'
    )

    assert author.get_shortened_string() == 'Main'


def test_author_get_full_string() -> None:
    author = BibAuthor(
        main_name='Main',
        other_names='Other',
        title='Title',
        display_name='Display'
    )

    assert str(author) == 'Main, Title, Other'


def test_author_get_full_no_title() -> None:
    author = BibAuthor(
        main_name='Main',
        other_names='Other',
        display_name='Display'
    )

    assert str(author) == 'Main, Other'
