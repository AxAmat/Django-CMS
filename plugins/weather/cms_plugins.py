from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from app.models import Article
import os
from urllib2 import urlopen
from xml.etree import ElementTree as ET


class WeatherPlugin(CMSPluginBase):
    model = CMSPlugin
    module = _('Weather Plugin')
    name = _('Погода')
    render_template = 'weather.html'
    cache = True

    def render(self, context, instance, placeholder):
        weather_list = {}
        try:
            rss = open('/home/azimuth/.env/django/new/project/mysite/app/weather.xml','w')
            inpt = urlopen('http://xml.meteoservice.ru/export/gismeteo/point/112.xml')
            f = inpt.read()
            rss.write(f)
            rss.close()
            f = open('/home/azimuth/.env/django/new/project/mysite/app/weather.xml', 'r')
            tree = ET.parse(f)
            root = tree.getroot()

            for child in root.iter():
                weather_list[child.tag] = child.attrib
            for i in weather_list.values():
                for k, v in i.items():
                    if v.isdigit(): i[k] = int(v)
        except:
            pass

        context.update({'instance': weather_list})
        return context

plugin_pool.register_plugin(WeatherPlugin)
