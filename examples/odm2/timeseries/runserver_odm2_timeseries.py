import soaplib
import logging

import wof

from odm2_timeseries_dao import Odm2Dao
import private_config

""" Before running this script, create a private_config.py file with the 
    connection string to your ODM database in SQL Server.  For example:
    
    odm2_connection_string = \
    'postgresql+psycopg2://username:password/db_name'
"""

logging.basicConfig(level=logging.DEBUG)

dao = Odm2Dao(private_config.odm2_connection_string)
app = wof.create_wof_app(dao, 'odm2_config_timeseries.cfg')
app.config['DEBUG'] = True

if __name__ == '__main__':
    # This must be an available port on your computer.  
    # For example, if 8080 is already being used, try another port such as
    # 5000 or 8081.
    openPort = 8080 

    url = "http://127.0.0.1:" + str(openPort) + "/"

    print "----------------------------------------------------------------"
    print "Access WaterML 1.0 'REST' endpoints at " + url
    print "Access WaterML 1.1 'REST' endpoints at " + url +"rest_1_1"
    print "Access WaterML 1.0 SOAP WSDL at " + url + "soap/wateroneflow.wsdl"
    print "Access WaterML 1.1 SOAP WSDL at " + url + "soap/wateroneflow_1_1.wsdl"
    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)
