
import data_cleaning
from markov_text import AssociationTable, FormattingRule

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
    new_text = markov.gen_text(500)
    print(new_text)

def himym():
    names = {
        "ted": "Ted",
        "marshall": "Marshall",
        "ranjit": "Ranjit",
        "robin": "Robin",
        "barney": "Barney",
        "i'm": "I'm",
        "i'll": "I'll"
    }
    with open("sample_text/himym_pilot.txt") as himym:
        text = himym.read()
    tokens = data_cleaning.clean_script(text, names)
    formatting_rules = {
        ".": FormattingRule(1, "."),
        ",": FormattingRule(2, ",", do_caps=False),
        "(": FormattingRule(3, "(", do_caps=False, preceding_space=True, is_delim=True),
        ")": FormattingRule(4, ")", do_caps=False),
        "\n": FormattingRule(5, "\n", is_delim=True),
        "..": FormattingRule(6, "."),
        ",,": FormattingRule(7, ",", do_caps=False),
    }
    markov = AssociationTable(formatting_rules=formatting_rules)
    markov.train(tokens)
    markov.update_probabilities()
    print(markov.gen_text(3000))

def motcm():
    with open("sample_text/motcp.txt") as motcp:
        text = motcp.read()
    
    propers = [
        "Europe", 
        "European",
        "Pope","Tsar", "Parliament",
        "Metternich", "Ledru-Rollin", "Engels", "Louis", "Blanc", "Charles", "Fourier", 
        "Guizot", "French", "Radicals", "German",
        "English", "French", "German", "Italian", "Flemish", "Danish",
        "Communist","Communism", "Réformist", "Chartist",
        "America", "Cape", "Italy", "France", "Switzerland", "Poland", "Germany", 
    ]
    names = {name.lower() : name for name in propers}

    formatting_rules = {
        ".": FormattingRule(1, ".", newline_prob=0.2),
        ",": FormattingRule(2, ",", do_caps=False)
    }
    tokens = data_cleaning.clean_motcp(text, names)
    markov = AssociationTable(formatting_rules=formatting_rules)
    markov.train(tokens)
    markov.update_probabilities()
    print(markov.gen_text(4000))

def tar():
    with open("sample_text/tar.txt") as tar:
        text = tar.read()

    formatting_rules = {
        ".": FormattingRule(1, ".", newline_prob=0.3),
        ",": FormattingRule(2, ",", do_caps=False)
    }
    tokens = data_cleaning.clean_tar(text)
    markov = AssociationTable(formatting_rules=formatting_rules)
    markov.train(tokens)
    markov.update_probabilities()
    print(markov.gen_text(4000))

def main():
    tar()

if __name__ == "__main__":
    main()