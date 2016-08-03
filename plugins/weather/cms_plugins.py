# -*- coding: utf-8 -*-

import datetime
import logging
import traceback
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from urllib2 import urlopen
from xml.etree import ElementTree as ET

logging.basicConfig(
    filename = 'mysite/app/weather.log',
    level = logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )


class WeatherPlugin(CMSPluginBase):
    model = CMSPlugin
    module = _('Weather Plugin')
    name = _('Погода')
    render_template = 'weather.html'
    cache = True

    def render(self, context, instance, placeholder):
        weather_list = {}
        url = 'http://xml.meteoservice.ru/export/gismeteo/point/112.xml'
        weather_xml = 'mysite/app/weather.xml'
        try:
            output_file = open(weather_xml,'w')
            input_url = urlopen(url)
            input_url_content = input_url.read()
            output_file.write(input_url_content)
            output_file.close()
            parse_file = open(weather_xml, 'r')
            tree = ET.parse(parse_file)
            root = tree.getroot()
            parse_file.close()

            for child in root.iter():
                weather_list[child.tag] = child.attrib

            try:
                weather_list['HEAT']
                weather_list['PRESSURE']
                weather_list['WIND']
                weather_list['PHENOMENA']
            except (KeyError, AttributeError) as e:
                raise Exception(e)

            for i in weather_list.values():
                for k, v in i.items():
                    if v.isdigit(): i[k] = int(v)

        except Exception as e:
            weather_list['except'] = e
            logging.error(traceback.format_exc(e))

        context.update({'instance': weather_list})
        return context

plugin_pool.register_plugin(WeatherPlugin)

