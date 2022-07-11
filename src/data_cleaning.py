"""
I need better documentation
"""

import re
from markov_text import AssociationTable
from typing import List, Dict

def clean_aow(text : str) -> List[str]:
    """
    specifically for cleaning text from the Art of War by Sun Tsu
     - the Lionel Giles translation available through MIT classics
    """

    # Roman-numeric headers
    text = re.sub(r"\n+[IVXL]+\.+.+\n", "\n", text)
    # numeric headers
    text = re.sub(r"\n+[\d,]+\.+", "\n", text)
    # end of sentence punctuation
    text = re.sub(r":--|[\.\?!;]+", " . ", text)
    # end of phrase punctuation
    text = re.sub(r"--|[,:]+", " , ", text)
    # get rid of repeated spaces
    text = re.sub("[ \t\n]+", " ", text) # not raw regex
    # remove text in parentheses
    text = re.sub(r"\([^\)]+\)", "", text)
    # get rid of quotes
    text = re.sub(r"\"", r"", text)
    # fix capitalization
    text = text.lower()
    text = re.sub(" sun tzu ", " Sun Tzu ", text)
    text = re.sub(" yin ", " Yin ", text)
    text = re.sub(" chih ", " Chih ", text)
    text = re.sub(" i ", " I ", text)
    # double spaces for some reason
    text = re.sub("[ \t]+", " ", text) # not raw regex
    # make list
    text_list = text.split(" ")
    text_list = list(filter(lambda x: len(x) > 0, text_list))
    return text_list

def clean_motcp(text : str, names : Dict[str, str]) -> List[str]:
    """
    seems fun
    """

    # Roman-numeric headers
    text = re.sub(r"\n+[IVXL]+\.", "\n", text)
    # numeric headers
    text = re.sub(r"\n+[\d,]+\.+", "\n", text)
    # end of sentence punctuation
    text = re.sub(r"[\.\?!;]+", " . ", text)
    # end of phrase punctuation
    text = re.sub(r"--|[,:()]+", " , ", text)
    # remove text in parentheses
    text = re.sub(r"\([^\)]+\)", "", text)
    text = re.sub(r"\[[^\]]+\]", "", text)
    # get rid of odd marks
    text = re.sub(r"\"|\*|†|‡", r"", text)
    # fix capitalization
    text = text.lower()
    text = re.sub(" i ", " I ", text)
    # get rid of repeated spaces
    text = re.sub("[ \t\n]+", " ", text) # not raw regex

    for key, val in names.items():
        text = text.replace(" " + key, " " + val) 

    # make list
    text_list = text.split(" ")
    text_list = list(filter(lambda x: len(x) > 0, text_list))
    return text_list

def clean_tar(text : str) -> List[str]:
    """
    general cleaning rules
    I still get rid of quotation marks, but there's probably a better way to handle them
    """

    # end of sentence punctuation
    text = re.sub(r"[\.\?!;]+", " . ", text)
    # end of phrase punctuation
    text = re.sub(r"--|[,:()]+", " , ", text)
    # get rid of repeated spaces
    text = re.sub("[ \t\n]+", " ", text) # not raw regex
    # get rid of quotes
    text = re.sub(r"\"", r"", text)
    # fix capitalization
    text = text.lower()
    text = re.sub(" i ", " I ", text)
    text = re.sub(" i'", " I'", text)
    text = re.sub(" u \. s \. ", " U.S. ", text)
    
    text = re.sub("( \.)+", " .", text)
    text = re.sub("( ,)+", " ,", text)
    text = re.sub(" , \.", " .", text)

    # make list
    text_list = text.split(" ")
    text_list = list(filter(lambda x: len(x) > 0, text_list))
    return text_list

def clean_generic(text : str) -> List[str]:
    """
    general cleaning rules
    I still get rid of quotation marks, but there's probably a better way to handle them
    """

    # end of sentence punctuation
    text = re.sub(r"[\.\?!;]+", " . ", text)
    # end of phrase punctuation
    text = re.sub(r"--|[,:()]+", " , ", text)
    # get rid of repeated spaces
    text = re.sub("[ \t\n]+", " ", text) # not raw regex
    # get rid of quotes
    text = re.sub(r"\"", r"", text)
    # fix capitalization
    text = text.lower()
    text = re.sub(" i ", " I ", text)
    text = re.sub(" i'", " I'", text)
    # make list
    text_list = text.split(" ")
    text_list = list(filter(lambda x: len(x) > 0, text_list))
    return text_list

def find_id(name, ids_names, name_to_id_dict):
    for row in ids_names[1:]:
        id_val, new_name = row[0], row[1]
        if new_name == name:
            name_to_id_dict[name] = id_val
            return name_to_id_dict
    
    print(f"ERROR: couldn't find id for name {name}")
    return name_to_id_dict

