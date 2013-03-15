import os
from pylons import config
from pylons.middleware import Response

class MinifyMiddleware(object):
    def __init__(self, app, minify=True):
        self.app = app
        
        self.static_files_path = os.path.abspath(config['pylons.paths']['static_files'])
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

    def __call__(self, environment, start_response):
        path = environment.get('PATH_INFO')

        if not path.endswith('.js'):
            return self.app(environment, start_response)
        elif path.endswith('.min.js'):
            return self.app(environment, start_response)

        # Check if the file exists, if it doesn't send 404 response
        # NOT WORKING
        full_path = os.path.join(self.static_files_path, path[1:])
        if not os.path.exists(full_path):
            return status_map[404]()(environment, start_response)

        f = open(full_path, 'rb')
        s = f.readlines()
        s = ''.join(s)
        f.close()
        print "Before %s: %d" % (path, len(s))
        if self.minify:
            content = self.minifier(s)
            
        print "After %s: %d" % (path, len(content))
        etag_key = '"%s"' % os.stat(full_path).st_mtime
        
        # Here we either need to register the response object with this thread,
        # or return something different
        response = Response()
        response.content_type = "text/javascript"
        response.headers['ETag'] = etag_key
        response.body = content

        return response(environment, start_response)