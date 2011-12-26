__author__ = 'bookcold'
# -*- coding:utf-8-*-


class Primitive:
    All_Primitive = {}
    Word_ID = {}
    def __init__(self,id=0,parent_id=0,primitive=''):
        self.id = id
        self.parent_id = parent_id
        self.primitive = primitive

    def __get_primitive__(self):
        return self.primitive

    def __get_id__(self):
        return self.id

    def __get_parent_id__(self):
        return self.parent_id

    def __is_top_primitive(self):
        return self.id == self.parent_id

    @staticmethod
    def is_Primitive(primitive):
        if Primitive.Word_ID.get(primitive):
            return True
        else:
            return False


    @staticmethod
    def Load_Primitive():
        file = open("dic/WHOLE.DAT")
        for line in file:
            word_list = line.strip().split(" ")
            id = word_list[0]
            primitive = word_list[2]
            name = primitive.split("|")
            parent_id = word_list[-1]
            Primitive.All_Primitive[id] = Primitive(id,parent_id,primitive)
            Primitive.Word_ID[name[0]]= id
            Primitive.Word_ID[name[1]]=id

    @staticmethod
    def Get_Parents_Primitive(primitive):
        Parents_ID = []
        id = Primitive.Word_ID.get(primitive);
        if (id != None):
            parent = Primitive.All_Primitive.get(id)
            Parents_ID.append(id)
            while(not parent.__is_top_primitive()):
                Parents_ID.append(parent.__get_parent_id__())
                parent = Primitive.All_Primitive.get(parent.__get_parent_id__())
        return Parents_ID
            



    
