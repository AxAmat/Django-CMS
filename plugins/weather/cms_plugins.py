# -*- coding: utf-8 -*-

"""
Created on 04.08.2016
:author: Алексей

Плагин погоды
"""


import logging
import traceback

from urllib2 import urlopen
from xml.etree import ElementTree as ET

from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin


logging.basicConfig(
    filename='blog/weather.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

"""
URL - адрес источника данных о погоде;
KEYS - список ключей, для формирования словаря с параметрами погодных условий.
"""

URL = 'http://xml.meteoservice.ru/export/gismeteo/point/112.xml'
KEYS = ['HEAT', 'PRESSURE', 'WIND', 'PHENOMENA']


class WeatherPlugin(CMSPluginBase):
    model = CMSPlugin
    module = _('Weather Plugin')
    name = _('Погода')
    render_template = 'weather.html'
    cache = True

    def render(self, context, instance, placeholder):

        weather_list = {}

        """
        Парсим содержимое URL, в ходе итерации добавляем в словарь значения, соответствующие ключам сз списка KEYS.
        В случае несоответствия длины словаря ожидаемому результату (4), выбрасываем KeyError.
        Меняем строковое представление чисел на int.
        """

        try:
            input_url = urlopen(URL)
            root = ET.fromstring(input_url.read())

            weather_list = {child.tag: child.attrib for child in root.iter() if child.tag in KEYS}

            if len(weather_list) < 4:
                raise KeyError

            for i in weather_list.values():
                for k, v in i.items():
                    if v.isdigit():
                        i[k] = int(v)

            """
            В случае вощникновения исключительных ситуаций, объект исключения передаётся
            в шаблон и логируется в файл blog/weather.log
            """

        except Exception as e:
            weather_list['except'] = e
            logging.error(traceback.format_exc(e))

        context.update({'instance': weather_list})
        return context

plugin_pool.register_plugin(WeatherPlugin)
