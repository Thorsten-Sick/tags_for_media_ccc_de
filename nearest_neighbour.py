#!/usr/bin/env python3

# Nearest neighbour AI code

# Idea: Text in, Feature selection. After DB is built: Nearest N talks can be found

# https://scikit-learn.org/stable/modules/feature_selection.html

class NN():
    def __init__(self):
        pass

    def _normalize(self, guid, event, title, subtitle, abstract, description, track, person_ids):
        pass

    def add_talk(self, guid, event, title="", subtitle="", abstract="", description="", track="", person_ids=None):
        """
        Add a talk item to the training data

        :param guid: guid of the talk
        :param event: event where the talk was ("36c3", for example)
        :param title: title of the talk
        :param subtitle: subtitle of the talk (from subtitles during the talk)
        :param abstract: abstract of the talk
        :param description: description of the talk
        :param track: track the talk was in
        :param person_ids: a list of person ids presenting
        :return:
        """
        # TODO: Maybe extend the person ids with person names

        if not person_ids:
            person_ids = []
        pass
        # TODO: Text processing

    def train(self):
        pass
        # TODO: Feature selection
        # https://scikit-learn.org/stable/modules/feature_extraction.html#loading-features-from-dicts

    def find_nn(self, n):
        """

        :param n: number of nearest neighbours to find
        :return:
        """
        pass
        # TODO: NN code

if __name__ == "__main__":
    pass

    nn = NN()
    # TODO: Add values to these variables
    guid = None
    title = None
    subtitle = None
    abstract = None
    description = None
    track = None
    person_ids = None
    nn.add_text(guid, title, subtitle, abstract, description, track, person_ids)