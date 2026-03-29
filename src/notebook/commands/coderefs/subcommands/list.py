import contextlib
import pkgutil
from typing import TYPE_CHECKING, cast

from rich.console import Console
from rich.table import Table

from ....paths import CODE_PATH
from ....support.coderefs import collector
from ..command import coderefs


if TYPE_CHECKING:
    import pathlib

    from _typeshed.importlib import PathEntryFinderProtocol


def recursively_load_modules(path: pathlib.Path) -> None:
    for submod_info in pkgutil.walk_packages([path.as_posix()]):
        subpath = path / submod_info.name

        module_name = 'notebook.' + subpath.relative_to(CODE_PATH).as_posix().replace('/', '.')
        finder = cast('PathEntryFinderProtocol', submod_info.module_finder)

        if (spec := finder.find_spec(module_name)) and (loader := spec.loader):
            # Some modules fail to import with a metaclass error that does not occur otherwise
            # These modules do not bother us, but ideally this would not occur
            with contextlib.suppress(TypeError):
                loader.load_module(module_name)

        if submod_info.ispkg:
            recursively_load_modules(subpath)


@coderefs.command('list')
def list_refs() -> None:
    recursively_load_modules(CODE_PATH / 'math')
    table = Table()
    table.add_column('Monograph reference')
    table.add_column('Function')

    for doc_ref, fun in collector.mapping.items():
        table.add_row(doc_ref, f'{fun.__module__.removeprefix('notebook.')}.{fun.__qualname__}')

    console = Console()
    console.print(table)
