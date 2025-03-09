# Scryfall RSS Generator

## Description

This project generates an RSS feed from a specified Scryfall search query, which is useful for keeping keep track of new Magic: The Gathering cards with specific characteristics. The script can be run manually or set up to automatically update periodically using GitHub Actions, cron jobs, or scheduled tasks.

## Prerequisites

Python 3.7 or higher is required.

The dependencies are:
- requests >= 2.28.0
- feedgenerator >= 2.0.0

These are listed in the `pyproject.toml` file and can be installed using pip or the package manager of your choice:

```bash
pip install -e .
```

## Usage

### Forking the Repo (Recommended)

This repository includes a GitHub Actions workflow that automatically generates and updates the RSS feed daily. This solves two problems--how to generate the feed on a schedule, and how to host it online so your feed reader can access it.

To use this option, fork the repo and change the Scryfall search query in `.github/workflows/scryfall_rss.yml`. You can also adjust the update frequency there, which defaults to daily. The workflow commits and pushes the updated feed to the `rss-feed` branch. You can also manually trigger the workflow from the Actions tab in the GitHub repository.

Point your RSS reader to the raw GitHub user content link of the feed on the `rss-feed` branch. For this repo, that URL would be:

```
https://raw.githubusercontent.com/samiralam/scryfall-rss/refs/heads/rss-feed/scryfall_feed.xml
```

### Running the Script Locally

If you want to self-host the feed, you can run the script locally with a cron job and host it in Google Drive or your own web server.

```bash
python scryfall_rss.py [options]
```

## Options

You can run the script with a Scryfall search query:

```bash
python scryfall_rss.py "((t:angel c=w) or (t:demon c=b) or (t:dragon c=r) or (t:sphinx c=u) or (t:wurm c=g)) not:reprint order:released"
```

Or use the Scryfall URL directly:

```bash
python scryfall_rss.py --url "https://scryfall.com/search?q=%28%28t%3Aangel+c%3Dw%29+or+%28t%3Ademon+c%3Db%29+or+%28t%3Adragon+c%3Dr%29+or+%28t%3Asphinx+c%3Du%29+or+%28t%3Awurm+c%3Dg%29%29+not%3Areprint+order%3Areleased&order=name"
```

- `--url` or `-u`: Run on a URL instead of a search query
- `--output` or `-o`: Specify the output file path (defaults to `scryfall_feed.xml`)
- `--title` or `-t`: Set a custom title for the RSS feed
- `--description` or `-d`: Set a custom description for the RSS feed

## License

This project is licensed under the MIT License.