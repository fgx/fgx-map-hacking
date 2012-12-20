##@package fgx.controllers.error
# @brief error handlers, 404 etc
#
import cgi

from paste.urlparser import PkgResourcesParser
from pylons.middleware import error_document_template
from webhelpers.html.builder import literal

from fgx.lib.base import BaseController

## Generates error documents as and when they are required.
#
#   The ErrorDocuments middleware forwards to ErrorController when error
#    related status codes are returned from the application.
#
#    This behaviour can be altered by changing the parameters to the
#    ErrorDocuments middleware in your config/middleware.py file.
#    
# @todo Pete to customize the error handler for ajax, production vs dev etc
#
class ErrorController(BaseController):
   
	## Render the error document
    def document(self):
        request = self._py_object.request
        resp = request.environ.get('pylons.original_response')
        content = literal(resp.body) or cgi.escape(request.GET.get('message', ''))
        page = error_document_template % \
            dict(prefix=request.environ.get('SCRIPT_NAME', ''),
                 code=cgi.escape(request.GET.get('code', str(resp.status_int))),
                 message=content)
        return page

    ## Serve Pylons' stock images
    def img(self, id):
        return self._serve_file('/'.join(['media/img', id]))

    ## Serve Pylons' stock stylesheets
    def style(self, id):
        return self._serve_file('/'.join(['media/style', id]))

    ## Call Paste's FileApp (a WSGI application) to serve the file at the specified path
    def _serve_file(self, path):
        request = self._py_object.request
        request.environ['PATH_INFO'] = '/%s' % path
        return PkgResourcesParser('pylons', 'pylons')(request.environ, self.start_response)
