import string

__author__ = 'bookcold'
# -*- coding:utf-8-*-
import os
import os.path
import re
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from  xml.dom import minidom
import urllib,urllib2,cookielib

for i in range(26,47):
#    url ="http://www.lixiaolai.com/archives/46"+str(i)+".html"
#
#    #url ="http://www.lixiaolai.com/archives/4628.html"
#
#    html = urllib2.urlopen(url)
#    soup=BeautifulSoup(html)
#    list = soup.find("div",{"id":"four-column-list"})
#
#    words= list.findAll("li")
    file = open('word.txt')
    words = file.readlines()

    for word in words:
        #print word.string

        #url2="http://dict.cn/ws.php?utf8=true&q="+word.string
        #url3="http://dict-co.iciba.com/api/dictionary.php?w="+word.string
        url2="http://dict.cn/ws.php?utf8=true&q="+word.rstrip()
        url3="http://dict-co.iciba.com/api/dictionary.php?w="+word.rstrip()

        tran = urllib.urlopen(url2)
        d= BeautifulStoneSoup(tran.read())
        e = d.find('def')
        if(e == None):
            continue
        stt = e.string
        if(stt.find('\n')):
            stt = e.string.replace('\n',' ')
        #ec = d.find('pron').string
        ps = urllib.urlopen(url3)
        pp = BeautifulStoneSoup(ps.read())
        pt = pp.find('ps')
        yinbiao=''
        if(pt != None):
             yinbiao = pt.string

        file  = open('kaobao.txt','a')
        #line  = word.string+': ['+yinbiao+'] '+stt+'\n'
        line  = word.rstrip()+': ['+yinbiao+'] '+stt+'\n'
        print line
        file.write(line.encode('utf-8'))
        file.close()

