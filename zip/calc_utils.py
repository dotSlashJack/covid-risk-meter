#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester, aditya nair, jeremy smith

Miscellaneous tools for genearting the covid metric and predicitons, etc.
e.g., number to color, reweighting, ...
"""
from scipy.integrate import odeint
from scipy.special import binom
import numpy as np

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
"""
function: library_size
returns the library size of basis functions
"""

def library_size(n, poly_order, include_sine):
    l = 0
    for k in range(poly_order+1):
        l += int(binom(n+k-1,k))
    if include_sine:
        l += n
    return l
    
"""function: polyLib
returns the polynomial basis library for regression
"""
    
def polyLib(x, poly_order):
    # dimension of the problem
    m = x.shape[0]
    n = x.shape[1]
    #
    # special case when poly_order = 0
    poly0 = np.ones((m,1), dtype=x.dtype)
    if poly_order == 0:
        return poly0
    # when poly_order >= 1
    poly_elm = np.concatenate((poly0, x), axis=1)
    poly_ind = polyID(0, n+1, poly_order)
    poly_lib = np.ones((m,len(poly_ind)), dtype=x.dtype)
    #
    for i in range(len(poly_ind)):
        for j in range(poly_order):
            poly_lib[:,i] *= poly_elm[:,poly_ind[i][j]]
    #
    return poly_lib
    
"""function: differentiate
returns the time derivative the data (second-order central difference)
"""

def differentiate(x_in, dt):
    #if x_in.ndim == 2:
    #    x = x_in.reshape((1, x_in.shape[0], x_in.shape[1]))
    #else:
    x = x_in
        
    dx = np.full_like(x, fill_value=np.nan)
    dx[:,1:-1] = (x[:,2:] - x[:,:-2])/(2*dt)
    dx[:,0] = (
        -11 / 6 * x[:,0] + 3 * x[:,1] - 3 / 2 * x[:,2] + x[:,3] / 3
        ) / dt
    dx[:,-1] = (
        11 / 6 * x[:,-1] - 3 * x[:,-2] + 3 / 2 * x[:,-3] - x[:,-4] / 3
        ) / dt
    #if x_in.ndim == 2:
    #    return dx[0]
    return dx

def polyID(s_id, e_id, level):
    """function: polyID
    return the id combinations with given
    starting id (include), ending id (exclude) and level
    """
    # initialize as empty set
    id_set = []
    #
    # return error when level is negative
    assert level >= 0, 'level cannot be negative'
    #
    # special cases when level are 0 and 1
    if level == 0:
        return id_set
    #
    if level == 1:
        return [[i] for i in range(s_id, e_id)]
    #
    # general cases when level are greater than 1
    # using recursion
    for i in range(s_id, e_id):
        sub_id_set = polyID(i, e_id, level - 1)
        for j in range(len(sub_id_set)):
            sub_id_set[j].insert(0, i)
        id_set.extend(sub_id_set)
    #
    return id_set
