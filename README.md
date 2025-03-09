# Scryfall RSS Generator

## Description

This project generates an RSS feed from a specified Scryfall search query. The script can be run manually or set up to automatically update periodically using cron jobs or scheduled tasks.

## Prerequisites

The requirements and dependencies are listed in the `pyproject.toml` file.

You can install these dependencies using pip:

```bash
pip install -e .
```

or if you are using uv for package management:

```bash
uv pip install -e .
```

## Usage

### Running the Script

```bash
python scryfall_rss.py [arguments]
```

#### Option 1: Run with a Scryfall query

```bash
python scryfall_rss.py "((t:angel c=w) or (t:demon c=b) or (t:dragon c=r) or (t:sphinx c=u) or (t:wurm c=g)) not:reprint order:released"
```

#### Option 2: Run with a Scryfall URL

```bash
python scryfall_rss.py --url "https://scryfall.com/search?q=%28%28t%3Aangel+c%3Dw%29+or+%28t%3Ademon+c%3Db%29+or+%28t%3Adragon+c%3Dr%29+or+%28t%3Asphinx+c%3Du%29+or+%28t%3Awurm+c%3Dg%29%29+not%3Areprint+order%3Areleased&order=name"
```


## Output

The script generates an XML file named `scryfall_feed.xml` by default. You can change the output file name using the `--output` or `-o` option.

You can open this file in your RSS reader to view the generated feed.

## Customizing the Feed

You can set a custom title and description for the RSS feed:

```bash
python scryfall_rss.py --title "Custom Title" --description "Description of the RSS feed"
```

### Scheduled Updates

To keep your RSS feed updated automatically, run the script as a cron job.

## Additional Options

- `--url` or `-u`: Run on a URL instead of a search query
- `--output` or `-o`: Specify the output file path
- `--title` or `-t`: Set a custom title for the RSS feed
- `--description` or `-d`: Set a custom description for the RSS feed

## License

This project is licensed under the MIT License.