A small DB tagging media.ccc.de videos.

As I do not know which format is required I wrote all the data into a python
program - that way it can be exported in any format.

![Python application test](https://github.com/Thorsten-Sick/tags_for_media_ccc_de/workflows/Python%20application/badge.svg)

# Low hanging fruit

- Methodisch Inkorrekt series
- FNORD newsshow series
- Ultimate talks series
- jeopardy series
-

TODO: Moving towards plugins for different data sources  (?): https://pluggy.readthedocs.io/en/latest/#a-toy-example
TODO: Moving towards a proper database (ElasticSearch overkill)


# Calling it

Frab only:
./dropdata.py --frab --out frab

# Data sources

## FRAB data bases (XML)

## subtitles

mirror.selfnet.de

## Usage

Getting statistics:
./dropdata.py --frab --statistics


## Development

### Running tox tests

Just call *tox*

### Travis on Github

### Running unittests

TODO: Running tests

https://docs.python.org/3/library/unittest.html

### Virtual Env and requirements

TODO: Enter/exit Venv (because I will use it a lot more)




TODO: Building packages (local, remote)

https://medium.com/@alejandrodnm/testing-against-multiple-python-versions-with-tox-9c68799c7880