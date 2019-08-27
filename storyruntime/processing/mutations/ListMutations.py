# -*- coding: utf-8 -*-
import random


class ListMutations:

    @classmethod
    def index(cls, mutation, value, story, line, operator):
        item = story.argument_by_name(mutation, 'of')
        try:
            return value.index(item)
        except ValueError:
            return -1

    @classmethod
    def length(cls, mutation, value, story, line, operator):
        return len(value)

    @classmethod
    def append(cls, mutation, value, story, line, operator):
        item = story.argument_by_name(mutation, 'item')
        copy = value.copy()
        copy.append(item)
        return copy

    @classmethod
    def prepend(cls, mutation, value, story, line, operator):
        item = story.argument_by_name(mutation, 'item')
        copy = value.copy()
        copy.insert(0, item)
        return copy

    @classmethod
    def random(cls, mutation, value, story, line, operator):
        return random.choice(value)

    @classmethod
    def reverse(cls, mutation, value, story, line, operator):
        copy = value.copy()
        copy.reverse()
        return copy

    @classmethod
    def sort(cls, mutation, value, story, line, operator):
        copy = value.copy()
        copy.sort()
        return copy

    @classmethod
    def min(cls, mutation, value, story, line, operator):
        return min(value)

    @classmethod
    def max(cls, mutation, value, story, line, operator):
        return max(value)

    @classmethod
    def sum(cls, mutation, value, story, line, operator):
        return sum(value)

    @classmethod
    def contains(cls, mutation, value, story, line, operator):
        item = story.argument_by_name(mutation, 'item')
        return item in value

    @classmethod
    def unique(cls, mutation, value, story, line, operator):
        copy = value.copy()
        tmp_set = set()
        i = 0
        while i < len(copy):
            if copy[i] in tmp_set:
                del copy[i]
            else:
                tmp_set.add(copy[i])
                i += 1

        return copy

    @classmethod
    def remove(cls, mutation, value, story, line, operator):
        item = story.argument_by_name(mutation, 'item')
        copy = value.copy()
        try:
            copy.remove(item)
        except ValueError:
            # The value to be removed is not in the list.
            pass
        finally:
            return copy

    @classmethod
    def replace(cls, mutation, value, story, line, operator):
        by = story.argument_by_name(mutation, 'by')
        copy = value.copy()
        item = story.argument_by_name(mutation, 'item')
        for i, el in enumerate(copy):
            if el == item:
                copy[i] = by

        return copy
