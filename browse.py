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

def printHelp():
    print("""
    
    tags: search for tags
    quit: quit
    help: get help
    """)

if __name__=="__main__":
    BrowserCompleter = NestedCompleter.from_nested_dict({'help': None, 'quit':None, 'tags':None}, ignore_case=True)

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
        else:
            print(user_input)
