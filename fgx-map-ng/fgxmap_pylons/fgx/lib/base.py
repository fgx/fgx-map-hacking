## @package fgx.lib.base
# @brief The base Controller API



from pylons.controllers import WSGIController
from pylons.templating import render_jinja2 as render

from fgx.model.meta import Sess

## Provides the BaseController wsgi class for subclassing.
class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        # Invoke the Controller
        # 
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Sess.navdata.remove()
            Sess.users.remove()
            Sess.mpnet.remove()
