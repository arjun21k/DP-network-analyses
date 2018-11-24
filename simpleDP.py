import json
import matplotlib.pyplot as plt
from random import gauss
from scipy.stats import laplace
import random
from collections import defaultdict

def loadData(filename):
    with open(filename) as f:
        packets = json.load(f)
    data = [int(item["_source"]["layers"]["ip"]["ip.len"]) for item in packets if "ip" in item["_source"]["layers"]]
    return data

def average(data):
    return sum(data)/len(data)

def globalGaussianAverage(num, sigma=1):
    noise = gauss(0, sigma)
    return num + noise

def localGaussianAverage(data, sigma=1):
    result = 0
    for entry in data:
        noise = gauss(0, sigma)
        result += (entry + noise)
    return result/len(data)

def globalLaplaceAverage(num, eps=0.1):
    noise = laplace.rvs(0, scale=1/eps)
    return num + noise

def localLaplaceAverage(data, eps=0.1):
    result = 0
    for entry in data:
        noise = laplace.rvs(0, scale=1/eps)
        result += (entry + noise)
    return result/len(data)

# take input as a list of tuples [(size, Value, localDiff, globalDiff), ..., ]
def plotSize(data):
    X = []
    Y_true = []
    Y_local = []
    Y_global = []
    for item in data:
        X.append(item[0])
        Y_true.append(item[1])
        Y_local.append(item[2])
        Y_global.append(item[3])
    plt.plot(X, Y_true, color="orange", label="private response")
    plt.plot(X, Y_local, color="blue", label="local")
    plt.plot(X, Y_global, color="green", label="global")
    plt.xlabel('Sample Size')
    plt.ylabel('Percentage error between noisy and private output')
    plt.title("Sample Size vs Error")
    plt.legend()
    plt.show()

# take input as a dictionary
def plotDiffEpslion(data):
   X = data['size']
   plt.plot(X, data['true'], color='orange', label="private respnse")
   plt.plot(X, data['0.1'], color='green', label="eps=0.1")
   plt.plot(X, data['1'], color='red', label="eps=1.0")
   plt.plot(X, data['3'], color='blue', label="eps=3")
   plt.xlabel('Number of packets')
   plt.ylabel('Average size of packets')
   plt.legend()
   plt.show()

def accuracy_privacy_tradeoff(data):
    res = defaultdict(list)
    # for packet size calculations
    psum = []
    _sum = 0
    for item in data:
        _sum += item
        psum.append(_sum)
    l = len(psum)
    for i in range(1000, l, 1000):
        res["size"].append(i)
        privateResult = (psum[i] - psum[i-1000])/1000
        res["true"].append(privateResult)
        for eps in [0.1, 1, 3]:
            noiseResult = globalLaplaceAverage(privateResult, eps)
            res[str(eps)].append(noiseResult)
    plotDiffEpslion(res)

def sample_size_factor(data):
    res = []
    l = len(data)
    for i in range(1000, l, 1000):
        privateResult = average(data[:i])
        localNoiseResult = localLaplaceAverage(data[:i])
        globalNoiseResult = globalLaplaceAverage(privateResult)
        res.append((i, privateResult, localNoiseResult, globalNoiseResult))
    plotSize(res)


if __name__ == "__main__":
    data = loadData("NetworkTraffic100k.json")
    #accuracy_privacy_tradeoff(data)
    sample_size_factor(data)
