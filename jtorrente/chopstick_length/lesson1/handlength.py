__author__ = 'jtorrente'

import xlrd
import os
import numpy
import pandas
import statsmodels.api as sm

DATADIR = "../../../data/"
DATAFILE = "Height and hand length of Udacians - Lesson 1.xlsx"

def parse_file(datafile):
    '''
    Parses the file containing Excel data into a matrix, which is returned.
    Only first three columns and 21 rows in sheet 0 are processed.
    '''
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    hand_lengths = []
    heights = []
    genders = []
    for i in range(1,21):
        hand_lengths.append(sheet.cell_value(i, 0))
        heights.append(sheet.cell_value(i, 1))
        genders.append(sheet.cell_value(i, 2))
    return pandas.DataFrame({'hand_length':hand_lengths, 'gender':genders, 'height':heights})


def linear_regression(features, values):
    '''
    Perform linear regression given a data set with an arbitrary number of features.
    '''

    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]

    return intercept, params

def predictions(dataframe, hand_length, gender):
    '''
    Performs linear regression on a dataframe with three columns: hand_length (float), height (float),
    and gender (string with possible values F and M), using hand_length and gender as features and height
    as output (dependent) variable.

    Based on the model generated, it returns the predicted height for a given hand_length and gender
    :param dataframe: The dataframe containing the data for a linear model
    :param hand_length: The hand_length to be used to create a new prediction
    :param gender: The gender to be used to create a new prediction
    :return: The predicted height for hand_length and gender
    '''
    # Select Features (try different features!)
    features = dataframe[['hand_length']]

    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe['gender'], prefix='unit')
    features = features.join(dummy_units)

    # Values
    values = dataframe['height']

    # Get the numpy arrays
    features_array = features.values
    values_array = values.values

    # Perform linear regression
    intercept, params = linear_regression(features_array, values_array)

    predictions = intercept + numpy.dot([hand_length, 1 if gender == 'F' else 0, 1 if gender == 'M' else 0], params)
    return predictions


os.chdir(DATADIR)

dataframe = parse_file(DATAFILE)
print "## DATAFRAME: ##"
print dataframe
print
print "## PREDICTED HEIGHT (inches): ##"
print predictions(dataframe, 6.75, 'F')