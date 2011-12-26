# -*- coding:utf-8-*-
from hcluster import *
from matplotlib.pyplot import show
import numpy
from numpy.random import rand

#y = [[0, 206, 429 ,1504],
#     [206,0,233,1308],
#     [429,233,0,1075],
#     [1504,1308,1075,0]]
#y = [[0, 0, 0 ,0],
#     [429,0,0,0],
#     [233,206,0,0],
#     [1504,1308,1075,0]]
#
#z = linkage(y)
#print z
#dendrogram(z)
#show()


for i in range(27,36):
    url ="http://www.lixiaolai.com/archives/46"+str(i)+".html"
    print url