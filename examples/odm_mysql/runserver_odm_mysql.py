#!/usr/bin/python

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


def startServer(connection, config='config.cfg',openPort=8080):
"""given an open file on connection, read it to get a connection string to open the database and start up flask running WOF."""

    dao = OdmDao(connection.read())
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
    print "HTML Access Service endpoints at "
    for path in wof.site_map(app):
        print "%s%s" % (url,path)

    print "----------------------------------------------------------------"

    app.run(host='0.0.0.0', port=openPort, threaded=True)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='start WOF for an ODM1 database.')
    parser.add_argument('connection', type=argparse.FileType('r'), 
                       help='The name of a file containing the Connection String eg: mysql://username:password@localhost/database')
    parser.add_argument('--config', default="config.cfg",
                       help='Configuration file')
    parser.add_argument('--port',
                       help='Open port for server."', default=8080, type=int)
    args = parser.parse_args()
    print(args)

    startServer(connection=args.connection,config=args.config,openPort=args.port)

