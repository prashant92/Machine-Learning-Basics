import itertools
import sys


# Reading the file (ToDO: Better way to remove the label spaces)
def read_training_file(filename):
    f = open(filename, 'r')
    df = f.read()
    data = []
    training_data = []
    data = df.split("\n")
    for row in data:
        temp_data = []
        if(len(row) < 1):
            continue
        s = row.split("\t")
        # print(s, "\n\n")
        for val in s:
            temp = val.split(' ')
            temp_data.append(temp[1])
        training_data.append(temp_data)
    return training_data


def hardcode_print():
    # Size of the input space
    print pow(2, 4)

    # Size of the concept space
    print pow(2, pow(2, 4))


def list_then_eliminate(possible_functions, possible_inputs):

    pfcopy = list(possible_functions)
    for row in train_data:
        inp = row[0:4]
        out = row[4].rstrip()
        for index in range(0, 16):
            if inp == possible_inputs[index]:
                for hyp in possible_functions:
                    if ((out == "Yes" and hyp[index] == "0") or (out == "No" and hyp[index] == "1")):
                        pfcopy.remove(hyp)
        possible_functions = list(pfcopy)
    print len(possible_functions)

    return possible_functions


hardcode_print()
train_data = read_training_file("4Cat-Train.labeled")

attr = [["Young", "Old"], ["1", "3"], ["Southampton", "Queenstown"], ["Male", "Female"]]
tuple_inputs = list(itertools.product(*attr))
possible_inputs = [list(elem) for elem in tuple_inputs]
possible_functions = list(itertools.product("01", repeat=16))

version_space = list_then_eliminate(possible_functions, possible_inputs)

test_data = read_training_file(sys.argv[1])

for row in test_data:
    correct = 0
    incorrect = 0
    inp = row[0:4]
    for index in range(0, 16):
        if inp == possible_inputs[index]:
            for hyp in version_space:
                if (hyp[index] == "1"):
                    correct = correct + 1
                else:
                    incorrect = incorrect + 1

    print correct, " ", incorrect
