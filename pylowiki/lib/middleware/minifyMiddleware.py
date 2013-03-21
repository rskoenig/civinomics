import os
from pylons import config
from pylons.middleware import Response

class MinifyMiddleware(object):
    def __init__(self, app, minify=True, cache = None):
        self.app = app
        if cache is None:
            self.cache = {}
        else:
            self.cache = cache
        self.static_files_path = os.path.abspath(config['pylons.paths']['static_files'])
        self.minify = minify

        if self.minify:
            try:
                # Try to import slimit for javascript minifying
                from slimit import minify as slimit_minify
                self.minifier = lambda x: slimit_minify(x, mangle=True)
                self.minifier_noMangle = lambda x: slimit_minify(x, mangle=False)
            except:
                try:
                    # Try jsmin as a fallback
                    from jsmin import jsmin
                    self.minifier = jsmin
                except:
                    # If no lib available cancel compression
                    self.minify = False

    def __call__(self, environment, start_response):
        path = environment.get('PATH_INFO')
        if not path.endswith('.js'):
            return self.app(environment, start_response)
        elif path.endswith('.min.js'):
            return self.app(environment, start_response)

        # Check if the file exists, if it doesn't send 404 response
        full_path = os.path.join(self.static_files_path, path[1:])
        if not os.path.exists(full_path):
            response = Response()
            response.status_int = 404
            return response(environment, start_response)
        
        etag_key = '"%s"' % os.stat(full_path).st_mtime
        cached = self.cache.get(path)
        if not cached or cached['etag_key'] != etag_key:
            f = open(full_path, 'rb')
            s = f.readlines()
            s = ''.join(s)
            f.close()
            if self.minify:
                if path.startswith('/js/ng/'):
                    content = self.minifier_noMangle(s)
                else:
                    content = self.minifier(s)
            else:
                content = s
            cached = {'content':content, 'etag_key':etag_key}
            self.cache[path] = cached
        
        # Here we either need to register the response object with this thread,
        # or return something different
        response = Response()
        response.content_type = "text/javascript"
        response.headers['ETag'] = etag_key
        response.body = content

        return response(environment, start_response)