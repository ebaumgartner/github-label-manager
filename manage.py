#!/usr/bin/env python

import colorsys
import json

import click
from github import Github
from github import Auth
from jinja2 import Environment, PackageLoader, select_autoescape


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
@click.argument("labels", type=click.File('r'))
@click.argument("output", type=click.File('w'))
@click.pass_context
def preview(ctx, labels, output):
    """
    Create an html OUTPUT file that previews a LABELS file.

    LABELS is the path to a json file containing labels, or "-" for stdin.

    OUTPUT is the file path for the preview html, or "-" for stdout.

    """
    def add_color_detail(label):
        """Add distinct RGB and HSL values to the label."""
        # rgb values range 0..255
        r, g, b = tuple(int(label["color"][i: i + 2], 16) for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        label.update({
            "r": r,
            "g": g,
            "b": b,
            "h": round(h * 360),
            "l": round(l * 100),
            "s": round(s * 100),
        })

    env = Environment(
        loader=PackageLoader("manage"),
        autoescape=select_autoescape()
    )
    label_list = json.load(labels)
    for label in label_list:
        add_color_detail(label)

    template = env.get_template("preview.html")
    html = template.render(labels=label_list, filename=labels.name)
    output.write(html)


if __name__ == '__main__':
    cli(obj={})
