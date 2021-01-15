import math

# https://stackoverflow.com/a/12413491
def normpdf(x, mean, sd):
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

# https://stackoverflow.com/a/3525548/3059148
def normcdf(x, mean, sd):
    return 0.5 * (1 + math.erf((x - mean) / math.sqrt(2 * sd**2)))

def input_float(msg):
    inp = input(msg).replace('$', '').upper()
    mul = 1
    if inp.endswith('M'):
        mul = 1000000
    elif inp.endswith('K'):
        mul = 1000
    elif inp.endswith('T'):
        mul = 1000000000000
    elif inp.endswith('B'):
        mul = 1000000000
    else:
        return float(inp)

    return float(inp[:-1]) * mul

def portfolio_func(coin, curnt_mk_cap, fut_mk_cap, growth): #growth (percent/yr)
    coin = coin.upper()
    
