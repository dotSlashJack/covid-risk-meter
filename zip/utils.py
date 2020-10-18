#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester

Miscellaneous tools for genearting the covid metric and plots
e.g., number to color, reweighting, ...
"""

"""
function to generate a a numerical value based on cutoffs for later use
scores the value to check against cutoffs
cutoffs, a list, the cutoffs to use
"""
def thresholdRanger(scores, cutoffs):
    if scores <= cutoffs[0]:
        return 0
    elif scores > cutoffs[0] and scores <= cutoffs[1]:
        return 1
    elif scores > cutoffs[1] and scores <= cutoffs[2]:
        return 2
    elif scores > cutoffs[2]:
        return 3

"""
function to generate a threat color based the OVERALL cutoffs
scores, a list, the value to check against cutoffs
cutoffs, a list, the cutoffs to use
"""
def thresholdRangerThreat(scores, cutoffs):
    if scores <= cutoffs[0]:
        return "GREEN"
    elif scores > cutoffs[0] and scores <= cutoffs[1]:
        return "YELLOW1"
    elif scores > cutoffs[1] and scores <= cutoffs[2]:
        return "YELLOW2"
    elif scores > cutoffs[2] and scores <= cutoffs[3]:
        return "ORANGE1"
    elif scores > cutoffs[3] and scores <= cutoffs[4]:
        return "ORANGE2"
    elif scores > cutoffs[4] and scores <= cutoffs[5]:
        return "RED1"
    elif scores > cutoffs[5] and scores <= cutoffs[6]:
        return "RED2"
    elif scores > cutoffs[6]:
        return "PURPLE"

"""
function to reweight scores for testing omission of 1 variable
scores the original list of scores to be reweighted
reweights as .25 pts extra in score per 1 point jump in original score
"""
def reweight(scores):
    reweighted_scores = []
    for score in scores:
        reweighted_scores.append(score+(.25*score))
    return reweighted_scores
