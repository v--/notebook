import importlib
import pathlib
import pkgutil

import click

from notebook.commands.coderefs.command import coderefs
from notebook.paths import CODE_PATH
from notebook.support.coderefs import collector


def recursively_load_modules(module_path: pathlib.Path, module_name: str) -> None:
    importlib.import_module(module_name)

    for submodule_info in pkgutil.walk_packages([module_path]):
        recursively_load_modules(
            module_path / submodule_info.name,
            module_name + '.' + submodule_info.name,
        )


@coderefs.command()
@click.argument('output-path', type=click.Path(writable=True, dir_okay=False, path_type=pathlib.Path), default='aux/corderef.aux')
def collect(output_path: pathlib.Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    recursively_load_modules(CODE_PATH / 'math', 'notebook.math')

    with output_path.open('w', encoding='utf-8') as file:
        file.write('\\ExplSyntaxOn\n')

        for doc_ref, fun in collector.mapping.items():
            module_name = fun.__module__.removeprefix('notebook.math.')
            code_ref = f'{module_name}.{fun.__qualname__}'.replace('.', '.\\penalty0 ')  # Allow a line break after the dot
            file.write(f'\\prop_gput:Nnn \\g_nb_coderef_prop {{{doc_ref}}} {{{code_ref}}} \n')

        file.write('\\ExplSyntaxOff\n')
