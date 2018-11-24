from scipy.stats import laplace
import json
import matplotlib.pyplot as plt
from random import gauss
from collections import defaultdict

def average(data):
    return 1.0 * sum(data)/len(data)

def globalGaussianAverage(data, sigma=1):
    result = average(data)
    noise = gauss(0, sigma)
    return result + noise

def localGaussianAverage(data, sigma=1):
    result = 0
    for entry in data:
        noise = gauss(0, sigma)
        result += (entry + noise)
    return result/len(data)

def globalLaplaceAverage(data, eps=0.1):
    result = average(data)
    noise = laplace.rvs(0, scale=1/eps)
    return result + noise

def localLaplaceAverage(data, eps=0.1):
    result = 0
    for entry in data:
        noise = laplace.rvs(0, scale=1/eps)
        result += (entry + noise)
    return result/len(data)

# take input as a list of tuples [(size, localDiff, globalDiff), ..., ]
def plotSize(alist, eps=0.1):
    X = []
    Y_local = []
    Y_global = []
    for item in alist:
        X.append(item[0])
        Y_local.append(item[1])
        Y_global.append(item[2])
    #print(X)
    #print(Y)
    plt.plot(X, Y_local)
    plt.plot(X, Y_global)
    plt.xlabel('Number of tuples')
    plt.ylabel('Percentage error between noisy output and raw data')
    plt.title("Tuple Size vs Epsilon")
    plt.show()

# take input as a dictionary of eps->[(size, trueValue, noisedValue),..., ]
def plotDiffEpslion(dummy):
   X = dummy['size']
   print(2, dummy["true"])
   plt.xlabel('Number of packets')
   plt.plot(X, dummy['true'], color='yellow')
   plt.ylabel('Average size of packets')
   plt.plot(X, dummy['0.1'], color='green')
   #print(dummy['0.1'])
   plt.plot(X, dummy['1'], color='red')
   #print(dummy['1'])
   plt.plot(X, dummy['10'], color='blue')
   #print(dummy["10"])
   plt.show()


if __name__ == "__main__":
    with open("NetworkTrace.json") as f:
        packets = json.load(f)
    
    data = [int(item["_source"]["layers"]["ip"]["ip.len"]) for item in packets if "ip" in item["_source"]["layers"]]
    res = {}
    res["size"] = []
    res["true"] = []
    for eps in [0.1, 1, 10]:
        res[str(eps)] = []
    for i in range(1000, 10000, 1000):
        res["size"].append(i)
        true = average(data[:i])
        res["true"].append(true)
        for eps in [0.1, 1, 10]:
            local = localLaplaceAverage(data[:i], eps)
            res[str(eps)].append(local)
        #glo = globalLaplaceAverage(data[:i], eps)
        #localDiff = 100 * abs(local-true)/true
        #gloDiff = 100 * abs(glo-true)/true
    print(1, res["true"])
    plotDiffEpslion(res)

    '''
    true = average(data)
    print("true " + str(true))
    print("local " + str(localLaplaceAverage(data)))
    print("global " + str(globalLaplaceAverage(data)))
    '''
