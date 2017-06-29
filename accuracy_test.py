"""Test the accuracy of the emotion tagging."""
import app
import pandas as pd
import numpy as np


test_file = "./accuracy_data/Ragazzo da parete - cap 1 e 2.txt"
mapping = {'rabbia': 0, 'anticipazione': 1, 'disgusto': 2,
           'paura': 3, 'gioia': 4, 'tristezza': 5,
           'sorpresa': 6, 'fiducia': 7}
emo_names = ['rabbia', 'anticipazione', 'disgusto', 'paura', 'gioia',
             'tristezza', 'sorpresa', 'fiducia']


def workflow():
    result_auto = analyze_file(test_file)
    sent_auto = result_auto['sentences']
    emo_auto = transpose_list(sent_auto)

    sent_human = load_human()
    emo_human = transpose_list(sent_human)

    res = [compare_series(h, a) for h, a in zip(emo_human, emo_auto)]

    for i in range(len(res)):
        equals, diff = res[i]
        percent_equals = sum(equals) / len(equals)
        print("Emozione: {}, accuratezza: {:.2f}%".format(emo_names[i],
                                                          percent_equals * 100)
              )

    return res


def transpose_list(l):
    return np.transpose(np.array(l)).tolist()


def load_human(filepath="./accuracy_data/Ragazzo da parete - taggato.csv"):
    df = pd.read_csv(filepath)
    return df.values[:, 1:].tolist()


def analyze_file(file_path=test_file):
    """Analyze the text in the file and get results."""
    with open(file_path, 'r') as f:
        text = f.read()

    result = app._analyze(text, also_get_sents=True)

    return result


def go(sent, start=0):
    i = start
    cont = True
    while i < len(sent) and cont:
        print("\n\nFrase {}".format(i))
        print(" ".join(sent[i]) + "\n")
        user_choice = input("Continua: [y]/n -> ")
        if user_choice == 'y' or user_choice == "":
            i = i + 1
        else:
            cont = False


def compare_series(human, auto):
    """Compare the human annotated series with syuzhet's one.

    Parameters
    ----------
    human: List[int]
        list of int, human[i] is the value of series in sentence i
        annotated by humans

    auto: List[int]
        list of int, auto[i] is the value of series in sentence i
        computed by syuzhet

    Returns
    -------
    result: List[bool]
        result[i] is True iff bool(human[i]) == bool(auto[i])
    """
    if len(human) != len(auto):
        raise ValueError("Different lenght of input")

    human_bool = map(bool, human)
    auto_bool = map(bool, auto)
    diff = list(map(xor, human_bool, auto_bool))
    equals = list(map((lambda x: not x), diff))

    return equals, diff


def xor(a, b):
    return (a and (not b)) or ((not a) and b)
