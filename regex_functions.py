"""
# Copyright 2013 Nick Cheng, Brian Harrington, Danny Heap, Yue Gan, 2013, 2014
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see .
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment

# Student code below this comment.


def is_regex(regex):
    '''
    (str) -> bool

    Check if regex is a valid statement, return True iff its valid
    From here, regex == regex statement

    REQ: regex must be string

    Example:

    >>>is_regex('(1|2)')
    True
    >>>is_regex('8e9rsoidhfsodf')
    False
    '''
    if regex == '':

        return False

    if len(regex) == 1:

        return regex in '012e'

    if regex[-1] == '*':

        return is_regex(regex[:-1])

    if regex[0] == '(' and regex[-1] == ')':

        # terminates regex that contains only 'r*'
        if len(regex) < 5:

            return False

        # set number of left bracket and right bracket
        # when number of left bracket and right bracket are the same,
        # it is a complete regex, else it does not validate

        # from here: o_index == operator index
        # num_left/right == number of left/right bracket
        num_left = 0
        num_right = 0
        o_index = 0
        bar = 0
        dot = 0

        for i in range(1, len(regex)):

            if regex[i] == '(':

                num_left += 1

            if regex[i] == ')':

                num_right += 1

            # if there are no inner bracket at all, then it is another case
            if num_left == num_right and num_left != 0 and i < len(regex):

                # if the bracket completes after the operator, then the
                # operator must be before the left bracket of r2
                # hence -4 is the least index it must reach for it to be at end
                if i > len(regex) - 4:

                    o_index = regex[1:].index('(')

                elif regex[i + 1] == '*':

                    # the next char that is not a '*' must be a operator
                    for s in range(i + 2, len(regex)):

                        if regex[s] != '*':

                            o_index = s

                            break

                else:
                    o_index = i + 1

                break

        if o_index == 0:

            if '|' in regex:
                bar = regex.index('|')

            if '.' in regex:
                dot = regex.index('.')

            if not(bar == 0 and dot == 0) or (bar == 0 and dot == 0):

                o_index = max(bar, dot)

        # check left side and right side
        return is_regex(regex[1:o_index]) and is_regex(regex[o_index + 1:-1])

    else:

        return False


def all_regex_permutations(regex):
    '''
    (str) -> set

    Function returns a set of permutation for the regex which is also a valid
    regular expression.

    REQ: regex must be string.

    Example:
    >>>all_regex_permutations('(1|2)')
    {'(1|2)', '(2|1)'}

    >>>all_regex_permutations(')(12|')
    {'(1|2)', '(2|1)'}

    >>>all_regex_permutations('(1|2)))))))))))')
    {}

    '''
    # First off check if there is any validation starting off

    left = 0
    right = 0
    for letters in regex:

        if letters not in '123e()|.*':

            return {}

        if letters == '(':

            left += 1

        if letters == ')':

            right += 1

    if left != right and left != 0:

        return {}

    valid_set = set()
    all_perm = perms(regex)

    for i in all_perm:

        if is_regex(i):

            valid_set.add(i)
        else:
            pass

    return valid_set


def perms(s):
    '''
    (str) -> set

    An algorithm from ex8 CSCA48 Winter 2013. This funciton helps to find
    all the possible permutation using brutal force.

    REQ: s must be a string.

    Example:
    >>>perm('1**')
    {'1**', '*1*', '**1', '1**', '*1*', '**1'}
    '''
    # ex 5

    if len(s) == 1:

        return set([s])

    perm = set()

    for seed in perms(s[1:]):

        for position in range(len(s)):

            perm.add(seed[:position] + s[0] + seed[position:])

    return perm


def regex_match(r, s):
    '''
    (str) -> bool

    This function checks if the given s(string) matches with the permutation
    from the given regex. Return True if and only if it passes the test.

    REQ: r must be a RegexTree, s must be string

    From here, r = regex, s = string

    Example:
    >>> regex_match(BarTree(Leaf('1'), StarTree(Leaf('0'))), '01')
    False
    >>> regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '0')
    True
    >>> regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '111110')
    True
    '''

    if isinstance(r, Leaf):

        if r.symbol == 'e':
            return s == ''

        return s == r.symbol

    if isinstance(r, StarTree):

        isTrue = True
        pattern = []

        # we can use the same pattern for dot and leaf
        if isinstance(r.children[0], DotTree) or\
           isinstance(r.children[0], Leaf):

            for i in range(1, len(s)):

                # if there is any  number that can devide the length, it might
                # be a pattern

                if len(s) % i == 0:

                    pattern = []

                    for x in range(0, len(s), i):

                        pattern.append(s[x:x + i])

                    # found the patter, ie ['12', '12', '12']
                    if check_identical(pattern):

                        break

                # if not check the whole string
                if i == len(s) - 1:

                    return regex_match(r.children[0], s)

            for substring in pattern:

                isTrue = regex_match(r.children[0], substring) and isTrue

            return isTrue

        if isinstance(r.children[0], BarTree):

            root_list = find_root(r)

            while s != '':

                temp_s = s
                # e for element
                for e in root_list:

                    if s[:len(e)] == e:

                        s = s[len(e):]

                # if the element is not in the root list
                if s == temp_s:

                    return False

            if s == '':

                return True

        else:

            return False

    if isinstance(r, DotTree):

        # i for index, check every posssibility
        isTrue = False
        for i in range(len(s)):

            isTrue = (regex_match(r.children[0], s[:i]) and
                      regex_match(r.children[1], s[i:])) or isTrue

        return isTrue

    if isinstance(r, BarTree):

        isTrue, left, right = False, False, False
        for i in range(len(s)):

            left = regex_match(r.children[0], s[:i + 1])
            right = regex_match(r.children[1], s[i + 1:])
            isTrue = ((left or right) and (left != right)) or isTrue

        return isTrue


def build_regex_tree(regex):
    '''
    (str) -> RegexTree

    This function takes a valid regex and build a tree correspoinding to its
    given permutation.

    REQ: regex must be string.

    Example:
    >>> build_regex_tree('(0*|1*)')
    BarTree(StarTree(Leaf('0')), StarTree(Leaf('1')))

    >>> build_regex_tree('((0.1).0)')
    DotTree(DotTree(Leaf('0'), Leaf('1')), Leaf('0'))

    >>> build_regex_tree('((1.(0|1)*).0)')
    DotTree(DotTree(Leaf('1'), StarTree(BarTree(Leaf('0'), Leaf('1')))),
            Leaf('0'))
    '''

    if len(regex) == 1:

        if regex in '012e':

            return Leaf(regex)

    if regex[-1] == '*':

        return StarTree(build_regex_tree(regex[:-1]))

    if regex[0] == '(' and regex[-1] == ')':

        num_left = 0
        num_right = 0
        o_index = 0
        bar = 0
        dot = 0

        for i in range(1, len(regex)):

            if regex[i] == '(':

                num_left += 1

            if regex[i] == ')':

                num_right += 1

            if num_left == num_right and num_left != 0 and i < len(regex):

                if i > len(regex) - 4:

                    o_index = regex[1:].index('(')

                elif regex[i + 1] == '*':

                    # the next char that is not a '*' must be a operator
                    for s in range(i + 2, len(regex)):

                        if regex[s] != '*':

                            o_index = s

                            break

                else:
                    o_index = i + 1

                break

        if o_index == 0:

            if '|' in regex:
                bar = regex.index('|')

            if '.' in regex:
                dot = regex.index('.')

            if not(bar == 0 and dot == 0) or (bar == 0 and dot == 0):

                o_index = max(bar, dot)

            # check left side and right side
        if regex[o_index] == '.':

            return DotTree(build_regex_tree(regex[1:o_index]),
                           build_regex_tree(regex[o_index + 1:-1]))

        else:

            return BarTree(build_regex_tree(regex[1:o_index]),
                           build_regex_tree(regex[o_index + 1:-1]))


def find_root(regex):
    '''
    (str) -> list of str

    This is a helper function which finds all the root of a tree.

    REQ: regex must be a RegexTree

    Example:
    >>>regex = StarTree(Leaf('1'))
    >>>find_root(regex)
    ['1']
    '''

    if isinstance(regex, Leaf):

        return [regex.symbol]

    if isinstance(regex, StarTree):

        return find_root(regex.children[0])

    if isinstance(regex, BarTree):

        return find_root(regex.children[0]) + find_root(regex.children[1])

    if isinstance(regex, DotTree):

        return [find_root(regex.children[0])[0] +\
                find_root(regex.children[1])[0]]

    else:
        return []


def check_identical(slist):
    '''
    (str) -> bool

    Helper function. check if every element in the list are identical

    REQ: slist must be a string list

    Example:
    >>> check_identical(['12', '12', '12'])
    True
    >>> check_identical(['123123123','4564565'])
    False
    '''

    if slist == ['']:

        return False

    temp = slist[0]

    # check for every element in the list, if one violate it will return False
    for x in slist:

        if x != temp:

            return False

    return True
