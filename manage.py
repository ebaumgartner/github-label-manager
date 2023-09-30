#!/usr/bin/env python

import json

import click
from github import Github
from github import Auth


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug


@cli.command()
@click.argument("repo", type=click.STRING)
@click.argument("output", type=click.File('w'))
@click.option(
    "--token", "--t",
    envvar="GITHUB_ACCESS_TOKEN",
    type=click.STRING,
    help="Your GitHub access token."
)
@click.pass_context
def download(ctx, repo, output, token):
    """
    Download the labels used by a REPO to json file OUTPUT.

    REPO should take the form "author/repo-name".

    OUTPUT is the file path to save the output to, or "-" for stdout.

    Be sure to define your GitHub access token via --token or by setting
    GITHUB_ACCESS_TOKEN.

    """
    def convert_label(label):
        return {
            "name": label.name,
            "color": label.color,
            "aliases": [],
            "description": label.description,
            "delete": False
        }

    try:
        auth = Auth.Token(token)
        g = Github(auth=auth)
        repo = g.get_repo(repo)
        labels = [convert_label(label) for label in repo.get_labels()]
        json.dump(labels, output, indent=2)
    except Exception as e:
        click.echo(e)
        exit(1)


@cli.command()
@click.pass_context
def preview(ctx):
    """Create a html file to preview labels."""
    click.echo("previewing...")


if __name__ == '__main__':
    cli(obj={})
