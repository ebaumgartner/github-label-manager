# github-label-manager
Efficiently manage a set of GitHub issue labels.

This repo will help you curate, review, and apply a set of labels to GitHub issues.

## Installation

```bash
npm install
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Access Token

Make your github personal access token available via `export GITHUB_ACCESS_TOKEN=...`.
All tools will pick it up as needed. You can also pass the token in the command line.

## Download the current label set for a repo

Repos are referenced via owner and repo name,
e.g. "owner/my-repo".

`python manage.py download REPO labels.json`

Result is a json file containing a list of objects. Each object
looks like:

```json
{
    "name": "type-bug",
    "color": "F2B7B8",
    "aliases": ["bug"],
    "description": "Something isn't working",
    "delete": false
}
```

This is the format used by [github-label-sync](https://github.com/Financial-Times/github-label-sync#label-config-file). Note that while github-label-sync also
supports YAML, this repo focuses solely on JSON.

## Create an html file to preview a local label set

`python manage.py preview labels.json labels.html`

Then open labels.html in a browser to review the labels. This is mostly useful to assess the label color scheme.
Be sure to check colors in light and dark mode.

## Upload your labels to a repo

`npx github-label-sync REPO --labels labels.json`

Add `-d` to do a dry run and see what would change.

