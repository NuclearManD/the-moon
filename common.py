import math

# https://stackoverflow.com/a/12413491
def normpdf(x, mean, sd):
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

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
