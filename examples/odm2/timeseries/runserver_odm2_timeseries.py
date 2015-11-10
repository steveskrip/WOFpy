import logging

import wof

from odm2_timeseries_dao import Odm2Dao
import private_config
ODM2_CONFIG_FILE = 'odm2_config_timeseries.cfg'

""" Before running this script, create a private_config.py file with the 
    connection string to your ODM database in SQL Server.  For example:
    
    odm2_connection_string = \
    'postgresql+psycopg2://username:password/db_name'
"""

logging.basicConfig(level=logging.DEBUG)

def startServer(config=ODM2_CONFIG_FILE):
    dao = Odm2Dao(private_config.odm2_connection_string)
    app = wof.create_wof_flask_app(dao, config)
    app.config['DEBUG'] = True

    openPort = 8080
    url = "http://127.0.0.1:" + str(openPort)
    print "----------------------------------------------------------------"
    print "Acess Service endpoints at "
    for path in wof.site_map(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

if __name__ == '__main__':
    startServer()
