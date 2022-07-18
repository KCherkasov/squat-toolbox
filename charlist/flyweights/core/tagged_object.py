# -*- coding: utf-8 -*-


class TaggedObject(object):
    def __init__(self, tag=''):
        self.__tag = tag

    def get_tag(self):
        return self.__tag
