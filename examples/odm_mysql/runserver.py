import soaplib
import logging

import wof

from odm_dao import OdmDao
import private_config

import sys

""" Before running this script, create a private_config.py file with the 
    connection string to your ODM database in SQL Server.  For example:
    
    connection_string = \
    'mysql://username:password@(local)/databasename'
"""

logging.basicConfig(level=logging.DEBUG)

dao = OdmDao(private_config.connection_string)
app = wof.create_wof_app(dao, 'config.cfg')
app.config['DEBUG'] = True

if __name__ == '__main__':
    # This must be an available port on your computer.  
    # For example, if 8080 is already being used, try another port such as
    # 5000 or 8081.
    openPort = int(sys.argv[1])

    url = "http://rths.us:" + str(openPort) + "/"

    print "----------------------------------------------------------------"
    print "Access 'REST' endpoints at " + url
    print "Access SOAP WSDL at " + url + "soap/wateroneflow.wsdl"
    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)
