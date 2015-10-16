import datetime

import soaplib.core
import soaplib.core.server.wsgi
import werkzeug

import wof.flask
import wof.soap
import wof.core_1_1 as wof_1_1
import wof.core_1_0 as wof_1_0

def create_wof_app(dao, config_file):
    """
    Returns a fully instantiated WOF wsgi app (flask + soap)
    """
    wof_obj_1_1 = wof_1_1.WOF_1_1(dao,config_file)
    app_1_1 = wof.flask.create_app_1_1(wof_obj_1_1)
    WOFService_1_1 = wof.soap.create_wof_service_class_1_1(wof_obj_1_1)
    soap_app_1_1 = soaplib.core.Application(
        services=[WOFService_1_1],
        tns='http://www.cuahsi.org/his/1.1/ws/',
        name='WaterOneFlow_1_1'
    )
    soap_wsgi_app_1_1 = soaplib.core.server.wsgi.Application(soap_app_1_1)

    wof_obj = wof_1_0.WOF(dao, config_file)
    app = wof.flask.create_app(wof_obj)
    WOFService = wof.soap.create_wof_service_class(wof_obj)
    soap_app = soaplib.core.Application(
        services=[WOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')
    soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)
    app.wsgi_app = werkzeug.wsgi.DispatcherMiddleware(app.wsgi_app, {
        '/rest_1_1' : app_1_1,
        '/soap/wateroneflow': soap_wsgi_app,
        '/soap/wateroneflow_1_1': soap_wsgi_app_1_1
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
