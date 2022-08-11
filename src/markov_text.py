
from random import uniform, choice


class FormattingRule:

    def __init__(self, code, symbol, do_caps = True, 
                 preceding_space = False, is_delim = False, newline_prob = 0):
        """
        code : integer representation
        symbol : str
        do_caps : bool
        preceding_space : bool
        is_delim : bool
        newline_prob : float
        """

        self.code = code
        self.symbol = symbol
        self.do_caps = do_caps
        self.preceding_space = preceding_space
        self.is_delim = is_delim
        self.newline_prob = newline_prob

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
            print("ERROR: update_probability: total_occur is 0")
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

    GEN_FORMATTING_RULES = {
        ".": FormattingRule(1, "."),
        ",": FormattingRule(2, ",", do_caps=False)
    }

    def __init__(self, formatting_rules = GEN_FORMATTING_RULES):
        """
        If you're reading this, hello
        """

        self.table = {}
        self.recalculated_probabilities = False
        self.words_analyzed = 0
        self.formatting_rules = formatting_rules

    def combine(self, assoc_table):
        """
        assoc_table : AssociationTable
        Returns new AssociationTable with combined graphs from self and assoc_table
        does not modify self
        formatting rules of self take precedence over assoc_table
        """

        f_rules = {**assoc_table.formatting_rules, **self.formatting_rules}
        new_table = AssociationTable(formatting_rules=f_rules)

        for word, entry in self.table.items():
            for next_word, list_entry in entry.assoc_list.items():
                for _ in range(list_entry.frequency):
                    new_table.add_word(word, next_word)

        for word, entry in assoc_table.table.items():
            for next_word, list_entry in entry.assoc_list.items():
                for _ in range(list_entry.frequency):
                    new_table.add_word(word, next_word)

        return new_table


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

        if len(word) == 0:
            print(f"[{word}]")
            print("ERROR: bad word for capitalization")
        
        return word[0].upper() + word[1:]

    def get_formatting_translation(self, word):
        return self.formatting_rules.get(word, word)
    
    def gen_text(self, num_words : int, start = None, caps_first = True):
        """
        num_words : int
        start : word, not Syntax
        newline_prob : float, probability that end of sentence will result in newline
        generates that many words, Syntax not included
        """

        if start == None or start not in self.table:
            for word in self.table:
                if type(word) is not FormattingRule:
                    start = word
                    break
            else:
                print("ERROR: only FormattingRules in model")
                return None

        prev_word = start

        if caps_first:
            start = self.capitalize(start)
            
        out = start
        do_caps = False
        preceding_space = True
        did_delim = False
        delim = " "

        for _ in range(num_words):
            next_word = self.table[prev_word].next_word()
            prev_word = next_word
            if did_delim:
                delim = ""
            else:
                delim = " "
            did_delim = False

            next_word = self.get_formatting_translation(next_word)

            if type(next_word) is FormattingRule:
                did_delim = next_word.is_delim 
                preceding_space = next_word.preceding_space
                do_caps = next_word.do_caps
                add_newline = uniform(0,1) < next_word.newline_prob
                next_word = next_word.symbol
                if add_newline:
                    next_word += "\n"
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

            self.add_word(word, next_word)

        if cyclic:
            self.add_word(training_text_list[-1], training_text_list[0])