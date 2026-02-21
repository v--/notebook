import pathlib
import re
import tomllib

import click
import loguru


def sync_dependencies(raw_pyproject: str, logger: loguru.Logger, dep_list: list[str], lockfile: dict) -> str:
    for dep_string in dep_list:
        match = re.match(r'(?P<name>[^(@\s]+)\s*\(>=?(?P<version>[^)]+)\)', dep_string)

        if match is None:
            continue

        name = match.group('name')
        version = match.group('version')

        for pkginfo in lockfile['package']:
            if pkginfo['name'] == name:
                if version != pkginfo['version']:
                    logger.info(f'Changing version of {name} from {version} to {pkginfo['version']}')
                    updated_dep_string = dep_string.replace(version, pkginfo['version'])
                    raw_pyproject = raw_pyproject.replace(dep_string, updated_dep_string)

                break

    return raw_pyproject


@click.command(help='A naive scripts that iterates through version specifiers of the form "package (>=version)" and updates the version based on the lockfile.')
@click.option('-p', '--pyproject', default='pyproject.toml', type=click.Path(readable=True, exists=True, dir_okay=False, path_type=pathlib.Path))
@click.option('-l', '--lockfile', default='poetry.lock', type=click.Path(readable=True, exists=True, dir_okay=False, path_type=pathlib.Path))
def merge_lockfile(pyproject: str, lockfile: str) -> None:
    with open(pyproject) as file:
        raw_pyproject = file.read()
        pyproject_toml = tomllib.loads(raw_pyproject)

    with open(lockfile, 'rb') as file:
        lockfile_toml = tomllib.load(file)

    if project_section := pyproject_toml.get('project'):
        if dep_list := project_section.get('dependencies'):
            logger = loguru.logger.bind(logger='Project dependencies')
            raw_pyproject = sync_dependencies(raw_pyproject, logger, dep_list, lockfile_toml)

        if optional := project_section.get('optional-dependencies'):
            for list_name, dep_list in optional.items():
                logger = loguru.logger.bind(logger=f'Optional dependency list {list_name!r}')
                raw_pyproject = sync_dependencies(raw_pyproject, logger, dep_list, lockfile_toml)

    if groups := project_section.get('dependency-groups'):
        for list_name, dep_list in groups.items():
            logger = loguru.logger.bind(logger=f'Dependency group {list_name!r}')
            raw_pyproject = sync_dependencies(raw_pyproject, logger, dep_list, lockfile_toml)

    with open(pyproject, 'w') as file:
        file.write(raw_pyproject)
