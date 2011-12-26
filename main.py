# -*- coding:utf-8-*-
__author__ = 'bookcold'


import MySQLdb
import SimWords
import Primitive
import numpy
import munkres
from hcluster import *
from matplotlib.pyplot import show
import sys


def LoadLocationWords():
    documents = []
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='lbs',charset='utf8')
    cursor = conn.cursor()

    cursor.execute('select distinct(UsrID) from User where IsCrawlDetail = 1 order by CheckInNum  desc limit 50')
    result = cursor.fetchall()
    for r in result:
        term = ''
        cursor.execute("""select Words from lbs.Location l
                            inner join (
                            select LocationID, count(LocationID) num from lbs.UsrLocation  where UsrID = '%s'
                            group by LocationID
                            order by num desc
                            limit 50
                            ) ul
                            on l.LocationID = ul.LocationID""" % r[0])
        Items = cursor.fetchall()
        for item in Items:
            if(item[0]):
                term += item[0]
                
        documents.append(term)
        #print(documents)
    cursor.close()
    conn.close()
    return documents

def InsertDistanceToSql(dis):
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='lbs',charset='utf8')
    cursor = conn.cursor()
    cursor.execute("""insert into lbs.UserDistance (Distance) value (%f) """ %dis)
    cursor.close()
    conn.close()

def GetWordList():
    DistanceMatrix = []
    documents = LoadLocationWords()
    for base in range(len(documents)):
        DistanceVector = []
        base_words = documents[base].split(None)
        i = 0
        while(i< base):
            DistanceVector.append(0)
            i = i+1
        while(i<len(documents)):
        #for doc in documents:
            doc = documents[i]
            if not base_words:
                DistanceVector.append(-1)
                i = i+1
                continue
            if not doc:
                DistanceVector.append(-1)
                i = i+1
                continue
            words = doc.split(None)
            #GetHungarianValue(WordsSimilarity(base,words))
            matrix12, matrix21 = WordsSimilarity(base_words,words)
            index12 = GetHungarianValue(matrix12)
            index21 = GetHungarianValue(matrix21)
            num12,value12 = GetWordDistance(index12,matrix12)
            num21,value21 = GetWordDistance(index21,matrix21)
            distance = -1
            if(value21+value12!=0) :
                distance = (num12 + num21)/(value12+value21)
            DistanceVector.append(distance)
            i = i+1
            #InsertDistanceToSql(distance)
        print (DistanceVector)
        DistanceMatrix.append(DistanceVector)
    return DistanceMatrix

def WordsSimilarity(list1,list2):
    #print(list1)
    #print(list2)
    words_sim_matrix_12=[]
    words_sim_matrix_21=[]
    for w1 in list1:
        vector = []
        for w2 in list2:
            if(w1 == w2):
                sim =1
            else:
                sim = SimWords.WordSimilarity.SimWord(w1,w2)
            vector.append(sim)
        words_sim_matrix_12.append(vector)

    for w1 in list2:
        vector = []
        for w2 in list1:
            if(w1 == w2):
                sim = 1
            else:
                sim = SimWords.WordSimilarity.SimWord(w1,w2)
            vector.append(sim)
        words_sim_matrix_21.append(vector)

    return words_sim_matrix_12, words_sim_matrix_21


def GetHungarianValue(words_sim_matrix):
    m = munkres.Munkres()
    matrix = []
    #munkres.make_cost_matrix(words_sim_matrix,lambda cost:1 - cost)
    for row in words_sim_matrix:
        cost_row = []
        for col in row:
            cost_row.append(1-col)
        matrix.append(cost_row)

    indexes = m.compute(matrix)
    return indexes
    #print_matrix(words_sim_matrix)
#    total = 0
#    for row,column in indexes:
#        value = words_sim_matrix[row][column]
#        total +=value
#        print ('(%f, %f) -> %f' %(row, column, value))
#    print ('total cost: %f' % total)

def GetWordDistance(indexes,matrix):
    num = 0
    value = 0
    for row,column in indexes:
        v = matrix[row][column]
        value +=v
        num +=1
    return num,value




            
    


if __name__ == "__main__":
    Primitive.Primitive.Load_Primitive()
    SimWords.WordSimilarity.LoadGlossary()
    #print(SimWords.WordSimilarity.SimWord("男人","女人"))
#    print("Close")
    #LoadLocationWords()

    #DistanceMatrix = numpy.array(GetWordList())
    DistanceMatrix = numpy.matrix(GetWordList())
    #DistanceMatrix  = numpy.invert(DistanceMatrix)
    z = linkage(DistanceMatrix.I)
    print z
    dendrogram(z)
    show()


#    matrix = [[0.4, 0.15, 0.4],
#              [0.4, 0.45, 0.6],
#              [0.3, 0.225,0.3]]
#    m = Hungarian.Munkres()
#    indexes = m.compute(matrix)
#    Hungarian.print_matrix(matrix)
#    total = 0
#    for row,column in indexes:
#        value = matrix[row][column]
#        total +=value
#        print ('(%f, %f) -> %f' %(row, column, value))
#    print ('total cost: %f' % total)