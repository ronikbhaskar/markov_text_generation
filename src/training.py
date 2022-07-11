
import csv
import re
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

def discord():
    with open("sample_text/discord/new_discord_format/in.txt", "r", encoding="UTF8") as f:
        text = f.read()

    with open("sample_text/discord/new_discord_format/member.csv", "r", encoding="UTF8") as f:
        members = list(csv.reader(f))

    with open("sample_text/discord/new_discord_format/channel.csv", "r", encoding="UTF8") as f:
        channels = list(csv.reader(f))

    with open("sample_text/discord/new_discord_format/role.csv", "r", encoding="UTF8") as f:
        roles = list(csv.reader(f))

    tokens = data_cleaning.new_clean_discord(text, members=members)

    formatting_rules = {
        ".": FormattingRule(1, ".", do_caps=False),
        ",": FormattingRule(2, ",", do_caps=False),
        "?": FormattingRule(3, "?", do_caps=False),
        "!": FormattingRule(4, "!", do_caps=False),
        "\n": FormattingRule(5, "\n", do_caps=False, preceding_space=False, is_delim=True)
    }

    markov = AssociationTable(formatting_rules=formatting_rules)
    markov.train(tokens)
    markov.update_probabilities()
    text = markov.gen_text(1000, caps_first=False)

    for id, _, disp_name in members:
        text = re.sub(id, disp_name, text)

    for id, disp_name in channels:
        text = re.sub(id, disp_name, text)

    for id, disp_name in roles:
        text = re.sub(id, disp_name, text)

    print(text)

def overheard():
    with open("sample_text/discord/overheard/formatted_overheard.txt") as oh:
        text = oh.read()

    formatting_rules = {
        ".": FormattingRule(1, ".", do_caps=False),
        ",": FormattingRule(2, ",", do_caps=False)
    }

    text_list = data_cleaning.clean_overheard(text)
    markov = AssociationTable(formatting_rules=formatting_rules)
    markov.train(text_list)
    markov.update_probabilities()
    new_text = markov.gen_text(1000, start="i", caps_first=False)
    print(new_text)

def main():
    overheard()

if __name__ == "__main__":
    main()