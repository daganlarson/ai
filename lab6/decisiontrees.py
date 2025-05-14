
from utils import *
import random
import bisect
import math

class DataSet:
    """
    Data set for learning problem.

    d.examples   A list of examples. Each one is a list of attribute values.
    d.attrs      A list of integers to index into an example, so example[attr]
                 gives a value. Normally the same as range(len(d.examples[0])).
    d.attr_names Optional list of mnemonic names for corresponding attrs.
    d.target     The attribute that a learning algorithm will try to predict.
                 By default the final attribute.
    d.inputs     The list of attrs without the target.
    d.values     A list of lists: each sublist is the set of possible
                 values for the corresponding attribute. If initially None,
                 it is computed from the known examples by self.set_problem.
                 If not None, an erroneous value raises ValueError.
    """
    def __init__(self,examples,attrs,attr_names,target=None,inputs=None):

        self.examples : list[list[int]]= examples
        self.attrs : list[int] = attrs
        self.attr_names = attr_names

        ## Default target is in last column
        self.target = target or len(self.attrs) -1

        ## inputs are all attributes that are not the target
        self.inputs = inputs or [a for a in self.attrs if a != self.target]
        
        ## Obtain sorted unique values for each attribute
        self.values = list(map(lambda seq: sorted(set(seq)), zip(*self.examples)))


    def column(self,col):
        """ Get the values from column col """
        return list(zip(*self.examples))[col]

################################################################################

def read_dataset_from_csv(filename):
    """
    Read a comma-separated-value table with a header
    """
    input = open(filename).read()    
    lines = [line for line in input.splitlines() if line.strip()]
    attr_names=lines[0].split(',')
    attrs = list(range(len(attr_names)))
    records= [list(map(read_field,line.split(','))) for line in lines[1:]]
    return DataSet(records,attrs,attr_names)

################################################################################

class OrderedValueMap:
    """An object that stores a set of ordered values and retrieves the
    nearest in-order value to a key

    """
    def __init__(self,values):
        self.values = values

    def __getitem__(self, key):
        index = bisect.bisect_left(self.values,key)        
        return self.values[min(index,len(self.values)-1)]

################################################################################
    
class DecisionTreeNode:
    """
    A fork of a decision tree holds an attribute to test, and a dict
    of branches, one for each of the attribute's values.
    """

    def __init__(self, attr, attr_name, values, branches=None):
        """Initialize by saying what attribute this node tests."""
        self.attr = attr
        self.attr_name = attr_name or attr
        self.valueMap = OrderedValueMap(values)
        self.branches = branches or {}

    def __call__(self, example):
        """Given an (unseen) example, classify it using the attribute and the
branches.

        """
        attr_val = example[self.attr]
        return self.branches[self.valueMap[attr_val]](example)
            
    def add(self, val, subtree):
        """Add a branch. If self.attr = val, go to the given subtree."""
        self.branches[val] = subtree

    def display(self, indent=0):
        name = self.attr_name
        print('Test', name)
        for (val, subtree) in self.branches.items():
            print(' ' * 4 * indent, name, '=', val, '==>', end=' ')
            subtree.display(indent + 1)

    def __repr__(self):
        return 'DecisionTreeNode({0!r}, {1!r}, {2!r})'.format(self.attr, self.attr_name, self.branches)

class DecisionTreeLeaf:
    """A leaf of a decision tree holds just a result."""

    def __init__(self, result):
        self.result = result

    def __call__(self, example):
        return self.result

    def display(self,indent):
        print('RESULT =', self.result)

    def __repr__(self):
        return repr(self.result)

def DecisionTreeLearner(dataset):

    target, values = dataset.target, dataset.values

    def decision_tree_learning(examples, attrs, parent_examples=()):
        ### YOU COMPLETE THIS ###
        ### Hint: you may use the other functions in this scope ###
        if len(examples) == 0:
            return plurality_value(parent_examples)
        elif all_same_class(examples):
            return DecisionTreeLeaf(examples[0][target])
        elif len(attrs) == 0:
            return plurality_value(examples)
        
        A = choose_attribute(attrs, examples)
        tree = DecisionTreeNode(A, None, examples)
        
        attrsMinusA = attrs.copy()
        attrsMinusA.remove(A)

        for val, exs in split_by(A, examples):
            subtree = decision_tree_learning(exs, attrsMinusA, examples)
            tree.add(exs, subtree)

        return tree

    def plurality_value(examples):
        """
        Return the most popular target value for this set of examples.
        (If target is binary, this is the majority; otherwise plurality).
        """
        popular = argmax_random_tie(values[target], fn=lambda v: count(target, v, examples))
        return DecisionTreeLeaf(popular)

    def count(attr, val, examples):
        """Count the number of examples that have example[attr] = val."""
        return sum(e[attr] == val for e in examples)

    def all_same_class(examples):
        """Are all these examples in the same target class?"""
        class0 = examples[0][target]
        return all(e[target] == class0 for e in examples)

    def choose_attribute(attrs, examples):
        """Choose the attribute with the highest information gain."""
        return argmax_random_tie(attrs, fn=lambda a: information_gain(a, examples))

    def information_gain(attr, examples):
        """Return the expected reduction in entropy from splitting by attr."""
        ### YOU COMPLETE THIS ###
        def B(q):
            return -(q * math.log2(q) + (1-q) * math.log2(1-q)) 
        
        def entropy(attr, examples):


        def Remainder(A):
            for val, examples in split_by(A):
                examples[target]

        
        

    def split_by(attr, examples):
        """Return a list of (val, examples) pairs for each val of attr."""
        return [(v, [e for e in examples if e[attr] == v]) for v in values[attr]]

    return decision_tree_learning(dataset.examples, dataset.inputs)

################################################################################    

def RandomForest(dataset : DataSet, n=11):
    """An ensemble of Decision Trees trained using bagging and feature bagging."""

    def data_bagging(dataset, m=100):
        """Sample m examples with replacement"""
        n = len(dataset.examples)
        return random.choices(dataset.examples,k=m or n)

    def feature_bagging(dataset, p=0.7):
        """Feature bagging with probability p to retain an attribute"""
        inputs = [i for i in dataset.inputs if p > random.random()]
        return inputs or dataset.inputs

    def predict(example):
        results = [predictor(example) for predictor in predictors]
        # Return the most frequent result (majority vote)
        return max(set(results), key=results.count)
    
    predictors = []

    for i in range(n):
        predictors.append(DataSet(data_bagging(dataset), feature_bagging(dataset), dataset.attr_names, dataset.target, dataset.inputs))

    return predict


################################################################################

if __name__ == "__main__":
    train = read_dataset_from_csv("heart.train.dat")
    test = read_dataset_from_csv("heart.test.dat")
    predict = RandomForest(train)
    print(predict(test.examples))
