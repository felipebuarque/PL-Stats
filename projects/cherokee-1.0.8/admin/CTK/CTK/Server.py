# -*- coding: utf-8 -*-

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

import re
import sys
import types
import errno
import threading
import traceback

import pyscgi
import Cookie
import Config

from util import json_dump
from Post import Post
from HTTP import HTTP_Response, HTTP_Error

from cgi import escape as escape_html


class PostValidator:
    def __init__ (self, post, validation_list):
        self.post            = post
        self.validation_list = validation_list

    def Validate (self):
        errors  = {}
        updates = {}

        for key in self.post:
            for regex, func in self.validation_list:
                if re.match(regex, key):
                    for n in range(len(self.post[key])):
                        val = self.post[key][n]
                        if not val and 'CHECK_ON_NO_VALUE' not in dir(func):
                            continue

                        try:
                            tmp = func (val)
                        except Exception, e:
                            errors[key] = str(e)
                            break

                        if tmp and tmp != val:
                            self.post[key][n] = tmp
                            updates[key] = tmp

        if errors or updates:
            return {'ret': "unsatisfactory",
                    'errors':  errors,
                    'updates': updates}


class ServerHandler (pyscgi.SCGIHandler):
    def __init__ (self, *args):
        self.response = HTTP_Response()

        # SCGIHandler.__init__ invokes ::handle()
        pyscgi.SCGIHandler.__init__ (self, *args)

    def _process_post (self):
        pyscgi.SCGIHandler.handle_post(self)
        post = Post (self.post)
        return post

    def _do_handle (self):
        # Read the URL
        url = self.env['REQUEST_URI']

        # Get a copy of the server (it did fork!)
        server = get_server()

        # Refer SCGI object by thread
        my_thread = threading.currentThread()
        my_thread.scgi_conn   = self
        my_thread.request_url = url

        for published in server._web_paths:
            if re.match (published._regex, url):
                # POST
                if published._method == 'POST':
                    post = self._process_post()
                    my_thread.post = post

                    # Validate
                    validator = PostValidator (post, published._validation)
                    errors = validator.Validate()
                    if errors:
                        resp = HTTP_Response(200, body=json_dump(errors))
                        resp['Content-Type'] = "application/json"
                        return resp

                # Execute handler
                ret = published (**published._kwargs)

                # Deal with the returned info
                if type(ret) == str:
                    self.response += ret
                    return self.response

                elif type(ret) == dict:
                    info = json_dump(ret)
                    self.response += info
                    self.response['Content-Type'] = "application/json"
                    return self.response

                elif isinstance(ret, HTTP_Response):
                    return ret

                else:
                    self.response += ret
                    return self.response

        # Not found
        return HTTP_Error (404)

    def handle_request (self):
        def manage_exception():
            # Print the backtrace
            info = traceback.format_exc()
            print >> sys.stderr, info

            # Custom error management
            if error.page:
                try:
                    page = error.page (info, desc)
                    response = HTTP_Response (error=500, body=page.Render())
                    self.send (str(response))
                    return
                except Exception, e:
                    print "!!!!!!", e
                    pass

            # No error handling page
            html = '<pre>%s</pre>' %(escape_html(info))
            self.send (str(HTTP_Error(desc=html)))

        try:
            content = self._do_handle()
            self.send (str(content))

        except OSError, e:
            if e.errno == errno.EPIPE:
                # The web server closed the SCGI socket
                return
            manage_exception()

        except Exception, desc:
            manage_exception()



class Server:
    def __init__ (self):
        self._web_paths = []
        self._scgi        = None
        self._is_init     = False
        self.lock         = threading.RLock()
        self.plugin_paths = []

    def init_server (self, *args, **kwargs):
        # Is it already init?
        if self._is_init:
            return
        self._is_init = True

        # Instance SCGI server
        self._scgi = pyscgi.ServerFactory (*args, **kwargs)

        # Figure plug-in paths
        from Plugin import figure_plugin_paths
        self.plugin_paths = figure_plugin_paths()

    def sort_routes (self):
        def __cmp(x,y):
            lx = len(x._regex)
            ly = len(y._regex)
            return cmp(ly,lx)

        self.lock.acquire()
        try:
            self._web_paths.sort(__cmp)
        finally:
            self.lock.release()

    def add_route (self, route_obj):
        self.lock.acquire()
        try:
            # Look for a duplicate
            to_remove = []
            for r in self._web_paths:
                if r._regex == route_obj._regex:
                    to_remove.append (r)

            self._web_paths = filter (lambda x: x not in to_remove, self._web_paths)

            # Insert
            self._web_paths.append (route_obj)
            self.sort_routes()
        finally:
            self.lock.release()

    def remove_route (self, path):
        self.lock.acquire()
        try:
            to_remove = []
            for r in self._web_paths:
                if r._regex == path:
                    to_remove.append (r)

            self._web_paths = filter (lambda x: x not in to_remove, self._web_paths)
        finally:
            self.lock.release()

    def serve_forever (self):
        try:
            while True:
                # Handle request
                self._scgi.handle_request()
        except KeyboardInterrupt:
            print "\r", "Server exiting.."
            self._scgi.server_close()


