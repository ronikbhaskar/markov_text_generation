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
    
        



