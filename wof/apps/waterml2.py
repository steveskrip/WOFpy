import StringIO
import logging
import datetime

from spyne.decorator import rpc
from spyne.model.complex import Array
from spyne.model.primitive import Unicode, AnyXml, Float, Boolean
from spyne.service import ServiceBase
from spyne.model.fault import Fault
from spyne.util import memoize
import wof

from jinja2 import Environment, Template, PackageLoader, FileSystemLoader

logger = logging.getLogger(__name__)

NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xmlns:wtr="http://www.cuahsi.org/waterML/" \
    xmlns="http://www.cuahsi.org/waterML/1.0/"'

@memoize
def TWOFService(wof_inst,T, T_name):
    class WOFService(ServiceBase):

        @rpc(Unicode, Unicode, Unicode, Unicode, _returns=T)
        def GetValues(self, location, variable, startDate=None,
                                      endDatee=None):
                # location = request.args.get('location', None)
                # variable = request.args.get('variable', None)
                # startDate = request.args.get('startDate', None)
                # endDatee = request.args.get('endDate', None)

                if (location == None or variable == None):
                    return "Must enter a site code (location) and a variable code \
                        (variable)"

                siteCode = location.replace(wof_inst.network + ':', '')
                varCode = variable.replace(wof_inst.network + ':', '')

                data_values = wof_inst.dao.get_datavalues(siteCode, varCode,
                                                                      startDate,
                                                                      endDatee)

                site_result = wof_inst.dao.get_site_by_code(siteCode)
                variable_result = wof_inst.dao.get_variable_by_code(varCode)

                current_date = str(datetime.datetime.now())

                # response = make_response(render_template('wml2_values_template.xml',
                #                                         current_date=current_date,
                #                                         data_values=data_values,
                #                                         site_result=site_result,
                #                                         variable_result=variable_result))
                env = Environment(loader=FileSystemLoader('D:/dev_odm/WOFpy/wof/apps/templates'))
                template = env.get_template('wml2_values_template.xml')
                response = template.render(current_date=current_date,
                                                        data_values=data_values,
                                                        site_result=site_result,
                                                        variable_result=variable_result)
                response = response.encode('utf-8')
                #response.headers['Content-Type'] = 'text/xml'

                return response


    return WOFService