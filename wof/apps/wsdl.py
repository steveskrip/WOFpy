import StringIO
import logging

from spyne.decorator import rpc
from spyne.model.complex import Array
from spyne.model.primitive import Unicode, AnyXml, Float, Boolean
from spyne.service import ServiceBase
from spyne.model.fault import Fault
from spyne.util import memoize
import wof
from jinja2 import Environment, Template, PackageLoader, FileSystemLoader
env = Environment(loader=PackageLoader('apps', 'templates'))

@memoize
def TWSDLService(wof_inst,T, T_name):
    class WSDLService(ServiceBase):
        @rpc( _returns=T)
       #@wsdl.route('/soap/wateroneflow.wsdl')
        def get_wsdl_1_0(ctx ):

        #TODO: The WSDL should be served separately from the Flask application.
        # Come up with a better way to do this.
            network = wof_inst.network.lower()
            ports = ctx.get_port_types()
            try:
               serv_loc = wof_inst.config['SOAP_SERVICE_URL']
            except KeyError:
                serv_loc = wof_inst.config.get(
                    'SOAP_SERVICE_URL',
            #        '%s/wateroneflow/' % request.url.rsplit('/', 1)[0])
                '/wateroneflow/')
            template = env.get_template('wsdl_temp.wsdl')
            response = template.render(
                                                     serv_loc=serv_loc,
                                                     network=network)

            response.headers['Content-Type'] = 'text/xml'

            return response