# Taken from https://bitbucket.org/clsdaniel/tgext.coffeescript

import subprocess
import os
from pylons import config
from pylons.middleware import Response

class CoffeeScriptMiddleware(object):
    def __init__(self, app, cache=None, bare=True, minify=False):
        self.app = app
        if cache:
            self.cache = cache
        else:
            self.cache = {}
        
        self.static_files_path = os.path.abspath(config['pylons.paths']['static_files'])
        self.bare = True
        self.minify = minify

        if self.minify:
            try:
                # Try to import slimit for javascript minifying
                from slimit import minify as slimit_minify
                self.minifier = lambda x: slimit_minify(x, mangle=True)
            except:
                try:
                    # Try jsmin as a fallback
                    from jsmin import jsmin
                    self.minifier = jsmin
                except:
                    # If no lib available cancel compression
                    self.minify = False
        
        try:
            coffee = subprocess.Popen(['coffee', '--version'], stdout=subprocess.PIPE)
        except OSError:
            pass
            #return

        out, err = coffee.communicate()

        if "CoffeeScript" in out:
            self.method = "subprocess"

    def compile_coffee(self, fullpath):
        if self.bare:
            args = ['coffee', '-bp', fullpath]
        else:
            ['coffee', '-p', fullpath]

        coffee = subprocess.Popen(args, stdout=subprocess.PIPE)
        out, err = coffee.communicate()

        # TODO: Handle returned error code from compiler
        if err:
            return ""

        return out

    def compile(self, fullpath):
        if self.method == "subprocess":
            return self.compile_coffee(fullpath)
        return ""

    def __call__(self, environment, start_response):
        path = environment.get('PATH_INFO')

        if not path.endswith('.coffee'):
            return self.app(environment, start_response)

        # Check if the file exists, if it doesn't send 404 response
        # NOT WORKING
        full_path = os.path.join(self.static_files_path, path[1:])
        if not os.path.exists(full_path):
            return status_map[404]()(environment, start_response)

        # Generate etag key (file modified time)
        etag_key = '"%s"' % os.stat(full_path).st_mtime
        none_match = environment.get('HTTP_IF_NONE_MATCH')

        if none_match and etag_key == none_match:
            start_response('304 Not Modified', (('ETag', etag_key),))
            return ['']

        cached = self.cache.get(path)
        if not cached or cached['etag_key'] != etag_key:
            content = self.compile(full_path)
            if self.minify:
                content = self.minifier(content)
            cached = dict(content=content, etag_key=etag_key)
            self.cache[path] = cached
        
        # Here we either need to register the response object with this thread,
        # or return something different
        response = Response()
        response.content_type = "text/javascript"
        response.headers['ETag'] = etag_key
        response.body = cached['content']

        return response(environment, start_response)