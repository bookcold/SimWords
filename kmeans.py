__author__ = 'bookcold'

import MySQLdb
import numpy
import matplotlib
from scipy.cluster.vq import *
from hcluster import pdist,linkage,dendrogram
import pylab

def GetNum():
    documents = []
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='lbs',charset='utf8')
    cursor = conn.cursor()
    cursor.execute("""select * from lbs.UserDistance""")
    result = cursor.fetchall()
    for item in result:
       documents.append(item[1])
    return documents

num = numpy.array( [[float(x),float(x)] for x in GetNum()])
#whitened = whiten(num)
#res,idx = kmeans2(num,3)
#
#
#colors = ([([0,0,0],[1,0,0],[0,0,1])[i] for i in idx])
#pylab.scatter(num[:,0],num[:,1],c=colors)
#pylab.savefig('clust.png')
#pylab.show()

z=linkage(num,'single')
dendrogram(z,color_threshold=0)
