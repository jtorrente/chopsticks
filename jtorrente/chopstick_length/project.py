__author__ = 'jtorrente'

import pandas as pd
import os

DATADIR = "../../data/"
DATAFILE = "chopstick-effectiveness.csv"

def example(data_file):
    dataFrame = pd.read_csv(data_file)
    dataFrame['Food.Pinching.Efficiency'].mean()
    meansByChopstickLength = dataFrame.groupby('Chopstick.Length')['Food.Pinching.Efficiency'].mean().reset_index()
    print meansByChopstickLength

os.chdir(DATADIR)
example(DATAFILE)
