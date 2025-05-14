
import numpy as np
import random

from statistics import mean

import collections
import bisect

def read_field(x):
    """ Converts x to int, float or None"""
    try:
        return int(float(x))
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return None

def mode(data):
    """Return the most common data item. If there are ties, return any one of them."""
    [(item, count)] = collections.Counter(data).most_common(1)
    return item


def err_ratio(predict, dataset, binary=False):
    correct = 0
    for example in dataset.examples:
        desired = example[dataset.target]
        output = predict(example)
        compare = (output == desired if not binary else (output==1) == (desired==1))
        if compare: correct += 1
    return 1 - (correct / len(dataset.examples))


def argmax_random_tie(seq, fn):
    """Return an element with highest fn(seq[i]) score; break ties at random."""
    shuffled_seq = list(seq)
    random.shuffle(shuffled_seq)
    return max(shuffled_seq, key=fn)

def normalize(dist):
    """Multiply each number by a constant such that the sum is 1.0"""
    if isinstance(dist, dict):
        total = sum(dist.values())
        for key in dist:
            dist[key] = dist[key] / total
            assert 0 <= dist[key] <= 1  # probabilities must be between 0 and 1
        return dist
    total = sum(dist)
    return [(n / total) for n in dist]

def remove_all(item, seq):
    """Return a copy of seq (or string) with all occurrences of item removed."""
    if isinstance(seq, str):
        return seq.replace(item, '')
    elif isinstance(seq, set):
        rest = seq.copy()
        rest.remove(item)
        return rest
    else:
        return [x for x in seq if x != item]

    
