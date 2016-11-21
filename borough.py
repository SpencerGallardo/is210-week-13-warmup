#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Warm up week 3"""

import csv
import json

GRADING_SCALE = {'A': (100 * .01),
                 'B': (90 * .01),
                 'C': (80 * .01),
                 'D': (70 * .01),
                 'F': (60 * .01)}


def get_score_summary(filename):
    """Health grade average calculator.
    Args:
        filename (string): String representing the filename whose data will be
        read and interpreted.
    Returns:
        (Dictionary): A dictionary containing a de-duplicated list of
        restaurants in a given borough. The borough name is the key, and the
        values as a tuple containing the total number of restaurants, and the
        average grade as a numerical score, converted from the letter grade.
    Examples:
        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314144), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331528),'QUEENS':
        (414, 0.9719806763285019)}
    """
    dedupe = {}
    fhandler = open(filename, 'rb')
    freader = csv.reader(fhandler, delimiter=',')

    for line in freader:
        camisid = line[0]
        boro = line[1]
        grade = line[10]
        if camisid not in dedupe and grade in GRADING_SCALE:
            dedupe[camisid] = [grade, boro]

    fhandler.close()

    boro_count = {}

    for restaurant in dedupe.values():
        letter = restaurant[0]
        borough = restaurant[1]
        if borough not in boro_count:
            boro_count[borough] = [1, GRADING_SCALE[letter]]
        else:
            boro_count[borough][0] += 1
            boro_count[borough][1] += GRADING_SCALE[letter]

    avg_scores = {}

    for borough, grades in boro_count.iteritems():
        avg_scores[borough] = grades[0], (grades[1])/(grades[0])

    return avg_scores


def get_market_density(filename):
    """Green Market Counter.
    Args:
        filename (string): String representing the filename of the JSON file
        whose data will be read.
    Returns:
        Dictionary with borough names as keys and total number of green markets
        in each borough as a value.
    Example:
        >>> get_market_density('green_markets.json')
        {u'Bronx': 32, u'Brooklyn': 48, u'Staten Island': 2,
        u'Manhattan':39, u'Queens': 16}
    """
    fhandler = open(filename, 'r')

    data = json.load(fhandler)

    fhandler.close()
    markets = {}
    for value in data['data']:
        borough = value[8]
        borough = borough.upper()
        borough = borough.rstrip()
        if borough not in markets:
            markets[borough] = 1
        else:
            markets[borough] += 1
    return markets


def correlate_data(restdata, mktsdata, output):
    """Combines data from two files and combines them into one.
    Args:
        restdata(string): The inspection_results.csv filename containing New
        York City restaurant grades.
        mktsdata (string): The green_markets.json filename containing New York
        City green markets locations.
        output(string): The name of the file as a string which the combined data
        will be dumped into.
    Returns:
        output(file): A text file containing the combined data as a dictionary.
        File is created in the directory the python file is located in.
    Example:
        >>> correlate_data('inspection_results.csv', 'green_markets.json',
        'output')
        >>>
    """
    restscore = get_score_summary(restdata)
    greenmkts = get_market_density(mktsdata)
    correlate = {}

    fhandler = open(output, 'w')

    dictlist = [restscore, greenmkts]
    for key in restscore.iterkeys():
        correlate[key] = tuple(correlate[key] for correlate in dictlist)

    combined = {}
    for key, value in correlate.iteritems():
        if key not in combined:
            combined[key] = (value[0][1], (float(value[1])/value[0][0]))

    json.dump(combined, fhandler)

    fhandler.close()
