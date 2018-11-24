import json
import matplotlib.pyplot as plt
from random import gauss
from scipy.stats import laplace
import random
from collections import defaultdict

def trueCount(data, target):
    count = 0
    for item in data:
        if item==target:
            count += 1
    return count

def randomizedResponseCount(data, target):
    result = 0
    for entry in data:
        coin = random.randrange(0, 1)
        if coin > 0.5:
            # give private answer
            if entry == target:
                result += 1
        else:
            result += random.randrange(0, 1)
    result = (result/len(data) - 0.25) * 2.0 * len(data)
    return result

def loadData(filename):
    with open(filename) as f:
        packets = json.load(f)
    data = [int(item["_source"]["layers"]["tcp"]["tcp.srcport"]) for item in packets if "tcp" in item["_source"]["layers"]]
    return data

def globalLaplaceAverage(num, eps=0.1):
    noise = laplace.rvs(0, scale=1/eps)
    return num + noise

def plotCDF(trueVals, noiseCDF0_1, noiseCDF1, noiseCDF10):
   X = [i for i in range(65536)]
   plt.plot(X, trueVals, label="true values")
   plt.plot(X, noiseCDF0_1, label="e = 0.1")
   plt.plot(X, noiseCDF1, label="e = 1")
   plt.plot(X, noiseCDF10, label="e = 10")
   plt.xlabel('Ports')
   plt.ylabel('CDF')
   plt.legend()
   plt.show()

if __name__=="__main__":

    data = loadData("NetworkTraffic100k.json")
    ports = [0 for _ in range(65535)]
    for item in data:
        ports[item] += 1
    
    cdf = [0]
    noisedCDF0_1 = [0]
    noisedCDF1 = [0]
    noisedCDF10 = [0]
    for p in ports:
        cdf.append(cdf[-1] + p)
        noisedCDF0_1.append(globalLaplaceAverage(cdf[-1]))
        noisedCDF1.append(globalLaplaceAverage(cdf[-1], eps=1.0))
        noisedCDF10.append(globalLaplaceAverage(cdf[-1], eps=10.0))
    
    plotCDF(cdf, noisedCDF0_1, noisedCDF1, noisedCDF10)
