# -*- coding: utf-8 -*-

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from app.models import Article
from urllib2 import urlopen
from xml.etree import ElementTree as ET
import datetime


#@cache_page(60 * 60 * 12)
class WeatherPlugin(CMSPluginBase):
    model = CMSPlugin
    module = _('Weather Plugin')
    name = _('Погода')
    render_template = 'weather.html'
    cache = True

    def render(self, context, instance, placeholder):
        weather_list = {}
        try:
            output_file = open('/home/azimuth/.env/django/new/project/mysite/app/weather.xml','w')
            input_url = urlopen('http://xml.meteoservice.ru/export/gismeteo/point/112.xml')
            input_url_content = input_url.read()
            output_file.write(input_url_content)
            output_file.close()
            parse_file = open('/home/azimuth/.env/django/new/project/mysite/app/weather.xml', 'r')
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
            except:
                raise Exception('Изменился формат данных')

            for i in weather_list.values():
                for k, v in i.items():
                    if v.isdigit(): i[k] = int(v)

        except Exception as e:
            weather_list['e'] = e
            log_time = datetime.datetime.now()
            log = open('/home/azimuth/.env/django/new/project/mysite/app/weather_log.xml','a')
            log.write('{} : {}\n'.format(str(e), str(log_time.strftime("%d.%m.%Y %H:%M:%S"))))
            log.close()

        context.update({'instance': weather_list})
        return context

plugin_pool.register_plugin(WeatherPlugin)
