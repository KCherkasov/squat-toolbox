# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class BaseCommand:
    __metaclass__ = ABCMeta

    def __init__(self, name, args):
        self.__name = name
        self.__args = args

    def get_name(self):
        return self.__name

    def get_args(self):
        return self.__args

    @abstractmethod
    def handle(self, args=None):
        pass
