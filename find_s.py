from __future__ import division
import math
import os
import sys


# Reading the file (ToDO: Better way to remove the label spaces)
def read_file(filename):
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
        for val in s:
            temp = val.split(' ')
            temp_data.append(temp[1])
        training_data.append(temp_data)
    return training_data


def hardcode_print():
    # Size of the input space
    print pow(2, 9)

    # Size of the concept space
    concept = int(math.log10(pow(2, 512))) + 1
    print concept

    # Size of the hypothesis space
    print pow(3, 9) + 1

    # Size of the hypothesis space after adding a column
    print pow(3, 10) + 1

    # Size of the hypothesis space after modifying a column
    print (pow(3, 8) * 4) + 1


def find_s_train(df):
    # Initial hypothesis
    h = ["null", "null", "null", "null", "null", "null", "null", "null", "null"]

    if os.path.exists("partA6.txt"):
        os.remove("partA6.txt")

    count = 0
    file = open("partA6.txt", "a")
    for row in df:
        if(count != 0 and count % 20 == 0):
            file.write('\t'.join(h[0:9]) + '\n')

        num = 0
        if(row[9] == "Yes"):
            if h[0] == "null":
                h = row
            else:
                for attr in row:
                    if (attr == h[num] or h[num] == "?"):
                        num = num + 1
                    else:
                        h[num] = "?"
                        num = num + 1
        count = count + 1
    file.close()
    return h


def test_h(test):
    total = 0
    miscalc = 0
    for row in test:
        pred = ""
        num = 0
        for attr in row[0:9]:
            if (attr == h[num] or h[num] == "?"):
                pred = "Yes"
                num = num + 1
            else:
                pred = "No"
                num = num + 1
                break
        if (pred != row[9]):
            miscalc = miscalc + 1
        total = total + 1
    print miscalc / total


def input_file(input_data):
    for row in input_data:
        pred = ""
        num = 0
        for attr in row[0:9]:
            if (attr == h[num] or h[num] == "?"):
                pred = "Yes"
                num = num + 1
            else:
                pred = "No"
                num = num + 1
                break
        print pred


train = read_file('9Cat-Train.labeled')
hardcode_print()
h = find_s_train(train)
h = h[0:9]
test = read_file('9Cat-Dev.labeled')
test_h(test)
input_data = read_file(sys.argv[1])
input_file(input_data)
