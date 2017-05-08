#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
from typing import List, TypeVar


class Range(object):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def get_id(self) -> str:
        return '%s-%s' % (self.start, self.end)

    def size(self) -> int:
        return self.end - self.start

    def merge(self, another: 'Range') -> 'Range':
        return Range(min(self.start, another.start), max(self.end, another.end))

    def shift(self, offset: int) -> 'Range':
        obj = copy.copy(self)
        obj.start += offset
        obj.end += offset
        return obj

    def same_range(self, range):
        return self.start == range.start and self.end == range.end

    def is_overlap(self, another):
        a, b = self, another
        if a.start > b.start:
            a, b = b, a

        return a.end > b.start

    def is_contain(self, another):
        return self.start <= another.start and self.end >= another.end

    def is_cross(self, another):
        return self.is_overlap(another) and not self.is_contain(another)


class IntervalTreeNode(object):

    def __init__(self, range: Range, children: List['IntervalTreeNode']):
        self.range = range
        self.children = children


def build_interval_tree(ranges: List[Range]) -> IntervalTreeNode:
    def tree_insert(node: IntervalTreeNode, range: Range):
        for child in node.children:
            if child.range.is_contain(range):
                return tree_insert(child, range)

        node.children.append(IntervalTreeNode(
            range=range,
            children=[]
        ))
        node.children.sort(key=lambda r: r.range.start)
        return

    """
        The algorithm will construct the tree such that range of subtree is contained in its parent.
        This is greedy algorithm, the algo. will sort ranges by its interval length, and insert one by one to the tree.
        
        Nodes of the returned tree are ranges, except the root of the tree is constructed by the left and right most interval.

        Examples:
            List of ranges: (1, 2), (4, 5), (1, 7), (8, 9) will result as the following tree:
                    (1, 9)
                /          \
              (1, 7)      (8, 9)
            |       |
           (1,2) (4, 5)
           List of ranges: (1, 3), (2, 3), (2, 4) will result the following tree:
                    (1, 4)
                /           \
            (1, 3)         (2, 4)
                |
            (2, 3)
    """
    left_most_value = min(ranges, key=lambda a: a.start).start
    right_most_value = max(ranges, key=lambda a: a.end).end

    root = IntervalTreeNode(Range(left_most_value, right_most_value), [])

    # sort ranges by its length, descending order, and start inserting to the tree until insert all ranges
    ranges = sorted(ranges, key=lambda a: a.end - a.start, reverse=True)
    for range in ranges:
        tree_insert(root, range)

    return root


class Annotation(Range):
    pass


def group_overlapped_range(ranges: List[Range]) -> List[List[Range]]:
    def get_range_start(x: Range) -> float:
        return x.start

    # sort by the start
    ranges.sort(key=get_range_start)
    overlapped_ranges = [(Range(ranges[0].start, ranges[0].end), [ranges[0]])]

    for i in range(1, len(ranges)):
        if ranges[i].is_overlap(overlapped_ranges[-1][0]):
            overlapped_ranges_ranges[-1][0] = ranges[i].merge(overlapped_ranges[-1][0])
            # overlapped_ranges_ranges[-1][0] =

    #     if len(match_ranges) == 0:
    #         overlapped_ranges.append(r)
    return ranges

group_overlapped_range([Annotation(1, 2), Annotation(4, 5)])
group_overlapped_range([Range(1, 2), Range(4, 5)])

group_overlapped_range([(1, 2), (4, 5)])
