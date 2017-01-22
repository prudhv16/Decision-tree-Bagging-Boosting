from __future__ import division
import DecisionTree as dtree
import random
import operator
import os
import sys



# function to take dataset as argument, store rows in a list and generate test and training data according to nFold value

def parseFile(dataset):
    #print dataset
    f = open(dataset, 'r')
    overallRows = []
    for line in f.readlines():
        lines = line.strip("\n").split(',')
        individualRow =[]
        for data in lines:
            individualRow.append(data)
        overallRows.append(individualRow)
    f.close()
    #print overallRows[0]
    return overallRows[1:]

def decisiontree(dataset,testingData,tdepth,nummodels,boost):
    #overallRows = parseFile(dataset)
    testData = parseFile(testingData)
    #print(overallRows[2])
    features = dataset[0]
    #featuresList =[]
    numOfFeatures = len(features[:20]+features[22:])
    #print features[20:22]
    #trainData =[]
    #testData =[]
    #Need changes here.
    #featuresList=[]
    #for ftr in range(numOfFeatures):
    #    featuresList.append([ftr])
    #subsetSize = int(len(overallRows)*0.7)
    #random.shuffle(overallRows)
    trainData = [x[:21]+x[22:] for x in dataset]
    testData = [x[:21]+x[22:] for x in testData]
    #print trainData[:1]
    #testData = testData #overallRows[subsetSize:]
    #trainData = trainData  #overallRows[:subsetSize]
    '''
    1. Added depth parameter
    2. Removed gain parameter
    '''
    #for depth in range(1,6):
    #for depth in range(1,6):
    depth = tdepth
    method = "entropy"
    if boost:
        noofboost = nummodels
        trainData = [x+[1] for x in trainData]
        #treelist = []
        for _ in range(noofboost):
            tree = dtree.buildtree(trainData, method, 0, depth,boost)
            #treelist.append(tree)
            #print dtree.classify(tree, testData, False)*100
            #print [x[-1] for x in trainData]
            trainData = dtree.classify(tree, trainData,boost)
        output = dtree.classify(tree, testData, False)
        print "accuracy is %f%%" %(float(output[0])*100)
        print "confusion matrix " +str(output[1])
    else:
        tree = dtree.buildtree(trainData,method,0,depth,boost=False)
        #print tree
        output = dtree.classify(tree, testData,boost)
        #print depth," depth." , "accuracy is %f%%" % (output[0]*100)
        #print "confusion matrix " +str(output[1])
        return tree

def create_bags(trainingData,noofbags):
    trainingData = parseFile(trainingData)
    datasize = len(trainingData)
    bags = []
    for _ in range(noofbags):
        item = [random.choice(trainingData) for _ in range(datasize)]
       #print item
        item2 = [tuple(x) for x in item]
        #print len(set(item2))
        bags.append(item)
        #print len(list(set(item)))
    return bags

def cal_accuracy(treeslist,testingData):
    correct = 0
    incorrect = 0
    TP=0;TN=0;FP=0;FN = 0
    testingData = parseFile(testingData)
    testingData = [x[:21]+x[22:] for x in testingData]
    for sample in testingData:
        results = []
        resultcount = {}
        for tree in treeslist:
            #results.append(dtree.validatation(tree, sample))
            results.append(dtree.validatation(tree, sample).keys()[0])
            #print dtree.validatation(tree, sample)
        #print results
        for result in results:
            #print result
            if result in resultcount:
                resultcount[result] += 1
            else:
                resultcount[result] = 1
        #print resultcount
        pointresult,count = max(resultcount.iteritems(),key=operator.itemgetter(1))
        #print pointresult,sample[20]
        if pointresult == sample[20]:
            if pointresult == 1:
                TP += 1
            else:
                TN += 1
            correct += 1
        else:
            if pointresult == 0:
                FN += 1
            else:
                FP += 1
            incorrect += 1
    #print correct,incorrect
    return correct/(correct+incorrect),[TN,FN,FP,TP]

def main():
    entype = sys.argv[1];
    # Get the depth of the trees
    tdepth = int(sys.argv[2]);
    # Get the number of bags or trees
    nummodels = int(sys.argv[3]);
    # Get the location of the data set
    datapath = sys.argv[4];
    #trainingSet= raw_input("Enter dataset file name")
    trainingData = "agaricuslepiotatrain1.csv"
    testingData = "agaricuslepiotatest1.csv"

    
    trainingData = os.path.join(datapath,trainingData)
#    print trainingData
    testingData = os.path.join(datapath,testingData)
#    print testingData
    #testingData = "testing_own.csv"
    #trainingData = parseFile(trainingData)
    #testingData = parseFile(testingData)
    if entype == 'boost':
        boost = True
        #boosting code
        trainingData = parseFile(trainingData)
        decisiontree(trainingData,testingData,tdepth,nummodels,boost=True)
    else:
        boost = False
        bags = create_bags(trainingData,nummodels)
        treeslist = []
        for bag in bags:
            #break
            treeslist.append(decisiontree(bag,testingData,tdepth,nummodels,boost=False))
        accuracy = cal_accuracy(treeslist,testingData)
        print "accuracy of boosting " + str(accuracy)




if __name__ == '__main__':
    main()
