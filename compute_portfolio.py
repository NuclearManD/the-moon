
from common import *
import random
import json

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

def portfolioTransfer(portfolioConstants, i, n):
    'Transfers n units to portfolioConstants[i] from the rest, evenly'

    if portfolioConstants[i] < -n:
        return portfolioConstants

    if n / (len(portfolioConstants) - 1) > min(portfolioConstants):
        return portfolioConstants

    portfolioConstants = portfolioConstants.copy()

    portfolioConstants[i] = round(portfolioConstants[i] + n, 4)

    n = n / (len(portfolioConstants) - 1)

    for j in range(len(portfolioConstants)):
        if j != i:
            portfolioConstants[j] = round(portfolioConstants[j] - n, 4)

    return portfolioConstants

def finessePortfolio(portfolioConsts):
    portfolioConsts = portfolioConsts.copy()

    order = list(range(len(portfolioConsts)))
    random.shuffle(order)

    for i in order:
        val = portfolioConsts[i]
        theRest = sum(portfolioConsts) - val

        rewardNoChange = optimizerRewardFunction(portfolioConsts)
        rewardP = optimizerRewardFunction(portfolioTransfer(portfolioConsts, i, .1))
        rewardN = optimizerRewardFunction(portfolioTransfer(portfolioConsts, i, -.1))

        if rewardNoChange >= rewardP and rewardNoChange >= rewardN:
            continue
        if rewardP < rewardN:
            addAmount = -0.01
            reward = rewardN
        else:
            reward = rewardP
            addAmount = 0.01

        portfolioConsts = portfolioTransfer(portfolioConsts, i, addAmount)

        while True:
            newConsts = portfolioTransfer(portfolioConsts, i, addAmount)
            if newConsts == portfolioConsts:
                # Can't go any further
                break

            newReward = optimizerRewardFunction(newConsts)

            if newReward <= reward:
                break

            portfolioConsts = newConsts

    return portfolioConsts

def optimizeRewardFunction(portfolioConstantSeeds, generations = 50, debug = True):

    if debug:
        print("Given", len(portfolioConstantSeeds), "seeds.")
        print("Computing rewards for each seed...")

    rewards = []
    for i in portfolioConstantSeeds:
        rewards.append(optimizerRewardFunction(i))

    if debug:
        print("Eliminating inferior seeds...")

    average_reward = sum(rewards) / len(rewards)

    goodSeeds = []
    for i in range(len(rewards)):
        if rewards[i] > average_reward:
            goodSeeds.append(portfolioConstantSeeds[i])

    if debug:
        print("There are", len(goodSeeds), "seeds left.")

    while True:

        if debug:
            print("Copying and finessing the seeds...")

        for i in range(len(goodSeeds)):
            seed = goodSeeds[i]
            goodSeeds.append(finessePortfolio(seed))
            if len(goodSeeds) < 1000:
                seedMutated = portfolioTransfer(seed, random.randint(0, len(seed) - 1), random.random())
                if seedMutated != seed:
                    goodSeeds.append(seedMutated)

        if debug:
            print("Eliminating inferior seeds and duplicates...")

        # Remove duplicates
        portfolioConstantSeeds = []
        for i in range(len(goodSeeds)):
            if not goodSeeds[i] in portfolioConstantSeeds:
                portfolioConstantSeeds.append(goodSeeds[i])

        if len(portfolioConstantSeeds) == 1:
            return portfolioConstantSeeds[0]

        rewards = []
        for i in portfolioConstantSeeds:
            rewards.append(optimizerRewardFunction(i))

        average_reward = sum(rewards) / len(rewards)

        goodSeeds = []
        for i in range(len(rewards)):
            if rewards[i] > average_reward:
                if not portfolioConstantSeeds[i] in goodSeeds:
                    goodSeeds.append(portfolioConstantSeeds[i])

        if len(goodSeeds) == 0:
            if debug:
                print("No seeds left, reverting...")

            goodSeeds = portfolioConstantSeeds
            continue

        elif len(goodSeeds) == 1:
            return goodSeeds[0]

        if debug:
            print("There are", len(goodSeeds), "seeds left.")

while True:
    goal = input_float('What is your profit goal?')
    total_invested = input_float('How much money are you investing?')
    multiplier = 1

    while goal < 50 or total_invested < 50:
        goal *= 10
        total_invested *= 10
        multiplier *= 10

    rewardMeanMinimum = goal + total_invested

    print("Computing best portfolio...")

    portfolio = optimizeRewardFunction(generateConstantSeeds(), debug = False)

    print("Portfolio:")

    for i in range(len(coins)):
        name = coins[i].name
        print(name + ' '*(6 - len(name)) + str(portfolio[i] / multiplier))

    print("Probability of success: " + str(round(goalProbabilityPercent(portfolio), 1)) + '%')

