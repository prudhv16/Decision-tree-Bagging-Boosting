from __future__ import division
from math import log
import operator


# class node to create instances

class Node:
    def __init__(self,feature=None,splitVal=None,results=None,LNode=None,RNode=None):
        self.feature=feature # column index of criteria being tested
        self.splitVal=splitVal # value necessary to get a true result
        self.results=results # dict of results for a node, None for everything except endpoints
        self.LNode=LNode
        self.RNode=RNode

# checking the efficiency of the split

def classify(tree, test_set,boost):
    correct = 0
    incorrect = 0
    TP=0;TN=0;FP=0;FN = 0
    for sample in test_set:
        #print sample[20],validatation(tree, sample)
        if validatation(tree, sample).get(sample[20]):
            if boost:
                sample[-1] -= sample[-1]/2
            else:
                correct += 1
                if sample[20] == 1:
                    TP += 1
                else:
                    TN += 1
        else:
            if boost:
                sample[-1] += sample[-1] / 2
            else:
                incorrect += 1
                if sample[20] == 1:
                    FN += 1
                else:
                    FP += 1
    if boost:
        return test_set
    else:
        return correct/(correct+incorrect),[TN,FN,FP,TP]


# splitting the data into right and left (yes OR NO)

def dataSplit(rows,column,value):
    leftSub =[]
    RightSub =[]

    for individualRow in rows:
        #Remove this code
        if isinstance(value,int) or isinstance(value,float):
            if individualRow[column] >= value:
                leftSub.append(individualRow)
            else:
                RightSub.append(individualRow)
        else:
            if individualRow[column] == value:
                leftSub.append(individualRow)
            else:
                RightSub.append(individualRow)


    return leftSub,RightSub


def attrValid(individualRow,column,value):

    if isinstance(value,int) or isinstance(value,float):
        if individualRow[column] >=value:
            return True
        else:
            return False
    else:
        if individualRow[column]== value:
            return True
        else:
            return False

# function to calculate entropy

def entropy(overallRows,boost):
    #print overallRows[0][21]
    numRows = len(overallRows)
    #print(numRows)
    catDict = {}
    curEntropy = 0.0
    if boost:
        for individualRow in overallRows:
            catDict.setdefault(individualRow[20], 0)
            catDict[individualRow[20]] += individualRow[-1]
        for value in catDict.values():
            #print(value)
            prob = value/numRows
            curEntropy -= prob * log(prob, 2)
    else:
        for individualRow in overallRows:
            catDict.setdefault(individualRow[20], 0)
            catDict[individualRow[20]] += 1
        for value in catDict.values():
            prob = value/numRows
            curEntropy -= prob * log(prob, 2)
    return curEntropy



# function to find the best attribute to split on


#Remove gain from this call
def findfeature(overallRows,gain,boost,class_index =-1):
    #print overallRows[20]
    numFeatures = len(overallRows[0])
    maximumGain =0.0
    bestAttribute = None
    bestsubsets = None
    best_left =[]
    best_right=[]
    gainCoeffecient = entropy
    if boost:
        numFeatures = numFeatures -1

    current_score = gainCoeffecient(overallRows,boost)
    for attribute in range(numFeatures):
        if attribute == 20:
            continue
        VarSet = set()
        for individualRow in overallRows:
            VarSet.add(individualRow[attribute])
        VarList = list(VarSet)
        VarList.sort()

        for th in VarList:
            leftSub, RightSub = dataSplit(overallRows, attribute, th)
            probLower = float(len(leftSub)) / len(overallRows)
            probGreater =float(len(RightSub))/len(overallRows)
            gain1 = current_score - (probLower*gainCoeffecient(leftSub,boost)) - (probGreater*gainCoeffecient(RightSub,boost))
            if gain1 > maximumGain and len(leftSub) > 0 and len(RightSub) > 0:
                maximumGain = gain1
                bestAttribute = (attribute, th)
                best_left = leftSub[:]
                best_right = RightSub[:]
    return maximumGain,bestAttribute,best_left,best_right


def majority_count(rows,class_index =20):
    BClass = None
    Bvalue =0
    class_count ={}
    #print rows[:1]
    for row in rows:
        class_count.setdefault(row[class_index],0)
        #print row[class_index]
        class_count[row[class_index]]+=1
    #print class_count
    BClass,Bvalue = max(class_count.iteritems(),key=operator.itemgetter(1))
    #print BClass,Bvalue
    #print class_count
    #print BClass,Bvalue
    return BClass,Bvalue

# function to build tree based on best attribute

def buildtree(overallRows,gain,currentHeight,requiredHeight,boost):
    Tree = Node()
    length_data = len(overallRows)
    #print overallRows[:1]
    parent_class,parent_value = majority_count(overallRows)
    classLabels = []
    #further changes for mushroom data.
    for row in overallRows:
        classLabels.append(row[20])
    #print classLabels[:1]
    if length_data == 0:
        return Tree

    if currentHeight == requiredHeight :
         return Node(results = {parent_class:parent_value})
    #print(classLabels)
    #check elif or or
    if len(set(classLabels)) == 1:
        return Node(results = {parent_class:parent_value})

    maximumGain,best_attribute,best_left,best_right = findfeature(overallRows,gain,boost)
    #print("maxGain:",maximumGain,"best_attribute:",best_attribute,"best_left:",best_left,"best_right:",best_right)
    left_child = buildtree(best_left,gain,currentHeight+1,requiredHeight,boost)
    right_child = buildtree(best_right,gain,currentHeight+1,requiredHeight,boost)
    return Node(feature=best_attribute[0], splitVal=best_attribute[1], LNode=left_child, RNode=right_child)

# tree validation

def validatation(tree,data):
    temp = tree
    #print data
    while temp.results == None:
        if attrValid(data,temp.feature,temp.splitVal):
            temp = temp.LNode
        else:
            temp = temp.RNode
    return temp.results
