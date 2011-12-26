__author__ = 'bookcold'
# -*- coding:utf-8-*-


class Word:
    def __init__(self,word='',type=''):
        self.word = word
        self.type = type
        self.other_primitives = []
        self.relational_primitive = {}
        self.relational_symbol_primitives = {}
        self.structural_words= []

    def __get_word__(self):
        return self.word

    def __get_type__(self):
        return self.type

    def __set_word__(self,word):
        self.word = word

    def __set_type__(self,type):
        self.type = type

    def __set_first_primitive__(self,first_primitive):
        self.first_primitive = first_primitive

    def __set_other_primitive__(self,other_primitives):
        self.other_primitives.append(other_primitives)

    def __set_structure_word__(self,word):
        self.structural_words.append(word)

    def __add_relational_primitive__(self,key,value):
        list = self.relational_primitive.get(key)
        if list is None:
            list = []
            list.append(value)
            self.relational_primitive[key] = list
        else:
            list.append(value)

    def __add_relational_symbol_primitive__(self,key,value):
        list = self.relational_symbol_primitives.get(key)
        if list is None:
            list = []
            list.append(value)
            self.relational_symbol_primitives[key]=list
        else:
            list.append(value)

    def __is_structural_word__(self):
        if len(self.structural_words) == 0:
            return False
        else:
            return True




    @staticmethod
    def loadGlossary():
        file = open("dic/glossary.dat")
        for line in file:
            list =  line.strip().replace("\t","").split("  ")
            name = list[0]
            type = ''
            print(list[0],list[-1])
            for word in list:
                if(word != ''):
                    type = word
            