import click
from ecs import project_loader
import yaml
import json
from pprint import pprint


# Shared options
_shared_options = [
    click.option('-p', '--project-path', 'project_path', show_default=True, default="ecs/"),
    click.option('-v', '--val', 'values', type=click.Path(exists=True), multiple=True),
    click.option('-e', 'envs', type=str, multiple=True)
]


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


# Definition of group necessary for building arguments
@click.group()
def group(**kwargs):
    pass


def _render_project(**kwargs):
    """ Function used for handling project_path, values, and envs options"""
    # Convert env input into dict
    envs = list(kwargs.get('envs', []))
    envs = dict([x.split('=') for x in envs])

    # Load and interpolate project
    return project_loader.load_project(
        kwargs.get('project_path'),
        list(kwargs.get('values', [])),
        envs)


@group.command()
@add_options(_shared_options)
@click.option('-f', '--format', 'oformat', type=click.Choice(['json', 'yaml']), default='json')
def render(**kwargs):
    """ Function interpolating whole project """

    # Interpolate the project
    ld = _render_project(**kwargs)
   
    # Print
    for i in zip(['Task definition', 'Service'], ld):
        # Generate in the output format
        if kwargs['oformat'].lower() == 'yaml':
            g = yaml.dump(i[1])
        if kwargs['oformat'].lower() == 'json':
            g = json.dumps(i[1],indent=2)
        
        # Print
        click.secho("* {}:".format(i[0]), fg='green')
        click.echo(g)


@group.command()
@add_options(_shared_options)
@click.option('-f', '--format', 'oformat', type=click.Choice(['json', 'yaml']), default='json')
def output(**kwargs):
    """ Function interpolating description of deployment project """
    # Interpolate the project
    ld = _render_project(**kwargs)
   
    # Print the output
    click.echo(ld[2])


if __name__ == '__main__':
    group()