__author__ = 'bookcold'
# -*- coding:utf-8-*-
from  xml.dom import minidom
from BeautifulSoup import BeautifulStoneSoup
import urllib,urllib2
import os
import os.path
#url2="http://dict.cn/ws.php?utf8=true&q=abandon"
url2="http://dict-co.iciba.com/api/dictionary.php?w=abandon"
print url2
tran = urllib.urlopen(url2)
#print tran

d= BeautifulStoneSoup(tran.read())
e = d.find('ps')
print e.string
#str = e.string.replace('\n',' ')

#file  = open('words.txt','a')
#file.write("abandon:"+str.encode('UTF-8')+'\n')
#file.close()