def new_clean_discord(text : str, members = None):
    """
    more formatting rules. I'm definitely not using a scraper
    """

    lines = text.split("\n")
    lines_len = len(lines)
    newlines = []
    members_dict = {}
    for i in range(lines_len):
        line = lines[i]
        
        try:
            colon_idx = line.index(":")
        except ValueError:
            # expected to happen
            continue

        header = line[:colon_idx + 1]
        body = line[colon_idx + 1:]

        # remove #\d{4}
        header = re.sub(r"#\d{4}", "", header)
        if members is not None:
            name = header[:-1]
            if name not in members_dict:
                members_dict = find_id(name, members, members_dict)
            header = members_dict[name] + ":"

        body = body.lower()

        line = header + body
        newlines.append(line)

    text = "\n".join(newlines) + "\n"
    # end of sentence punctuation

    text = re.sub("\.+ ", " . ", text)
    text = re.sub("\?+ ", " ? ", text)
    text = re.sub("!+ ", " ! ", text)
    text = re.sub(r"\.+\n", " . \n", text)
    text = re.sub(r"\?+\n", " ? \n", text)
    text = re.sub(r"!+\n", " ! \n", text)
    # end of phrase punctuation
    text = re.sub(r"--|,+", " , ", text)

    # remove custom emoji
    text = re.sub(r"<:[-_\w^>]+:\d+>", "", text)

    # fix @ mentions
    text = re.sub(r"<@[!\&]\d{18}>", "@"+r"\g<0>" + "@", text)
    text = re.sub(r"(<@[!\&])|(>@)", "", text)

    # fix # mentions
    text = re.sub(r"<#\d{18}>", "#"+r"\g<0>" + "#", text)
    text = re.sub(r"(<#)|(>#)", "", text)
    
    text = re.sub("\n+", "\n", text)
    text = re.sub("\n", " \n ", text)

    text = re.sub("[ \t]+", " ", text)
    return text.split(" ")

def clean_discord(text : str):
    """
    this is gonna be a lot of lowercase
    """

    lines = text.split("\n")
    lines_len = len(lines)
    newlines = []
    for i in range(lines_len):
        line = lines[i]

        if line[0] != "[":
            # not message
            continue

        try:
            timestamp_end = line.index("]")
        except ValueError as e:
            print("unexpected line starting with \[ with out \]")
            continue

        line = line[timestamp_end + 2:]
        
        try:
            colon_idx = line.index(":")
        except ValueError:
            # expected to happen
            continue

        header = line[:colon_idx + 1]
        body = line[colon_idx + 1:]

        # remove timestamp in brackets
        header = re.sub(r"\[[^\]]+\]", "", header)
        # no spaces between parts of username
        header = re.sub(" ", "_", header)
        
        header = re.sub("[\.\?!,]+", "", header)

        body = body.lower()

        line = header + body
        newlines.append(line)

    text = "\n".join(newlines)
    # end of sentence punctuation
    text = re.sub(r"\.+", " . ", text)
    text = re.sub(r"\?+", " ? ", text)
    text = re.sub(r"!+", " ! ", text)
    # end of phrase punctuation
    text = re.sub(r"--|,+", " , ", text)
    
    text = re.sub("\n+", "\n", text)
    text = re.sub("\n", " \n ", text)

    text = re.sub("[ \t]+", " ", text)
    return text.split(" ")


def clean_script(text : str, names : Dict[str, str]) -> List[str]:
    # asterisks at end of lines
    text = re.sub(r"\*", "\n", text)
    # numeric headers
    text = re.sub(r"\n+[\d,]+\.+", "\n", text)

    text = re.sub(r"\n+", "\n ", text)
    lines = text.split("\n")
    lc = re.compile('[a-z]+')

    newlines = [" " + lines[0]]
    for line in lines[1:]:
        if line.isspace():
            continue
        prev_lowercase = list(lc.findall(newlines[-1]))
        lowercase = list(lc.findall(line))
        if bool(lowercase) == bool(prev_lowercase) and len(newlines[-1].split(" ")) > 2:
            newlines[-1] = newlines[-1] + line
        else:
            newlines.append(line)

    text = "\n".join(newlines)

    lines = text.split("\n")

    for i in range(len(lines)):
        text = lines[i]
        # get rid of quotes
        text = re.sub(r"\"", r"", text)

        lowercase = list(lc.findall(lines[i]))

        if lowercase:
            do_lower = True

            for j in range(len(text)):
                if do_lower:
                    text = text[:j] + text[j].lower() + text[j+1:]
                if text[j] == "(":
                    do_lower = False
                elif text[j] == ")":
                    do_lower = True
            
            # text = text.lower()
            # end of sentence punctuation
            text = re.sub(r"[\.\?!;]+", " .. ", text)
            # end of phrase punctuation
            text = re.sub(r"--|[,:]+", " ,, ", text)
            # in parentheses
            text = re.sub("\(", "( ", text)
            text = re.sub("\)", " )", text)
            # need to fix names
            for key, val in names.items():
                text = text.replace(" " + key, " " + val)
            text = re.sub(" i ", " I ", text)
        elif "(" not in text: 
            # end of sentence punctuation
            text = re.sub(r"[\.]+", " . ", text)
            # end of phrase punctuation
            text = re.sub(r"[,:]+", " , ", text)
        
        # get rid of repeated spaces
        lines[i] = text

    text = "\n".join(lines)

    text = re.sub("[ \t]+", " ", text) # not raw regex
    text = re.sub("\s\n+", "\n", text)
    text = re.sub("\n+\s", "\n", text)
    text = re.sub("\n\.", "\n", text)
    text = re.sub("\n", " \n ", text)

    text = re.sub("[ \t]+", " ", text) # not raw regex
    tokens = text.split(" ")
    tokens = list(filter(lambda x: len(x) > 0, tokens))
    return tokens
    
def clean_overheard(text : str) -> List[str]:
    text = re.sub('"', '', text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower()
    tokens = text.split(" ")
    tokens = list(filter(lambda x: len(x) > 0, tokens))
    return tokens