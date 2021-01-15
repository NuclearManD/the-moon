
from common import *
import json

goal = input_float('What is your profit goal?')
total_invested = input_float('How much money are you investing?')

coins = []

class Coin:
    def __init__(self, name, marketCap, futureCapMean, futureCapStdDev):
        self.cap = marketCap
        self.mean = futureCapMean
        self.stddev = futureCapStdDev
        self.name = name

with open('coins.json', 'r') as f:
    doc = json.load(f)

    for coin_data in doc['coins']:
        coins.append(Coin(
            coin_data['name'],
            coin_data['marketCap'],
            coin_data['futureCap'],
            coin_data['standardDeviation']
        ))

rewardMeanMinimum = goal + total_invested

#def 

def goalProbabilityPercent(portfolioConstants):
    pass
   