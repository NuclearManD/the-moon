
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

def calcRewardMean(portfolioConstants):
    total = 0
    for i in range(len(coins)):
        coin = coins[i]
        total += coin.mean * portfolioConstants[i] / coin.cap

    return total

def calcRewardStdDev(portfolioConstants):
    total = 0
    for i in range(len(coins)):
        coin = coins[i]
        x = coin.stddev * portfolioConstants[i] / coin.cap
        total += x * x

    return math.sqrt(total)

def goalProbabilityPercent(portfolioConstants):
<<<<<<< HEAD
    pass
   
=======
    Rm = calcRewardMean(portfolioConstants)
    Ro = calcRewardStdDev(portfolioConstants)

    return 100 * (1 - normcdf(rewardMeanMinimum, Rm, Ro))

def optimizerRewardFunction(portfolioConstants):
    # Modify this to change what the optimizer optimizes for
    return goalProbabilityPercent(portfolioConstants)

def generateConstantSeeds():
    l_coins = len(coins)

    li = []

    # Add the case of the even distribution
    li.append([total_invested / l_coins] * l_coins)

    # Add the single choice cases
    for i in range(l_coins):
        item = [0] * l_coins
        item[i] = total_invested
        li.append(item)

        # Add the two choice cases
        for j in range(i + 1, l_coins):
            item = [0] * l_coins
            item[i] = total_invested / 2
            item[j] = total_invested / 2
            li.append(item)

    return li

>>>>>>> 93bbb3b427fa98889213b05e56ec94e19ebbeb46
