#!/usr/bin/env python3


# TODO: Write a command line tool to browser and search in the database

# TODO: Define a command set to search for strings, tags, similar talks, mark talks as seen, mark talks as irrelevant, mark talks as relevant, open a browser and watch, show details, quit

# https://opensource.com/article/17/5/4-practical-python-libraries

# TODO: Maybe use fuzzyfinder

# TODO: use prompt_toolkit autocompletion, auto suggestion and history

# TODO: Use pygments for syntax highlighting https://pygments.org/

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter
from dropdata import MediaTagger

def printHelp():
    print("""

    tags: list tags
    TODO tags + tag: list all talks containing a specific tag 
    TODO similar: Find similar content
    TODO seen: Mark talks as seen
    TODO irrelevant: Mark talks as irrelevant
    TODO relevant: Mark talks as relevant
    TODO show: Show content in browser
    TODO details: Show details
    quit: quit
    help: get help
    """)

def getCompleter():
    """ Generates a nested completer

    :return:
    """

    mt = MediaTagger(frab=False, subtitles=False, default=False, offline=True)

    return NestedCompleter.from_nested_dict({'help': None,       # Show help
                                             'quit':None,         # Quit
                                             'tags': {key: None for (key) in mt.list_tags()+[""]},        # Search for tags
                                             'similar':None,     # Find similar content using k-nearest
                                             })

if __name__=="__main__":
    BrowserCompleter = getCompleter()

    mt = MediaTagger(frab=False, subtitles=False, default=False, offline=True)
    while 1:
        user_input = prompt('> ',
                            history=FileHistory("history.txt"),
                            auto_suggest=AutoSuggestFromHistory(),
                            completer=BrowserCompleter,
                            )

        user_input = user_input.lower()
        if user_input == "quit":
            break
        elif user_input == "help":
            printHelp()
        elif user_input == "tags":
            # pure tags, list them
            print(",".join(mt.list_tags()))
        else:
            print(user_input)
