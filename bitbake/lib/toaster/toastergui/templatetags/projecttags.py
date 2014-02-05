#
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# BitBake Toaster Implementation
#
# Copyright (C) 2013        Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from datetime import datetime, timedelta
from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def time_difference(start_time, end_time):
    return end_time - start_time

@register.filter(name = 'sectohms')
def sectohms(time):
    try:
        tdsec = int(time)
    except ValueError:
        tdsec = 0
    hours = int(tdsec / 3600)
    return "%02d:%02d:%02d" % (hours, int((tdsec - (hours * 3600))/ 60), int(tdsec) % 60)

@register.assignment_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)

@register.filter
def divide(value, arg):
    if int(arg) == 0:
        return -1
    return int(value) / int(arg)

@register.filter
def multiply(value, arg):
    return int(value) * int(arg)

@register.assignment_tag
def datecompute(delta, start = timezone.now()):
    return start + timedelta(delta)


@register.filter(name = 'sortcols')
def sortcols(tablecols):
    return sorted(tablecols, key = lambda t: t['name'])

@register.filter
def task_color(task_object):
    """ Return css class depending on Task execution status and execution outcome
    """
    if not task_object.task_executed:
        return 'class=muted'
    elif task_object.get_outcome_display == 'Failed':
        return 'class=error'
    else:
        return ''

@register.filter
def filtered_icon(options, filter):
    """Returns btn-primary if the filter matches one of the filter options
    """
    for option in options:
        if filter == option[1]:
            return "btn-primary"
    return ""

@register.filter
def filtered_tooltip(options, filter):
    """Returns tooltip for the filter icon if the filter matches one of the filter options
    """
    for option in options:
        if filter == option[1]:
            return "Showing only %s"%option[0]
    return ""

@register.filter
def format_none_and_zero(value):
    """Return empty string if the value is None, zero or Not Applicable
    """
    return "" if (not value) or (value == 0) or (value == "0") or (value == 'Not Applicable') else value
