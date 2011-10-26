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

import os
import tempfile
from cgi import FieldStorage

from Box import Box
from Button import Button
from RawHTML import RawHTML
from Server import publish, get_scgi

HEADERS = [
    '<script type="text/javascript" src="/CTK/js/ajaxupload.3.6.js"></script>'
]

JS = """
var button = $('#%(id)s .button');
var msg    = $('#%(id)s .msg');

new AjaxUpload (button, {
  name:   'file',
  action: '%(upload_url)s',
  onSubmit: function (file, ext) {
     this.disable();
     msg.html('Uploading');

     interval = window.setInterval(function(){
	 var text = msg.html();
	 if (text.length < 13){
	    msg.html(text + '.');
	 } else {
	    msg.html('Uploading');
	 }
     }, 200);
  },
  onComplete: function (file, response) {
     window.clearInterval (interval);
     msg.html('');
     this.enable();
     $('#%(id)s').trigger ({'type':'upload_finished', 'filename': file});
  }
});
"""

# The internal POST Receiver and Storage classes are imported from
# CTK.Uploader().
#
from Uploader import UploadRequest


class AjaxUpload (Box):
    def __init__ (self, props={}, params=None, direct=True):
        Box.__init__ (self)

        self.id         = 'ajax_upload_%d'%(self.uniq_id)
        self._url_local = '/ajax_upload_%d' %(self.uniq_id)
        self.props      = props.copy()

        handler    = self.props.get('handler')
        target_dir = self.props.get('target_dir')

        # Widgets
        button = Button(_('Upload'))
        msg    = Box ({'class': 'msg'}, RawHTML(' '))

        self += button
        self += msg

        # Register the uploader path
        publish (self._url_local, UploadRequest,
                 handler=handler, target_dir=target_dir, params=params, direct=direct)

    def Render (self):
        props = {'id':         self.id,
                 'upload_url': self._url_local}

        render = Box.Render (self)
        render.headers += HEADERS
        render.js      += JS %(props)

        return render
