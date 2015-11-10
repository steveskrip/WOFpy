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

M_CONFIG_FILE = './measurement/odm2_config_measurement.cfg'
T_CONFIG_FILE = './timeseries/odm2_config_timeseries.cfg'

def startServer(m_config=M_CONFIG_FILE,t_config=T_CONFIG_FILE):

    m_dao = measurement(odm2_connection_string)
    t_dao = timeseries(odm2_connection_string)

    m_conf = wof.core.wofConfig(m_dao, m_config)
    t_conf = wof.core.wofConfig(t_dao, t_config)

    app= wof.core.create_wof_flask_multiple({m_conf,t_conf},templates='../../wof/apps/templates')

    openPort = 8080
    url = "http://127.0.0.1:" + str(openPort)
    print "----------------------------------------------------------------"
    print "Service endpoints"
    for path in wof.core.site_map_flask_wsgi_mount(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"
    print "----------------------------------------------------------------"
    print "Acess HTML descriptions of endpoints at "
    for path in wof.site_map(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

if __name__ == '__main__':
    # This must be an available port on your computer.
    # For example, if 8080 is already being used, try another port such as
    # 5000 or 8081.

    startServer()
