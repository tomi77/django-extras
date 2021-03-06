from django.template import Library
from django.utils.dateparse import parse_date, parse_datetime, parse_duration, parse_time

register = Library()


register.filter('parse_datetime', parse_datetime, expects_localtime=True)
register.filter('parse_date', parse_date, expects_localtime=True)
register.filter('parse_time', parse_time, expects_localtime=True)
register.filter('parse_duration', parse_duration)
