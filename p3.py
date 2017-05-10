''' Python script to implement P3 of Python Learning Program
    And some unittests for it (at the end of the file) '''

import unittest
import copy
from os import fsync

def my_sort(input_f, output_f):
    ''' Sorting algorithm for P3 '''
    dict_list = read_file(input_f)
    dict_order = dict_sort_order(dict_list)
    write_file(dict_order, output_f)
    return dict_order

def read_file(filepath):
    ''' read file and return the dictionaries within it in a list '''
    # list of all dictionaries found in file, which will be returned
    dictionaries = []
    # because we read one line at a time,
    # we are adding key-value pairs in a (temp) dictionary and
    # only after we read newline will we add the (temp) dictionary to list of dictionaries
    current_dictionary = {}
    with open(filepath, 'r') as fpointer:
        for line in fpointer:
            # strip endline (but but linux has only \n ...)
            line = line.rstrip("\r\n")
            # stackoverflow tells me that '==' uses __cmp__ while 'is' checks address
            if line != '':
                # there should be 2 values: the key and the pair
                lines = line.split(' ')
                # adding the same key cases a KeyError exception to be thrown,
                # so we check for that case
                if len(lines) > 1 and (lines[0] not in current_dictionary):
                    current_dictionary[lines[0]] = lines[1]
                    #print "key {} has value {}".format(lines[0], current_dictionary[lines[0]])
            # if we read a newline, then the temp dictionary is ready
            # to be added to the list of dictionaries
            elif current_dictionary != {}:
                #print "end of dictionary!"
                dictionaries.append(current_dictionary)
                current_dictionary = {}
        # append last dictionary, if it exists (i.e. no endline at end of input file)
        if current_dictionary != {}:
            dictionaries.append(current_dictionary)
    return dictionaries

def dict_sort_order(dict_list):
    ''' actually sort the dictionary list
        meaning, provide an order in the result list
        it probably needs improvement '''
    result = []
    # make a copy to not modify the passed param/arg
    copy_dict_list = copy.deepcopy(dict_list)
    # while there are items in the copy, keep removing items from it
    while copy_dict_list != []:
        # find minimum
        idx, item = min_dict(copy_dict_list)
        #print "found minimum: ", item
        # put in the result the index from the original list
        result.append(dict_list.index(item))
        # remove that minimum
        del copy_dict_list[idx]

    return result

def write_file(dict_list, filepath):
    ''' write the provided sorted order in the provided filepath '''
    #print "writing to file: ", dict_list
    # open file in writemode - probably need to make sure the file exists
    # and create it if it doesn't exist
    with open(filepath, 'w') as fpointer:
        for dict_idx in dict_list:
            fpointer.write(str(dict_idx) + '\n')
        fpointer.flush()
        # make sure the filesystem contains the written stuff
        fsync(fpointer)

def min_dict(dict_list):
    ''' find the minimum of the dictionaries '''
    #return the index of the minimum
    min_idx = None
    #return the minimum
    minimum = None
    # check types before iterating
    if isinstance(dict_list, (list, tuple)):
        for idx, item in enumerate(dict_list):
            # check if there is a dictionary,
            # that we don't have the first minimum (first element of dictionary,
            # that the item is less than our minimum so far
            if isinstance(item, dict) and ((min_idx is None) or (dict_less_than(item, minimum))):
                min_idx = idx
                minimum = item
    return (min_idx, minimum)


def dict_less_than(dict_a, dict_b):
    ''' the comparison operation for two dicts
        there's a sort here as well: for the keys
        there's an assumption that the keys are the same
        between dict_a and dict_b '''
    # result is undefined at start
    result = None

    # get the keys, we compare through these
    keys_a = dict_a.keys()
    keys_b = dict_b.keys()

    while result is None and keys_a != [] and keys_b != []:
        # setup some variables: the lowest key and its value
        # for each dictionary
        min_a = min(keys_a)
        min_b = min(keys_b)

        value_a = dict_a[min_a]
        value_b = dict_b[min_b]

        if value_a > value_b:
            result = False
            #print "{0} is greater than {1}".format(value_a, value_b)
        elif value_a < value_b:
            result = True
            #print "{0} is less than {1}".format(value_a, value_b)
        #if the values are equal, we check next keys in the dictionaries (result still None)
        elif value_a == value_b:
            # remove minimums from the keys, so min will take the next minimum,
            # which is greater than this minimum
            keys_a.remove(min_a)
            keys_b.remove(min_b)
            #print "{0} is equal to {1}".format(value_a, value_b)
    if result is None:
        result = False
    return result

class SortTest(unittest.TestCase):
    ''' class to test the my_sort function'''
    def test_sortsimple(self):
        ''' test sorting an empty dictionary '''
        exp = [2, 1, 0]
        input_f = 'dictionaries.in'
        output_f = 'dictionaries.out'
        self.assertListEqual(my_sort(input_f, output_f), exp, "test sorting an empty dict")