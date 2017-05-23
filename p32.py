""" Python script to implement the second problem of the third phase of the Python Learning Program
    P2. Write a generator that returns all the subsets of a given set. Example:
        Input: set([1, 2, 3])
        Output: set([1, 2, 3]), set([2, 3]), set([1, 3]), set([3]), set([1,
        2]), set([2]), set([1]), set([])
    """
from itertools import chain, ifilter, imap, permutations


def isubsets(given_set):
    """ iterable that returns all the subsets of a given set """
    size = len(given_set) # this will be used with range for the permutations' length
    # how it's done:
    # 1. make a list(?) of itertools.permutations of length from 0 to len(given_set) - 1
    # 2. pass the list to itertools.chain
    # 2. itertools.ifilter from that list the permutations that are not sorted
    #    e.g.: we want set([1,2]) but not also set([2, 1])
    # 3. the itertools.permutations gives us tuples, we want sets (results are sub-sets)
    result = imap(set,
                  ifilter(lambda x: sorted(x) == list(x),
                          chain(permutations(given_set, index) for index in range(size))))
    return result


def gsubsets(given_set):
    """ generator that returns all the subsets of a given set """
    set_size = len(given_set)
    # we will run itertools.permutations on given_set with a size for
    # the resulting tuples (from 0 to len(given_set)-1)
    for psize in range(set_size):
        permutation = permutations(given_set, psize)
        # permutation holds all the permutations of a psize size
        # for each of it, we verify if it's sorted: we want set([1,2]) but not also set([2, 1])
        # if true, then we yield the set of that tuple
        for item in permutation:
            # sorted return a list, while item is a tuple
            if sorted(item) == list(item):
                yield set(item)

    yield set([])


# to test with sets of numbers
SUBSET_LIST = [set([1, 2]), set([1, 3]), set([2, 3]), set([1]), set([2]), set([3]), set([])]
# to test with sets of strings
SUBSET_LIST2 = [set(['a', 'b']),
                set(['a', 'c']),
                set(['b', 'c']),
                set(['a']),
                set(['b']),
                set(['c']),
                set([])]


def test_isubsets_example():
    """ test the iterable subset with the example in pdf """
    argument = set([1, 2, 3])

    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item in SUBSET_LIST


def test_gsubsets_example():
    """ test the generator subset with the example in pdf """
    argument = set([1, 2, 3])

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item in SUBSET_LIST


def test_subsets_empty():
    """ test subsets with the empty set """
    argument = set([])
    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item == set([])

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item == set([])

    argument = set()
    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item == set()

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item == set()

    argument = set([()])
    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item == set([])

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item == set([])


def test_subsets_chars():
    """ test the subsets iterable and generator with sets of characters """
    argument = set(['a', 'b', 'c'])

    to_iterate = isubsets(argument)
    for item in to_iterate:
        assert item in SUBSET_LIST2

    to_iterate = gsubsets(argument)
    for item in to_iterate:
        assert item in SUBSET_LIST2
