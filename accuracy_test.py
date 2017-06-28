"""Test the accuracy of the emotion tagging."""
import app

test_file = "./test_data/Ragazzo da parete - cap 1 e 2.txt"


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
        print("Frase {}".format(i))
        print(" ".join(sent[i]) + "\n")
        user_choice = input("Continua: [y]/n -> ")
        if user_choice == 'y' or user_choice == "":
            i = i + 1
        else:
            cont = False
