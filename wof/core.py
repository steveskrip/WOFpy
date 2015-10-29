import datetime

import werkzeug
import wof.flask
import wof.core_1_1 as wof_1_1
import wof.core_1_0 as wof_1_0

from spyne.server.wsgi import WsgiApplication
from spyne.application import Application
from spyne.model.primitive import Unicode, AnyXml
from spyne.protocol.soap import Soap11
from spyne.protocol.http import HttpRpc
from spyne.protocol.xml import XmlDocument

from wof.apps.spyned_1_0 import TWOFService as wml10
from wof.apps.spyned_1_1 import TWOFService as wml11

import logging
#logging.basicConfig(level=logging.INFO)
logging.getLogger('spyne.model.complex').setLevel(logging.ERROR)
logging.getLogger('spyne.interface._base').setLevel(logging.ERROR)
logging.getLogger('spyne.util.appreg').setLevel(logging.ERROR)
logging.getLogger('spyne.interface.xml_schema').setLevel(logging.ERROR)

_SERVICE_PARAMS = {
    "r_type" : "rest",
    "s_type" : "soap",
    "wml10_tns" : "http://www.cuahsi.org/his/1.0/ws/",
    "wml11_tns" : "http://www.cuahsi.org/his/1.1/ws/",
    "wml10_rest_name" : "WaterOneFlow_rest_1_0",
    "wml10_soap_name" : "WaterOneFlow_soap_1_0",
    "wml11_rest_name" : "WaterOneFlow_rest_1_1",
    "wml11_soap_name" : "WaterOneFlow_soap_1_1",
}

def create_wof_app(dao, config_file):
    """
    Returns a fully instantiated WOF wsgi app (flask + apps)
    """

    wof_obj_1_0 = wof_1_0.WOF(dao, config_file)
    wof_obj_1_1 = wof_1_1.WOF_1_1(dao,config_file)
    app = wof.flask.create_app(wof_obj_1_0,wof_obj_1_1)

    soap_app_1_0 = Application(
        [wml10(wof_obj_1_0,Unicode,_SERVICE_PARAMS["s_type"])],
        tns=_SERVICE_PARAMS["wml10_tns"],
        name=_SERVICE_PARAMS["wml10_soap_name"],
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )

    rest_app_1_0 = Application(
        [wml10(wof_obj_1_0,AnyXml,_SERVICE_PARAMS["r_type"])],
        tns=_SERVICE_PARAMS["wml10_tns"],
        name=_SERVICE_PARAMS["wml10_rest_name"],
        in_protocol=HttpRpc(validator='soft'),
        out_protocol=XmlDocument(),
    )

    soap_app_1_1 = Application(
        [wml11(wof_obj_1_1,Unicode,_SERVICE_PARAMS["s_type"])],
        tns=_SERVICE_PARAMS["wml11_tns"],
        name=_SERVICE_PARAMS["wml11_soap_name"],
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )

    rest_app_1_1 = Application(
        [wml11(wof_obj_1_1,AnyXml,_SERVICE_PARAMS["r_type"])],
        tns=_SERVICE_PARAMS["wml11_tns"],
        name=_SERVICE_PARAMS["wml11_rest_name"],
        in_protocol=HttpRpc(validator='soft'),
        out_protocol=XmlDocument(),
    )

    rest_wsgi_wrapper_1_0 = WsgiApplication(rest_app_1_0)
    soap_wsgi_wrapper_1_0 = WsgiApplication(soap_app_1_0)
    rest_wsgi_wrapper_1_1 = WsgiApplication(rest_app_1_1)
    soap_wsgi_wrapper_1_1 = WsgiApplication(soap_app_1_1)

    app.wsgi_app = werkzeug.wsgi.DispatcherMiddleware(app.wsgi_app, {
        '/rest/1_0': rest_wsgi_wrapper_1_0,
        '/rest/1_1' : rest_wsgi_wrapper_1_1,
        '/soap/wateroneflow': soap_wsgi_wrapper_1_0,
        '/soap/wateroneflow_1_1': soap_wsgi_wrapper_1_1,
        })

    return app

def _get_iso8061_datetime_string(object, local_datetime_attr,
                                 utc_datetime_attr):
    """
    Returns a datetime string given an object and the names of the
    attributes for local time and utc date time
    """
    local_datetime = getattr(object, local_datetime_attr, None)
    if local_datetime:
        if type(local_datetime) == datetime.datetime:
            if not local_datetime.tzinfo:
                raise ValueError("local times must be timezone-aware")
            return local_datetime.isoformat()
        else:
            return local_datetime
    else:
        utc_datetime = getattr(object, utc_datetime_attr)
        if type(utc_datetime) == datetime.datetime:
            return utc_datetime.replace(tzinfo=None).isoformat() + 'Z'
        else:
            return utc_datetime
