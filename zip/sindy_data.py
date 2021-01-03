#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: aditya nair
"""
import numpy as np
import scipy.linalg as la
from scipy.integrate import odeint

class SindyData:
    def __init__(self, X, dX, poly_order, libfunc):
        # input data
        self.m = X.shape[0] # temporal dimension
        self.n = X.shape[1] # spatial dimension
        self.X = X
        self.dX = dX
        self.poly_order = poly_order
        # construction library
        self.library = libfunc
        self.Theta = self.library(X, poly_order)
        self.l = self.Theta.shape[1]

    def predict(self, Sigma, X):
        return np.dot(self.library(X, self.poly_order), Sigma)


    def simulate(self, Sigma, x0, t):
        # note: must pass in I as a function of t
        f = lambda x,t : np.dot(self.library(np.array(x).reshape((1,self.n)),
           self.poly_order),Sigma).reshape((self.n,))

        x = odeint(f, x0, t)
        return x

    def fit_thresholdedlstsq(self, coefficient_threshold, iterations=10):
        xi = np.linalg.lstsq(self.Theta, self.dX, rcond=None)[0]

        for k in range(iterations):
            small_inds = (np.abs(xi) < coefficient_threshold)
            xi[small_inds] = 0
            for i in range(self.n):
                big_inds = ~small_inds[:,i]
                if np.where(big_inds)[0].size == 0:
                    continue
                xi[big_inds,i] = np.linalg.lstsq(self.Theta[:,big_inds], self.dX[:,i], rcond=None)[0]
        return xi


