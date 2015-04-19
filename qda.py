from liblo import *
import sys
import datetime
import time
import numpy as np
import pickle

def qdaLearn(X,Y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmats - A list of k d x d learnt covariance matrices for each of the k classes
    print X.shape
    print Y.shape
    # IMPLEMENT THIS METHOD
    Y = Y.reshape(Y.size)
    covmats = np.zeros((np.unique(Y).size, X.shape[1], X.shape[1]))
    for i in range(2):
		covmats[i, :] = np.cov(X[Y==i], rowvar=0) 
    
    means =  np.zeros((2,X.shape[1]))
    for i in range(2):
    	# print np.mean(X[(Y==i).reshape((Y==i).size),:], 0) 
		means[i,:] = np.mean(X[(Y==i).reshape((Y==i).size),:], 0) 
    return means,covmats



def qdaTest(means,covmats,xtest,ytest):
    # Inputs
    # means, covmats - parameters of the QDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    
    # IMPLEMENT THIS METHOD
    predict = np.zeros((xtest.shape[0], 2))
    for i in range(0,2):
	   	xtestSubtract = xtest - means[i,:]
	   	invCov = np.linalg.inv(covmats[i,:])
	   	det = np.linalg.det(covmats[i,:])
	   	predict[:, i] = np.divide(1, np.sqrt(2 * np.pi) * det * det) * np.power(np.e, -0.5 * np.sum(np.multiply(np.dot(xtestSubtract, invCov), xtestSubtract), 1))
    
    finalOutput = np.argmax(predict, 1)
    ytest = ytest.reshape(ytest.size)
    qdaAccuracy = 100 * np.mean((finalOutput == ytest).astype('float'))    
    # for i in range(750,800):
    # 	print finalOutput[i], ' ', str(ytest[i])
    print np.sum(finalOutput)
    print np.sum(ytest)
    return qdaAccuracy

def qdapredict(means,covmats,xtest):
    # Inputs
    # means, covmats - parameters of the QDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    
    # IMPLEMENT THIS METHOD
    print xtest
    predict = np.zeros((xtest.shape[0], 2))
    for i in range(0,2):
	   	xtestSubtract = xtest - means[i,:]
	   	invCov = np.linalg.inv(covmats[i,:])
	   	det = np.linalg.det(covmats[i,:])
	   	predict[:, i] = np.divide(1, np.sqrt(2 * np.pi) * det * det) * np.power(np.e, -0.5 * np.sum(np.multiply(np.dot(xtestSubtract, invCov), xtestSubtract), 1))
    print predict.shape
    print "ABOUVE SHAPE VALUE"
    finalOutput = np.argmax(predict, 1)
    
    if np.sum(finalOutput) > finalOutput.shape[0]/2.0:
    	return "happy"
    return "sad"

limit = 700
sad_file = open('beta_sad.pickle', 'rb')
happy_file = open('beta_happy.pickle', 'rb')
sad = pickle.load(sad_file)
happy = pickle.load(happy_file)
sd = np.hstack(((sad[0])[:limit,:], (sad[1])[:limit,:]))
hp = np.hstack(((happy[0])[:limit,:], (happy[1])[:limit,:]))
train = np.concatenate((sd, hp))
label = np.zeros((sd.shape[0] + hp.shape[0], 1))
label[limit:,0] = 1
# label[1498:,0] = 1

inputSize = range(train.shape[0])
        #inputSize = 5000
#train.shape[0] - validation_size  
validation_size = 200
randomIndex = np.random.permutation(inputSize)
vData = train[randomIndex[0:validation_size],:]
tData = train[randomIndex[validation_size:],:]
validation_data = vData
validation_label = label[randomIndex[0:validation_size],:]
# true_label[:,i] = 1;
#validation_label = np.concatenate((validation_label, np.zeros((1000,1)) + i))
# validation_label = np.concatenate((validation_label, true_label))
train_data = tData
train_label = label[randomIndex[validation_size:],:]
# sd = np.hstack(((sad[0])[:700,:], (sad[1])[:700,:]))
# hp = np.hstack(((happy[0])[:700,:], (happy[1])[:700,:]))
# train = np.concatenate((sd, hp))
# label = np.zeros((1400, 1))
# label[700:,0] = 1

X = train_data
y = train_label
means,covmats = qdaLearn(X,y)
qdaacc = qdaTest(means,covmats,X,y)
print('QDA Accuracy Train Data= '+str(qdaacc))

X = validation_data
y = validation_label
means,covmats = qdaLearn(X,y)
qdaacc = qdaTest(means,covmats,X,y)
print('QDA Accuracy Train Data= '+str(qdaacc))
