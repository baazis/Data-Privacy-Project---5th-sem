"""
run algorithm with given parameters
"""

# !/usr/bin/env python
# coding=utf-8
from algorithm import algorithm
from utils.read_adult_data import read_data as read_adult
from utils.read_informs_data import read_data as read_informs
import sys, copy, random

DATA_SELECT = 'a'
RELAX = False
INTUITIVE_ORDER = None


def write_to_file(result):
    """
    write the anonymized result to anonymized.data
    """
    with open("data/anonymized.data", "w") as output:
        for r in result:
            output.write(';'.join(r) + '\n')


def get_result_one(data, k=10):
    """
    run algorithm for one time, with k=10
    """
    print("K=%d" % k)
    data_back = copy.deepcopy(data)
    result, eval_result = algorithm(data, k, RELAX)
    # Convert numerical values back to categorical values if necessary
    if DATA_SELECT == 'a':
        result = covert_to_raw(result)
    else:
        for r in result:
            r[-1] = ','.join(r[-1])
    # write to anonymized.out file all the result using write_to_file function
    write_to_file(result)
    data = copy.deepcopy(data_back)
    print("NCP %0.2f" % eval_result[0] + "%")
    print("Running time %0.2f" % eval_result[1] + " seconds")



# this data  is finalizing the anonymized result
def get_result_k(data):
    """
    change k, while fixing QD and size of data set
    """
    data_back = copy.deepcopy(data)
    for k in range(5, 105, 5):
        print('#' * 30)
        print("K=%d" % k)
        result, eval_result = algorithm(data, k, RELAX)
        if DATA_SELECT == 'a':
            result = covert_to_raw(result)
        data = copy.deepcopy(data_back)
        print("NCP %0.2f" % eval_result[0] + "%")
        print("Running time %0.2f" % eval_result[1] + " seconds")




def covert_to_raw(result, connect_str='~'):
    """
    During preprocessing, categorical attributes are covert to
    numeric attribute using intuitive order. This function will covert
    these values back to they raw values. For example, Female and Male
    may be converted to 0 and 1 during anonymizaiton. Then we need to transform
    them back to original values after anonymization.
    """
    covert_result = []
    qi_len = len(INTUITIVE_ORDER)
    for record in result:
        covert_record = []
        for i in range(qi_len):
            if len(INTUITIVE_ORDER[i]) > 0:
                vtemp = ''
                if connect_str in record[i]:
                    temp = record[i].split(connect_str)
                    raw_list = []
                    for j in range(int(temp[0]), int(temp[1]) + 1):
                        raw_list.append(INTUITIVE_ORDER[i][j])
                    vtemp = connect_str.join(raw_list)
                else:
                    vtemp = INTUITIVE_ORDER[i][int(record[i])]
                covert_record.append(vtemp)
            else:
                covert_record.append(record[i])
        if isinstance(record[-1], str):
            covert_result.append(covert_record + [record[-1]])
        else:
            covert_result.append(covert_record + [connect_str.join(record[-1])])
    return covert_result


if __name__ == '__main__':
    K_VALUE = ''
    LEN_ARGV = len(sys.argv)
    try:
        MODEL = sys.argv[1]
        DATA_SELECT = sys.argv[2]
    except IndexError:
        MODEL = 's'
        DATA_SELECT = 'a'
    INPUT_K = 10
    # read record
    if MODEL == 's':
        RELAX = False
    else:
        RELAX = True
    if RELAX:
        print("Relax State")
    else:
        print("Strict State")
    if DATA_SELECT == 'i':
        print("Institute for Operations Research and the Management Sciences data")
        DATA = read_informs()
    else:
        print("Adult data from UCI Machine Learning Observatory")
        # INTUITIVE_ORDER is an intuitive order for
        # categorical attributes. This order is produced
        # by the reading (from data set) order.
        DATA, INTUITIVE_ORDER = read_adult()
        print(INTUITIVE_ORDER)
    if LEN_ARGV > 3:
        K_VALUE = sys.argv[3]
    if K_VALUE == 'k':
        get_result_k(DATA)
    
    elif K_VALUE == '':
        get_result_one(DATA)
    else:
        try:
            INPUT_K = int(K_VALUE)
            get_result_one(DATA, INPUT_K)
        except ValueError:
            print("Usage: python anonymizer [r|s] [a | i] [k | qi | data]")
            print("r: relax algorithm, s: strict algorithm")
            print("a: adult dataset, i: INFORMS dataset")
            print("k: varying k")
    # anonymized dataset is stored in result
    print("Finish algorithm!! Anonymized dataset formed")
