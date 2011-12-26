__author__ = 'bookcold'
# -*- coding:utf-8-*-
import Primitive
import Word


class WordSimilarity:
    RELATIONAL_SYMBOL = "#%$*+&@?!"

    SPECIAL_SYMBOL = "{"

    Default_Primitive_Dis = 20

    Logical_Symbol = ',~^'

    ALL_WORDS = {}

    alpha = 1.6
    beta1 = 0.5
    beta2 = 0.2
    beta3 = 0.17
    beta4 = 0.13
    gamma = 0.2
    delta = 0.2



    @staticmethod
    def LoadGlossary():

        file = open("dic/glossary.dat")
        for line in file:
            list =  line.strip().replace("\t","").split("  ")
            w = Word.Word()
            #print(list[0],list[-1])

            for word in list[1:]:
                if(word != ''):
                    #w = Word.Word(list[0],word)
                    w.__set_word__(list[0])
                    w.__set_type__(word)
                    break
            WordSimilarity.GetWordDetail(list[-1],w)
            WordSimilarity.AddWord(w)

    @staticmethod
    def GetWordDetail(detail,word):
        isFirst = True
        isRelational = False
        isSymbol = False
        chinese = ''
        relationalPrimitiveKey = ''
        symbolKey = ''
        list = detail.split(',')
        for item in list:
            #具体词以括号表示
            if item.startswith('('):
                item = item[1:-2]

            if item.find('=') != -1 :
                isRelational = True
                strs = item.split('=')
                relationalPrimitiveKey = strs[0]
                value = strs[1].split('|')[1]
                word.__add_relational_primitive__(relationalPrimitiveKey,value)
                continue

            strs = item.split('|')
            type = WordSimilarity.GetStaticType(strs[0])

            if len(strs) > 1 :
                chinese = strs[1]
            if chinese != '' and (chinese.endswith(')') or chinese.endswith('}')):
                chinese = chinese[:-2]

            if type == 0:
                if isRelational:
                    word.__add_relational_primitive__(relationalPrimitiveKey,chinese)
                    continue
                if isSymbol:
                    word.__add_relational_symbol_primitive__(symbolKey,chinese)
                    continue
                if isFirst:
                    word.__set_first_primitive__(chinese)
                    isFirst = False
                    continue
                else:
                    word.__set_other_primitive__(chinese)
                    continue
            if type ==1:
                isSymbol = True
                isRelational = False
                symbolKey = strs[0][0]
                word.__add_relational_symbol_primitive__(symbolKey,chinese)
                continue
            if type ==2:
                if strs[0].startswith('{'):
                    english = strs[0][1::]
                    if chinese != '':
                        word.__set_structure_word__(chinese)
                        continue
                    else:
                        word.__set_structure_word__(english)
                        continue


                
                
    @staticmethod
    def GetStaticType(str):
        first = str[0]
        if WordSimilarity.RELATIONAL_SYMBOL.find(first)!=-1:
            return 1
        if WordSimilarity.SPECIAL_SYMBOL.find(first)!=-1:
            return 2
        return 0

    @staticmethod
    def AddWord(w):
        list = WordSimilarity.ALL_WORDS.get(w.__get_word__())
        if list is None:
            list = []
            list.append(w)
            WordSimilarity.ALL_WORDS[w.__get_word__()] = list
        else:
            list.append(w)

    @staticmethod
    def SimWord(word1,word2):
        list1 = WordSimilarity.ALL_WORDS.get(word1);
        list2 = WordSimilarity.ALL_WORDS.get(word2);
        if list1 != None and list2 != None:
            max = 0
            for w1 in list1:
                for w2 in list2:
                    sim = WordSimilarity.simWord(w1,w2)
                    max = (sim > max and sim) or max
            return max
        else:
            #print("其中有词没有被收录")
            return 0

    @staticmethod
    def simWord(w1,w2):
        if(w1.__is_structural_word__()!=w2.__is_structural_word__()):
            return 0
        if(w1.__is_structural_word__() and w2.__is_structural_word__()):
            l1 = w1.structural_words
            l2 = w2.structural_words
            return WordSimilarity.simList(l1,l2)
        if(not w1.__is_structural_word__() and not w2.__is_structural_word__() ):
            firstPrimitive1 = w1.first_primitive
            firstPrimitive2 = w2.first_primitive
            sim1 = WordSimilarity.simPrimitive(firstPrimitive1,firstPrimitive2)
            l1 = w1.other_primitives
            l2 = w2.other_primitives
            sim2 = WordSimilarity.simList(l1,l2)
            dic1 = w1.relational_primitive
            dic2 = w2.relational_primitive
            sim3 = WordSimilarity.simDic(dic1,dic2)
            dic1 = w1.relational_symbol_primitives
            dic2 = w2.relational_symbol_primitives
            sim4 = WordSimilarity.simDic(dic1,dic2)
            product = sim1
            sum = WordSimilarity.beta1 * product
            product *=sim2
            sum += WordSimilarity.beta2*product
            product *=sim3
            sum += WordSimilarity.beta3*product
            product *=sim4
            sum +=WordSimilarity.beta4*product
            return sum

            
    @staticmethod
    def simDic(dic1,dic2):
        if not dic1 and not dic2:
            return 1
        if not dic1 or not dic2:
            return WordSimilarity.delta
        total = len(dic1.keys()) + len(dic2.keys())
        sim = 0
        count = 0
        for key in dic1:
            if dic2.get(key) != None:
                l1 = dic1.get(key)
                l2 = dic2.get(key)
                sim += WordSimilarity.simList(l1,l2)
                count+=1
        return (sim + WordSimilarity.delta*(total -2*count))/ (total - count)

    @staticmethod
    def simList(l1,l2):
        if not l1 and not l2:
            return 1
        m = len(l1)
        n = len(l2)
        big = m if m > n else n
        N = m if m < n else n
        count = 0

        sum = 0
        while count < N:
            max = 0
            index1 = 0
            index2 = 0
            for i in range(len(l1)):
                for j in range(len(l2)):
                    sim = WordSimilarity.innerSimWord(l1[i],l2[j])
                    if sim > max:
                        index1 = i
                        index2 = j
                        max = sim
            sum +=max
            l1.remove(l1[index1])
            l2.remove(l2[index2])
            count+=1
        return (sum+WordSimilarity.delta*(big - N))/big

    @staticmethod
    def innerSimWord(w1,w2):
        if Primitive.Primitive.is_Primitive(w1) and Primitive.Primitive.is_Primitive(w2):
            return WordSimilarity.simPrimitive(w1,w2)
        if not Primitive.Primitive.is_Primitive(w1) and not Primitive.Primitive.is_Primitive(w2):
            if w1 == w2:
                return 1
            else:
                return 0
        return WordSimilarity.gamma

    @staticmethod
    def simPrimitive(p1,p2):
        dis = WordSimilarity.disPrimitive(p1,p2)
        return WordSimilarity.alpha/(dis + WordSimilarity.alpha)

    @staticmethod
    def disPrimitive(p1,p2):
        l1 = Primitive.Primitive.Get_Parents_Primitive(p1)
        l2 = Primitive.Primitive.Get_Parents_Primitive(p2)
        for item in l1:
            if item in l2:
                index  = l2.index(item)
                return index + l1.index(item)
        return WordSimilarity.Default_Primitive_Dis



                    

                




        