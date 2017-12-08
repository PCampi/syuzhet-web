# """Test the accuracy of the emotion tagging."""
# import app
# import pandas as pd
# import numpy as np


# test_file = "./accuracy_data/Ragazzo da parete - cap 1 e 2.txt"
# mapping = {'rabbia': 0, 'anticipazione': 1, 'disgusto': 2,
#            'paura': 3, 'gioia': 4, 'tristezza': 5,
#            'sorpresa': 6, 'fiducia': 7}
# emo_names = ['rabbia', 'anticipazione', 'disgusto', 'paura', 'gioia',
#              'tristezza', 'sorpresa', 'fiducia']


# def acc(human, machine):
#     if len(human) != len(machine):
#         raise Exception("Lengths different!")

#     n = len(human)
#     ok_vec = [0, 0, 0, 0, 0, 0, 0, 0]
#     null_count = [0, 0, 0, 0, 0, 0, 0, 0]

#     for i in range(n):
#         h = human[i]
#         m = machine[i]
#         if len(h) != len(m):
#             raise Exception("Subdata lengths differ!!!")

#         for j in range(len(h)):
#             if h[j] == 0 and m[j] == 0:
#                 null_count[j] += 1
#             if h[j] > 0 and m[j] > 0:
#                 ok_vec[j] += 1

#     accuracy = [ok/(n - nulls) for ok, nulls in zip(ok_vec, null_count)]
#     return accuracy, ok_vec, null_count


# def accuracy_keep_zeros(human, machine):
#     if len(human) != len(machine):
#         raise Exception("Lengths different!")

#     n = len(human)
#     ok_vec = [0, 0, 0, 0, 0, 0, 0, 0]

#     for i in range(n):
#         h = human[i]
#         m = machine[i]
#         if len(h) != len(m):
#             raise Exception("Subdata lengths differ!!!")

#         for j in range(len(h)):
#             if (h[j] > 0 and m[j] > 0) or (h[j] == 0 and m[j] == 0):
#                 ok_vec[j] = ok_vec[j] + 1

#     accuracy = [ok / n for ok in ok_vec]

#     return ok_vec, accuracy


# def transpose_list(l):
#     return np.transpose(np.array(l)).tolist()


# def analyze_file(lex_version, file_path=test_file):
#     """Analyze the text in the file and get results."""
#     if lex_version != 'base' and lex_version != 'enhanced':
#         raise Exception("Unknown lexicon version: accepted values are " +
#                         "``base`` and ``enhanced``")

#     with open(file_path, 'r') as f:
#         text = f.read()

#     result = app._analyze(text, sent_list=True, sent_strs=True,
#                           lex_version=lex_version)

#     return result


# def go(sent, emotions, start=0):
#     i = start
#     cont = True
#     while i < len(sent) and cont:
#         print("\n\nFrase {}".format(i))
#         print(sent[i] + "\n")
#         curr_emos = emotions[i]
#         emos = ""
#         j = 0
#         for j in range(len(curr_emos)):
#             if curr_emos[j] > 0:
#                 emos = emos + emo_names[j] + " "
#         print(emos)
#         user_choice = input("Continua: [y]/n -> ")
#         if user_choice == 'y' or user_choice == "":
#             i = i + 1
#         else:
#             cont = False


# def go_to_sentence(sentences, index):
#     if index >= 0 and index < len(sentences):
#         print(sentences[index] + '\n')
#     else:
#         raise ValueError("Index out of bounds: {}".format(index))


# def compare_series(human, auto):
#     """Compare the human annotated series with syuzhet's one.

#     Parameters
#     ----------
#     human: List[int]
#         list of int, human[i] is the value of series in sentence i
#         annotated by humans

#     auto: List[int]
#         list of int, auto[i] is the value of series in sentence i
#         computed by syuzhet

#     Returns
#     -------
#     result: List[bool]
#         result[i] is True iff bool(human[i]) == bool(auto[i])
#     """
#     if len(human) != len(auto):
#         raise ValueError("Different lenght of input")

#     human_bool = map(bool, human)
#     auto_bool = map(bool, auto)
#     diff = list(map(xor, human_bool, auto_bool))
#     equals = list(map((lambda x: not x), diff))

#     return equals, diff


# def xor(a, b):
#     return (a and (not b)) or ((not a) and b)
