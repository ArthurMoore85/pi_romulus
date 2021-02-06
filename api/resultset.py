# -*- coding: utf-8 -*-
"""
.. module:: .result.py
    :synopsis: ResultSet and ResultItem classes

.. moduleauthor:: Arthur Moore <arthur.moore85@gmail.com>
.. creation date:: 04-11-2017
.. licence:: 
"""
from __future__ import unicode_literals

from api.resultitem import ResultItem

__author__ = "arthur"


class ResultSet(object):
    """
    ResultSet object.
    """

    def __init__(self, *args, **kwargs):
        self._raw_item_objects = kwargs.get('results', [])
        self._caller = kwargs.get('caller', None)
        self._item_objects = self._create_objects()

    def _get_download_id(self, url):
        """
        Returns a Download ID if possible (Emuparadise)
        """
        code = url.split('/')[-1]
        try:
            return int(code)
        except ValueError:
            return None

    def _create_objects(self):
        """
        Converts results list into ResultItem set.
        """
        objs = []
        count = 0

        for item, values in self._raw_item_objects.items():
            download_id = values['download_id']
            download_url = values['game_link']
            objs.append(ResultItem(id=count, download_url=download_url, name=values['game_name'],
                                   system_id=0, system=values['system_name'], download_id=download_id,
                                   filesize='NA', token=self._caller.token))
            count += 1
        return set(objs)

    def first(self):
        """
        Returns the first ResultItem object.
        """
        return list(self._item_objects)[0]

    def last(self):
        """
        Returns the last ResultItem object.
        """
        return list(self._item_objects)[-1]

    def all(self):
        """
        Returns all the ResultItems
        """
        return self._item_objects

    def filter(self, system_id=None, system=None):
        """
        Filters the ResultSet.
        """
        results = []
        for item in self._item_objects:
            if system_id:
                results.append(item) if item.system_id == system_id else None
            if system:
                results.append(item) if item.system == system else None

        results = set(results)
        if not results:
            results = self._item_objects

        return results
