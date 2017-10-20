# -*- coding: UTF-8 -*-


__author__ = 'Ivan'



class Pagination():
    def __init__(self,total_count,page_index,page_size,items):
        self.totalCount=total_count
        self.pageIndex = page_index

        self.pageSize = page_size
        self.totalPage=self.pages()
        self.datas = items



    def pages(self):

        if self.totalCount<=0:
            return 0

        if self.totalCount % self.pageSize >0:
            return  (self.totalCount/self.pageSize) +1;

        else:
            return  self.totalCount /self.pageSize

