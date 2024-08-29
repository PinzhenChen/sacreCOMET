import csv
import itertools
import sys


import numpy as np
import scipy.stats

##Note: should we scale DA or COMET in the same range? 
# 14 systems for de-en?
# MAE by system? 

def read_tsv(path):
    #For calculating MAE and kendaltau-c
    da_score, comet_score = [], []
    with open(path, "r") as fin:
        csv_reader = csv.DictReader(fin, delimiter='\t')

        for row in csv_reader:
            da_score.append(float(row["score"]))
            comet_score.append(float(row["comet_score"]))

    #scale the comet to [0, 100]
    return 100*np.array(comet_score), np.array(da_score)


def read_tsv_for_pairwise_accuracy(path):
    #Read the .tsv file and create a dict 
    # which key: system; value: np.array([[comet, da], ..])
    comet_da_bySystem = {}
    with open(path, "r") as fin:
        csv_reader = csv.DictReader(fin, delimiter="\t")
        
        for row in csv_reader:
            sys = row["system"]
            da_score = float(row["score"])
            comet_score = float(row["comet_score"])

            if sys not in comet_da_bySystem:
                comet_da_bySystem[sys] = [[comet_score, da_score]]
            else:
                comet_da_bySystem[sys].append([comet_score, da_score])

    for sys in comet_da_bySystem.keys():
        comet_da_bySystem[sys] = np.array(comet_da_bySystem[sys])

    return comet_da_bySystem


def MAE(y_pred, y):
    return np.average(np.abs(y_pred-y))

def kendalltau(y_pred, y):
    return scipy.stats.kendalltau(y, y_pred, variant='c')

def pairwise_accuracy(comet_da_bySystem, macro=True):
    # Give a language pair 
    #  each system refer to each particated system outputs
    #  Each precision reprt a new metric

    match, n_instances = 0, 0
    systems = [s for s in comet_da_bySystem.keys()]

    for pair in itertools.product(systems, systems):
        if pair[0] == pair[1]:
            continue

        sys1 = comet_da_bySystem[pair[0]]
        sys2 = comet_da_bySystem[pair[1]]
        assert sys1.size == sys2.size

        if macro is True:
            #Kocmi et. al 2021 uses the macro version
            sign_metric = (np.mean(sys1[:,0]) > np.mean(sys2[:,0]))
            sign_da = (np.mean(sys1[:,1]) > np.mean(sys2[:,1]))

            match += (sign_metric == sign_da)
            n_instances += 1
        else:
            _match = ((sys1[:,0] > sys2[:,0]) == (sys1[:,1] > sys2[:,1]))
            match += _match.sum()
            n_instances += _match.size

    return match / n_instances


if __name__ == "__main__":
    inFile = sys.argv[1] #e.g. output.de-en.float16_gpu1.comet_segment_score.tsv

    comet_score, da_score = read_tsv(inFile)
    print(MAE(comet_score, da_score))
    print(kendalltau(comet_score, da_score))
    print(pairwise_accuracy(read_tsv_for_pairwise_accuracy(inFile)))

