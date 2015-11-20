
import logging

import wof
from wof.core import WOFConfig

from odm_dao import OdmDao


import sys

"""
    python runserver_odm_mysql.py
    --config=config.cfg
    --connection=mysql://username:password@(local)/databasename

    Also:
    python runserver_odm_mysql.py
    --config=../odm_sqlserver/lbr_config.cfg
    --connection=mssql+pyodbc://username:password@localhost/databasename?driver=SQL+Server+Native+Client+10.0

"""

logging.basicConfig(level=logging.DEBUG)


def startServer(config='config.cfg',connection=None,openPort=8080):

    dao = OdmDao(connection)
    app = wof.create_wof_flask_app(dao, config)
    app.config['DEBUG'] = True

    configFile = WOFConfig(config)

    url = "http://127.0.0.1:" + str(openPort)
    print "----------------------------------------------------------------"
    print "Service endpoints"
    for path in wof.core.site_map_flask_wsgi_mount(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"
    print "----------------------------------------------------------------"
    print "HTML Acess Service endpoints at "
    for path in wof.site_map(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='start WOF for an ODM1 database.')
    parser.add_argument('--config',
                       help='Configuration file')
    parser.add_argument('--connection',
                       help='Connection String eg: "mssql+pyodbc://username:password@localhost/LittleBear11?driver=SQL+Server+Native+Client+10.0"')

    parser.add_argument('--port',
                       help='Open port for server."', default=8080, type=int)
    args = parser.parse_args()
    print(args)

    startServer(config=args.config,connection=args.connection,openPort=args.port)
