from __future__ import division
import math
import sys
import numpy as np

# Code to implement ID3 decision trees from scratch

# Create a Binary tree object
class BinaryTree():
    def __init__(self):
        self.pos = {}
        self.neg = {}
        self.split = {}
        self.columnName = None

    def test(self, row, titles):
        titles = np.asarray(titles)
        attr = row[np.where(titles == self.columnName)][0]
        if self.split[attr] is None:
            if self.pos[attr] > self.neg[attr]:
                return "+"
            else:
                return "-"
        else:
            return self.split[row[np.where(titles == self.columnName)][0]].test(row, titles)


def read_file(filepath):
    return np.loadtxt(open(filepath, "rb"), delimiter=",", dtype=object)


def label_entropy(total, pos, neg):
    ppos = pos / total
    pneg = neg / total
    if ppos == 0 or pneg == 0:
        return 0.0
    else:
        return -1 * (ppos * math.log(ppos, 2) + pneg * math.log(pneg, 2))


# Calculate the information gain
def info_gain(labelentropy, cc_pos_pos, cc_pos_neg, cc_neg_pos, cc_neg_neg):
    pppos = cc_pos_pos / (cc_pos_pos + cc_pos_neg)
    pnpos = cc_neg_pos / (cc_neg_pos + cc_neg_neg)
    total = cc_pos_pos + cc_pos_neg + cc_neg_pos + cc_neg_neg

    if pppos == 0 or pppos == 1:
        entropy = 0
    else:
        entropy = ((cc_pos_pos + cc_pos_neg) / total) * (pppos * math.log(pppos, 2) + (1 - pppos) * math.log((1 - pppos), 2)) * -1
    if pnpos == 0 or pnpos == 1:
        entropy2 = 0
    else:
        entropy2 = ((cc_neg_pos + cc_neg_neg) / total) * (pnpos * math.log(pnpos, 2) + (1 - pnpos) * math.log((1 - pnpos), 2)) * -1
    info_gain = labelentropy - entropy - entropy2
    return info_gain


def subset(data, feat, index):
    ndata = data[np.where(data[0:, index] == feat)]
    identifier = set(list(ndata[:, index]))
    ndata = np.delete(ndata, index, axis=1)
    return ndata, list(identifier)[0]


def train_stump(data, titles, depth):
    if depth >= 2:
        return
    tree = BinaryTree()
    labels = data[:, -1]
    bin_out = list(set(labels))
    poslist = ["A", "yes", "democrat"]
    neglist = ["notA", "no", "republican"]
    if bin_out[0] in poslist:
        posvar = bin_out[0]
        negvar = neglist[poslist.index(bin_out[0])]
    else:
        posvar = poslist[neglist.index(bin_out[0])]
        negvar = bin_out[0]

    count_yes = list(labels).count(posvar)
    count_no = len(labels) - count_yes
    len(labels) - count_no
    labelentropy = label_entropy(len(labels), count_yes, count_no)
    if labelentropy == 0.0:
        return
    info = []
    for j in range(0, len(titles) - 1):
        feats = []
        feats = data[0:, j]
        bin_feat = list(set(feats))

        cc_pos_pos = 0
        cc_pos_neg = 0
        cc_neg_pos = 0
        cc_neg_neg = 0
        for x in range(0, len(labels)):
            if feats[x] == bin_feat[0] and labels[x] == negvar:
                cc_pos_neg += 1
            elif feats[x] == bin_feat[0] and labels[x] == posvar:
                cc_pos_pos += 1
            elif feats[x] == bin_feat[1] and labels[x] == negvar:
                cc_neg_neg += 1
            elif feats[x] == bin_feat[1] and labels[x] == posvar:
                cc_neg_pos += 1
        info.append(info_gain(labelentropy, cc_pos_pos, cc_pos_neg, cc_neg_pos, cc_neg_neg))
    if max(info) < 0.1:
        return

    max_feat = list(set(data[0:, info.index(max(info))]))
    data1, identifier1 = subset(data, max_feat[0], info.index(max(info)))
    tree.columnName = titles[info.index(max(info))]
    tree.pos[max_feat[0]] = list(data1[:, -1]).count(posvar)
    tree.neg[max_feat[0]] = list(data1[:, -1]).count(negvar)
    extra = ""
    for x in range(0, depth):
        extra += "| "
    print '{4}{0} = {1}: [{2}+/{3}-]'.format(tree.columnName, identifier1, tree.pos[max_feat[0]], tree.neg[max_feat[0]], extra)
    tree.split[max_feat[0]] = train_stump(data1, np.delete(titles, info.index(max(info))), depth + 1)
    data2, identifier2 = subset(data, max_feat[1], info.index(max(info)))
    tree.pos[max_feat[1]] = list(data2[:, -1]).count(posvar)
    tree.neg[max_feat[1]] = list(data2[:, -1]).count(negvar)
    print '{4}{0} = {1}: [{2}+/{3}-]'.format(tree.columnName, identifier2, tree.pos[max_feat[1]], tree.neg[max_feat[1]], extra)
    tree.split[max_feat[1]] = train_stump(data2, np.delete(titles, info.index(max(info))), depth + 1)
    return tree


depth = 0
data = read_file(sys.argv[1])
titles = data[0]
titles = map(str.strip, titles)
data = data[1:]
labels = data[:, -1]
bin_out = list(set(labels))
poslist = ["A", "yes", "democrat"]
neglist = ["notA", "no", "republican"]
if bin_out[0] in poslist:
    posvar = bin_out[0]
    negvar = neglist[poslist.index(bin_out[0])]
else:
    posvar = poslist[neglist.index(bin_out[0])]
    negvar = bin_out[0]

count_no = list(labels).count(negvar)
count_yes = len(labels) - count_no
print '[{0}+/{1}-]'.format(count_yes, count_no)
tree = train_stump(data, titles, depth)
correct = 0
wrong = 0
for row in data:
    if row[-1:] == posvar and tree.test(row, titles) == "+":
        correct += 1
    elif row[-1:] == negvar and tree.test(row, titles) == "-":
        correct += 1
    else:
        wrong += 1
print "error(train): ", wrong / (correct + wrong)

# Testing the dtree
ndata = read_file(sys.argv[2])
ndata = ndata[1:]
correct = 0
wrong = 0
for row in ndata:
    if row[-1:] == posvar and tree.test(row, titles) == "+":
        correct += 1
    elif row[-1:] == negvar and tree.test(row, titles) == "-":
        correct += 1
    else:
        wrong += 1
print "error(test): ", wrong / (correct + wrong)
