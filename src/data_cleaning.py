"""
I need better documentation
"""

import re
from markov_text import AssociationTable
from typing import List

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
    # make list
    text_list = text.split(" ")
    text_list = list(filter(lambda x: len(x) > 0, text_list))
    return text_list


