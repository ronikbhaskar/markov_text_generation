
from random import uniform, choice
from enum import Enum
import re

class ListEntry:   

    def __init__(self, word):
        """
        word : str or Syntax
        """

        self.word = word
        self.frequency = 1
        self.probability = 0

    def inc(self):
        """
        increment frequency
        """

        self.frequency += 1

    def dec(self):
        """
        decrement frequency
        don't think I'll need this
        """

        self.frequency -= 1

    def update_probability(self, total_occur : int):
        """
        total_occur : int - total occurrences of the preceding word
        """

        if not total_occur:
            printf("ERROR: update_probability: total_occur is 0")
            self.probability = 0
        else:
            self.probability = self.frequency / total_occur

class AssociationEntry:

    def __init__(self, word, next_word):
        """
        word : str or Syntax - word for AssociationEntry
        next_word : str or Syntax - first entry in list
        """

        self.word = word
        self.num_occurrences = 1
        self.assoc_list = {next_word : ListEntry(next_word)}
        self.recalculated_probabilities = False

    def add_word(self, word):
        """
        add word to assoc_list
        """

        self.num_occurrences += 1

        if word in self.assoc_list:
            self.assoc_list[word].inc()
        else:
            self.assoc_list[word] = ListEntry(word)

        self.recalculated_probabilities = False

    def update_probabilities(self):
        """
        slow, should only be run when done training model
        """

        if self.recalculated_probabilities:
            return

        for word in self.assoc_list:
            self.assoc_list[word].update_probability(self.num_occurrences)

        self.recalculated_probabilities = True

    def next_word(self):
        """
        generates random next word / Syntax 
        """

        if not self.recalculated_probabilities:
            print("ERROR: next_word: probabilities have not been recalculated")

        random_num = uniform(0, 1)

        for word, entry in self.assoc_list.items():
            if entry.probability > random_num:
                return word
            random_num -= entry.probability

        print("ERROR: unable to generate random word")
        return None

class AssociationTable:

    EOS = 1 # end of sentence
    EOP = 2 # end of phrase  

    SYNTAX_TABLE = {
        ".": EOS,
        ",": EOP
    }

    def __init__(self):
        """
        If you're reading this, hello
        """

        self.table = {}
        self.recalculated_probabilities = False
        self.words_analyzed = 0

    def add_word(self, word, next_word):
        """
        word : str or Syntax
        next_word : str or Syntax
        """

        self.words_analyzed += 1

        if word in self.table:
            self.table[word].add_word(next_word)
        else:
            self.table[word] = AssociationEntry(word, next_word)

        self.recalculated_probabilities = False

    def update_probabilities(self):
        """
        updates all probabilities in entries of table
        """

        if self.recalculated_probabilities:
            return

        for word in self.table:
            self.table[word].update_probabilities()

        self.recalculated_probabilities = True

    def capitalize(self, word):
        """
        capitalization for English
        """

        if len(word) == 0 or word == AssociationTable.EOS or word == AssociationTable.EOP:
            print(f"[{word}]")
            print("ERROR: bad word for capitalization")
        
        return word[0].upper() + word[1:]

    def get_syntax_translation(self, word):
        return AssociationTable.SYNTAX_TABLE.get(word, word)
    
    def gen_text(self, num_words : int, start = None, newline_prob = 0.3):
        """
        num_words : int
        start : word, not Syntax
        newline_prob : float, probability that end of sentence will result in newline
        generates that many words, Syntax not included
        """

        if start == AssociationTable.EOS or start == AssociationTable.EOP:
            print("ERROR: start is a Syntax, not word")

        if start == AssociationTable.EOS or start == AssociationTable.EOP or start == None or start not in self.table:
            for word in self.table:
                if word != AssociationTable.EOS and word != AssociationTable.EOP and word != "\n":
                    start = word
                    break
            else:
                print("ERROR: only AssociationTable.EOS and AssociationTable.EOP in model")
                return None

        prev_word = start

        out = self.capitalize(start)
        do_caps = False
        preceding_space = True
        did_newline = False
        delim = " "

        for _ in range(num_words):
            next_word = self.table[prev_word].next_word()
            prev_word = next_word
            if did_newline:
                delim = "\n\n"
            else:
                delim = " "
            did_newline = False

            if next_word == AssociationTable.EOS:
                next_word = "."
                did_newline = uniform(0,1) < newline_prob
                preceding_space = False
                do_caps = True
            elif next_word == AssociationTable.EOP:
                next_word = ","
                preceding_space = False
            elif next_word == "\n":
                preceding_space = False
                do_caps = True
            elif do_caps:
                next_word = self.capitalize(next_word)
                do_caps = False

            if preceding_space:
                out += delim
            
            out += next_word
            preceding_space = True

        return out

    def quick_output(self):
        """
        simple representation of model
        """

        for entry in self.table.values():
            print(" * " + str(entry.word))
            for word in entry.assoc_list:
                print("    + " + str(word))

    def train(self, training_text_list, cyclic = True):
        """
        list of words for training
        periods and commas are also separate
        """

        if len(training_text_list) == 0:
            print("ERROR: training text list is empty")
            return

        for word, next_word in zip(training_text_list[:-1], training_text_list[1:]):
            # inefficient change to pseudo enum
            if len(word) == 0 or len(next_word) == 0:
                continue

            word = self.get_syntax_translation(word)

            next_word = self.get_syntax_translation(next_word)

            self.add_word(word, next_word)

        if cyclic:
            word = self.get_syntax_translation(training_text_list[-1])
            next_word = self.get_syntax_translation(training_text_list[0])
            self.add_word(word, next_word)