#
# Helpers
#
def cfg_reply_ajax_ok():
    if cfg.has_changed():
        return {'ret':'ok', 'modified': '#save-button'}

    return {'ret':'ok', 'not-modified': '#save-button'}

def cfg_apply_post():
    for k in post:
        cfg[k] = post[k]

    return cfg_reply_ajax_ok()


__global_server = None
def get_server():
    global __global_server
    if not __global_server:
        __global_server = Server ()

    return __global_server

def get_scgi():
    my_thread = threading.currentThread()
    return my_thread.scgi_conn

def init (*args, **kwargs):
    # Deals with UTF-8
    if sys.getdefaultencoding() != 'utf-8':
        reload (sys)
        sys.setdefaultencoding('utf-8')

    # Server
    srv = get_server()

    if not 'threading' in kwargs:
        kwargs['threading'] = True

    kwargs['handler_class'] = ServerHandler
    srv.init_server (*args, **kwargs)

def set_synchronous (sync):
    srv = get_server()
    srv._scgi.set_synchronous (sync)

def add_plugin_dir (path):
    srv = get_server()
    srv.plugin_paths.insert (0, path)

def run (*args, **kwargs):
    init (*args, **kwargs)

    srv = get_server()
    srv.serve_forever()

def step ():
    srv = get_server()
    srv._scgi.handle_request()


class Publish_FakeClass:
    def __init__ (self, func):
        self.__func = func

    def __call__ (self, *args, **kwargs):
        return self.__func (*args, **kwargs)


def publish (regex_url, klass, **kwargs):
    # Instance object
    if type(klass) == types.ClassType:
        obj = klass()
    else:
        obj = Publish_FakeClass (klass)

    # Set internal properties
    obj._kwargs     = kwargs
    obj._regex      = regex_url
    obj._validation = kwargs.pop('validation', [])
    obj._method     = kwargs.pop('method', None)

    # Register
    server = get_server()
    server.add_route (obj)

def unpublish (regex_url):
    # Unregister
    server = get_server()
    server.remove_route (regex_url)


class _Cookie:
    def __setitem__ (self, name, value):
        my_thread = threading.currentThread()
        response = my_thread.scgi_conn.response
        response['Set-Cookie'] = "%s=%s" %(name, value)

    def get_val (self, name, default=None):
        my_thread = threading.currentThread()
        scgi = my_thread.scgi_conn
        cookie = Cookie.SimpleCookie(scgi.env.get('HTTP_COOKIE', ''))
        if name in cookie:
            return cookie[name].value
        else:
            return default

    def __getitem__ (self, name):
        return self.get_val (name, None)


class _Post:
    def get_val (self, name, default=None):
        my_thread = threading.currentThread()
        post = my_thread.post
        return post.get_val(name, default)

    def __getitem__ (self, name):
        return self.get_val (name, None)

    def __iter__ (self):
        my_thread = threading.currentThread()
        post = my_thread.post
        return post.__iter__()

    def __str__ (self):
        my_thread = threading.currentThread()
        post = my_thread.post
        return str(post)

    def pop (self, *args):
        my_thread = threading.currentThread()
        post = my_thread.post
        return post.pop(*args)

    def keys (self, *args):
        my_thread = threading.currentThread()
        post = my_thread.post
        return post.keys(*args)

    def get_all (self, *args):
        my_thread = threading.currentThread()
        post = my_thread.post
        return post.get_all(*args)


class _Request:
    def _get_request_url (self):
        my_thread = threading.currentThread()
        return my_thread.request_url

    def _get_scgi_conn (self):
        return get_scgi()

    url  = property (_get_request_url)
    scgi = property (_get_scgi_conn)


class _Error:
    def __init__ (self):
        self.page = None


cookie  = _Cookie()
post    = _Post()
request = _Request()
error   = _Error()
cfg     = Config.Config()
