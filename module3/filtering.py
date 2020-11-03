"""Filter out stopwords for word cloud"""

import sys
import nltk
from nltk.corpus import stopwords

sw = stopwords.words("french")
sw += ["les", "plus", "cette", "fait", "faire", "être", "deux", "comme", "dont", "tout",
       "ils", "bien", "sans", "peut", "tous", "après", "ainsi", "donc", "cet", "sous",
       "celle", "entre", "encore", "toutes", "pendant", "moins", "dire", "cela", "non",
       "faut", "trois", "aussi", "dit", "avoir", "doit", "contre", "depuis", "autres",
       "van", "het", "autre", "jusqu", "ici", "intéresse", "ouvrir" , "l" , "lorsqu", "oui", "très",
       "tel", "elles", "enfin", "doivent", "afin", "assez", "jour", "car", "parce", "rien", "déjà", "quand", 
       "reste", "crois", "laquelle", "toute", 
       ]
sw = set(sw)


def filtering(year):
    path = f"{year}.txt"
    output = open(f"{year}_keywords.txt", "w", encoding="utf8")

    with open(path) as f:
        text = f.read()
        words = nltk.wordpunct_tokenize(text)
        kept = [w.lower() for w in words if len(
            w) > 2 and w.isalpha() and w.lower() not in sw]
        kept_string = " ".join(kept)
        output.write(kept_string)


if __name__ == '__main__':
    year = sys.argv[1]
    filtering(year)