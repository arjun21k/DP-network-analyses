import matplotlib.pyplot as plt

alist = [(1000, 90, 87), (2000, 81, 88), (3000, 73, 67), (4000, 68, 55), (5000, 54, 43), (6000, 47, 36)]

e = 0.1
def plotSize(alist, e):
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

dummy = {
    'size' : [1000, 2000, 3000, 4000],
    'true' : [30, 40 , 50 ,60],
    '0.1': [35, 45, 55, 65],
    '1': [33, 43, 53, 63],
    '10': [31, 41, 51, 61]
}
def plotDiffEpslion(dummy):
    X = dummy['size']
    plt.plot(X, dummy['true'], color="orange")
    plt.plot(X, dummy['0.1'], color='green', label="e=0.1")
    plt.plot(X, dummy['1'], color='red', label="e=1")
    plt.plot(X, dummy['10'], color='blue', label="e=10")
    plt.xlabel('Number of tuples')
    plt.ylabel('Size of packet')
    plt.legend()
    plt.show()
#plotSize(alist, 0.1)
#plotDiffEpslion(dummy)

testData = [(1,2), (2,0), (0,2), (4,5), (1,3), (2,2)]

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

plotCDF(testData)
