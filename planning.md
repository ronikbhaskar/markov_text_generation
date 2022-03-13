

## cleaning.py

clean_text - clean the text
 - lowercase
 - separate out periods/exclamations/question marks and commas
 - remove other punctuation

word_pairs - return generator to getting the next word and the word after

## markov_text.py

## Classes

ListEntry
 - word : string or some syntactical idea
 - frequency : int
 - probability : float
 - methods
    - increment - increments frequency
    - update_probability(total_occurrences) - change probability to frequency / total_occurrences

AssociationEntry
 - word : associated word or some syntactical idea 
 - num_occurences : int
 - assoc_list : list of ListEntry
 - methods
    - add_word(word) - either increment the associated word or add a new entry
    - update_probabilities - iterate through list and call update_probability on them all
    - next_word - generate random next word

MarkovModel
 - table : AssociationTable
    - table of {word : AssociationEntry}
 - recalculated_probabilities : bool
 - methods
    - update_probabilities - iterate through list and call update_probabilities on them all, change recalc_prob to True
    - add_word(word, next_word) - update entry or create entry

