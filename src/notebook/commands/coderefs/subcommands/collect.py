import contextlib
import pathlib
import pkgutil
from typing import TYPE_CHECKING, cast

import click

from notebook.commands.coderefs.command import coderefs
from notebook.paths import CODE_PATH
from notebook.support.coderefs import collector


if TYPE_CHECKING:
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


@coderefs.command()
@click.argument('output-path', type=click.Path(writable=True, dir_okay=False, path_type=pathlib.Path), default='aux/corderef.aux')
def collect(output_path: pathlib.Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    recursively_load_modules(CODE_PATH / 'math')

    with output_path.open('w', encoding='utf-8') as file:
        file.write('\\ExplSyntaxOn\n')

        for doc_ref, fun in collector.mapping.items():
            module_name = fun.__module__.removeprefix('notebook.math.')
            code_ref = f'{module_name}.{fun.__qualname__}'.replace('.', '.\\penalty0 ')  # Allow a line break after the dot
            file.write(f'\\prop_gput:Nnn \\g_nb_coderef_prop {{{doc_ref}}} {{{code_ref}}} \n')

        file.write('\\ExplSyntaxOff\n')
