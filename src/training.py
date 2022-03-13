
import data_cleaning
from markov_text import AssociationTable

def taow():
    with open("sample_text/taow.txt") as taow:
        text = taow.read()
    text_list = data_cleaning.clean_aow(text)
    markov = AssociationTable()
    markov.train(text_list)
    markov.update_probabilities()
    new_text = markov.gen_text(1000)
    print(new_text)

def unff():
    with open("sample_text/unff.txt") as taow:
        text = taow.read()
    text_list = data_cleaning.clean_aow(text)
    markov = AssociationTable()
    markov.train(text_list)
    markov.update_probabilities()
    new_text = markov.gen_text(300)
    print(new_text)

def main():
    unff()

if __name__ == "__main__":
    main()