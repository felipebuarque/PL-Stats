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

from Container import Container

HTML = """
<div id="%(id)s" class="indenter">
%(content)s
</div>
"""

class Indenter (Container):
    def __init__ (self, widget=None, level=1):
        Container.__init__ (self)
        self.level = level

        if widget:
            self += widget

    def Render (self):
        render = Container.Render (self)

        for n in range(self.level):
            render.html = HTML%({'id': self.id, 'content': render.html})

        return render
