#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

__author__ = "Christian Rojas"

import cProfile
import pstats
import functools
import timeit


def profile(func):
    """A function that can be used as a decorator to measure performance"""
    # You need to understand how decorators are constructed and used.
    # Be sure to review the lesson material on decorators, they are used
    # extensively in Django and Flask.
    @functools.wraps(func)
    def inner(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        result = func(*args, **kwargs)
        profiler.disable()
        ps = pstats.Stats(profiler).strip_dirs().sort_stats('cumulative')
        ps.print_stats(10)
        return result
    return inner
    #raise NotImplementedError("Complete this decorator function")


def read_movies(src):
    """Returns a list of movie titles"""
    print('Reading file: {}'.format(src))
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """returns True if title is within movies list"""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates


def timeit_helper():
    """Part A:  Obtain some profiling measurements using timeit"""
    t = timeit.Timer(
        stmt="find_duplicate_movies('movies.txt')",
        setup='from __main__ import find_duplicate_movies'
    )

    runs_per_repeat = 5
    num_repeats = 7
    result = t.repeat(repeat=num_repeats, number=runs_per_repeat)
    best_time = min(result) / float(runs_per_repeat)
    print("Best time across {} repeats of {} runs per repeat: {} sec".format(
        num_repeats, runs_per_repeat, best_time))


def main():
    """Computes a list of duplicate movie entries"""
    result = find_duplicate_movies('movies.txt')
    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result))


if __name__ == '__main__':
    main()
