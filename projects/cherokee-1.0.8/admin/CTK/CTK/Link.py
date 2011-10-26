# CTK: Cherokee Toolkit
#
# Authors:
#      Alvaro Lopez Ortega <alvaro@alobbs.com>
#
# Copyright (C) 2009 Alvaro Lopez Ortega
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from Widget import Widget
from Container import Container
from util import formater, props_to_str

LINK_HTML      = '<a href="%(href)s" id="%(id)s" %(props)s>%(content)s</a>'
LINK_ICON_HTML = '<div id="%(id)s"><span class="ui-icon ui-icon-%(icon)s"></span>%(link)s</div>'


class Link (Container):
    def __init__ (self, href, content=None, props={}):
        Container.__init__ (self)
        self.href  = href[:]
        self.props = props.copy()

        if 'id' in self.props:
            self.id = self.props.pop('id')

        if content:
            self += content

    def Render (self):
        render = Container.Render (self)

        props = {'id':      self.id,
                 'href':    self.href,
                 'props':   props_to_str(self.props),
                 'content': render.html}

        render.html = formater (LINK_HTML, props)
        return render


class LinkWindow (Link):
    def __init__ (self, href, content=None, props={}):
        self.props = props.copy()
        props['target'] = '_blank'

        Link.__init__ (self, href, content, props)


class LinkIcon (Link):
    def __init__ (self, href="#", icon='newwin', content=None):
        Link.__init__ (self, href)
        self.icon = icon

        if content:
            self += content

    def Render (self):
        render = Link.Render (self)

        props = {'id':   self.id,
                 'icon': self.icon,
                 'link': render.html}

        render.html = formater (LINK_ICON_HTML, props)
        return render

