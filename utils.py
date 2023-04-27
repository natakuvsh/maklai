import itertools
import json
from nltk import ParentedTree
from typing import List



def has_two_child_nps_and_cc_or_comma(tree):
    """
    :param tree: Receiving a subtree
    :return: True if the subtree meets conditions
    """
    labels = [child.label() for child in tree[0:]]
    if labels.count('NP') >= 2 and ('CC' in labels or ',' in labels):
        return True


def get_position_permutations(positions: List):
    """

    :param positions: list of lists of position indexes [[(0, 0), (0, 3)], [(2, 1, 1, 1, 1, 0), (2, 1, 1, 1, 1, 2)]]
    :return: list of all possible permutations inside each of list
    """
    position_permutations = []
    for position in positions:
        permutation_generator = itertools.permutations(position)
        position_permutations.append(permutation_generator)
    return position_permutations


def find_positions(ptree):
    """
    Getting a list of lists, that contains all positions of interchangeable "NP"
    [[(0, 0), (0, 3)], [(2, 1, 1, 1, 1, 0), (2, 1, 1, 1, 1, 2), (2, 1, 1, 1, 1, 4)]]
    :param ptree: receiving a parented tree
    :return: list of positions of "NP" that can be permuted
    """
    positions = []
    for subtree in ptree.subtrees(lambda x: x.label() == 'NP'):
        # Checking if our subtree contains two or more "NP" and "CC" or comma in it
        if has_two_child_nps_and_cc_or_comma(subtree):
            # Creating a list to append positions of all "NP" that are inside one "NP"
            position = []
            first_sub = True
            for sub in subtree.subtrees(lambda x: x.label() == 'NP'):
                # Skipping the first subtree as it contains original "NP" not the subtrees we want
                if first_sub:
                    first_sub = False
                    continue
                position.append(sub.treeposition())
            positions.append(position)
    return positions


def paraphrase_tree(tree: str, limit: int = 20):
    """
    :param tree: receiving a tree as a string as like '(S(NP(NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)))'
    :param limit: limit the paraphrase sentence quantity
    :return: json with paraphrase "{"paraphrases": {"tree": "(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)))}"}
    """
    ptree = ParentedTree.fromstring(tree)

    # Finding positions of all "NP" , that has two or more "NP" and "CC" or comma inside it
    positions = find_positions(ptree)

    # Get permutations of positions
    position_permutations = get_position_permutations(positions)

    # Get permutations of sentences
    permutations = itertools.product(*(permutation_gen for permutation_gen in position_permutations))
    # Initial positions of "NP" values
    initial_positions_list = [list(item) for sublist in positions for item in sublist]

    result = []
    for t in permutations:
        new_position_lists = [list(item) for sublist in t for item in sublist]
        new_tree = ptree.copy(deep=True)
        for i, n in enumerate(new_position_lists):
            # Placing new "NP" to the place of original "NP"
            np_tree = ptree[n].copy(deep=True)
            new_tree[initial_positions_list[i]] = np_tree
        result.append({'tree': new_tree.pformat()})
        # Checking if we exceed our limit of paraphrase sentences
        if len(result) == limit:
            break

    # If we do not want to include original sentence - can use result[1:]
    return json.dumps({'paraphrases': result})
