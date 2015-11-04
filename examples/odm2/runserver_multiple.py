import logging
import os
import tempfile

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound

import wof
from measurement.odm2_measurement_dao import Odm2Dao as measurement
from timeseries.odm2_timeseries_dao import Odm2Dao as timeseries
from measurement.private_config import odm2_connection_string

logging.basicConfig(level=logging.DEBUG)

m_dao = measurement(odm2_connection_string)
t_dao = timeseries(odm2_connection_string)

m_app = wof.create_wof_flask_app(m_dao, './measurement/odm2_config_measurement.cfg')
m_app.config['DEBUG'] = True
m_site_map = wof.site_map(m_app)

t_app = wof.create_wof_flask_app(t_dao, './timeseries/odm2_config_timeseries.cfg')
t_app.config['DEBUG'] = True
t_site_map = wof.site_map(t_app)

combined_app = DispatcherMiddleware(NotFound, {
    '/measurement': m_app,
    '/timeseries': t_app,
})

if __name__ == '__main__':
    # This must be an available port on your computer.  
    # For example, if 8080 is already being used, try another port such as
    # 5000 or 8081.
    openPort = 8080 

    url = "http://127.0.0.1:" + str(openPort)

    print "----------------------------------------------------------------"
    print "Acess Service endpoints at "
    for path in m_site_map:
        print "%s%s%s" % (url,'/measurement',path)
    for path in t_site_map:
        print "%s%s%s" % (url,'/timeseries',path)
    print "----------------------------------------------------------------"

    run_simple('0.0.0.0', openPort, combined_app, use_reloader=True,
               use_debugger=True, threaded=True)
