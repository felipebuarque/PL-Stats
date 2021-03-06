# Cheroke Admin
#
# Authors:
#      Alvaro Lopez Ortega <alvaro@alobbs.com>
#
# Copyright (C) 2009-2010 Alvaro Lopez Ortega
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

import CTK

from Rule import RulePlugin
from util import *

URL_APPLY = '/plugin/header/apply'

NOTE_HEADER = N_("Header against which the regular expression will be evaluated.")
NOTE_MATCH  = N_("Regular expression.")
NOTE_TYPES  = N_("It defines how this match has to be evaluated.")

HEADERS = [
    ('Accept-Encoding', 'Accept-Encoding'),
    ('Accept-Charset',  'Accept-Charset'),
    ('Accept-Language', 'Accept-Language'),
    ('Referer',         'Referer'),
    ('User-Agent',      'User-Agent'),
    ('Cookie',          'Cookie'),
    ('Host',            'Host')
]

TYPES = [
    ('regex',    _('Matches a Regular Expression')),
    ('provided', _('Is Provided'))
]

def commit():
    # POST info
    key       = CTK.post.pop ('key', None)
    vsrv_num  = CTK.post.pop ('vsrv_num', None)
    new_hdr   = CTK.post.pop ('tmp!header', None)
    new_match = CTK.post.pop ('tmp!match', None)
    new_type  = CTK.post.pop ('tmp!type', None)

    # New entry
    if new_hdr:
        next_rule, next_pre = cfg_vsrv_rule_get_next ('vserver!%s'%(vsrv_num))

        CTK.cfg['%s!match'%(next_pre)]        = 'header'
        CTK.cfg['%s!match!header'%(next_pre)] = new_hdr
        CTK.cfg['%s!match!match'%(next_pre)]  = new_match
        CTK.cfg['%s!match!type'%(next_pre)]   = new_type

        return {'ret': 'ok', 'redirect': '/vserver/%s/rule/%s' %(vsrv_num, next_rule)}

    # Modifications
    return CTK.cfg_apply_post()


class Plugin_header (RulePlugin):
    def __init__ (self, key, **kwargs):
        RulePlugin.__init__ (self, key)
        is_new = key.startswith('tmp')
        props  = ({},{'class': 'noauto'})[is_new]

        type_widget = CTK.ComboCfg ('%s!type'%(key), TYPES, props)
        type_val    = CTK.cfg.get_val ('%s!type'%(key), 'regex')

        table = CTK.PropsTable()
        table.Add (_('Header'), CTK.ComboCfg('%s!header'%(key), HEADERS, props), _(NOTE_HEADER))
        table.Add (_('Type'),   type_widget, _(NOTE_TYPES))

        if is_new or type_val == 'regex':
            table.Add (_('Regular Expression'), CTK.TextCfg('%s!match'%(key), False, props), _(NOTE_MATCH))

        if is_new:
            type_widget.bind ('change',
                  """if ($('#%(type_widget)s').val() == 'regex') {
                           $('#%(regex)s').show();
                     } else {
                           $('#%(regex)s').hide();
                  }""" %({'type_widget': type_widget.id, 'regex': table[2].id}))

        submit = CTK.Submitter (URL_APPLY)
        submit += CTK.Hidden ('key', key)
        submit += CTK.Hidden ('vsrv_num', kwargs.pop('vsrv_num', ''))
        submit += table
        self += submit

        # Validation, and Public URLs
        CTK.publish (URL_APPLY, commit, method="POST")

    def GetName (self):
        header = CTK.cfg.get_val ('%s!header' %(self.key), '')
        match  = CTK.cfg.get_val ('%s!match' %(self.key), '')
        type_  = CTK.cfg.get_val ('%s!type' %(self.key), '')

        if type_ == 'provided':
            return _("Header %s is provided") %(header)
        else:
            return "%s %s ~ %s" % (_('Header'), header, match)
