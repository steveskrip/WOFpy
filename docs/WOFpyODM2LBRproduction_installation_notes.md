# Installing WOFpy with Little Bear River MySQL ODM2 test database

These notes cover installation of `WOFpy` from its `conda` package; downloading and installing the Little Bear River (LBR) ODM2 MySQL test database; configuring WOFpy for the LBR database; and running WOFpy. *The instructions enable the creation of "live" web services exposed to external use.*

Most of the steps were originally copied from [WOFpyODM2LBRtest_installation_notes.md](https://github.com/ODM2/WOFpy/blob/master/docs/WOFpyODM2LBRtest_installation_notes.md) with some modifications; we're no longer actively maintaining that page, but it still has useful content, including references to relevant discussions.

## Table of Contents

- [Testing Environments](#testing-environments)
	+ [Amazon Web Services (AWS)](#amazon-web-services-aws)
	+ [Local Ubuntu Machine](#local-ubuntu-machine)
- [Installing WOFpy](#installing-wofpy)
- [Installing NGINX](#installing-nginx)
- [Setting up runserver script and wsgi.py](#setting-up-runserver-script-and-wsgipy)
- [Configuring WSGI](#configuring-wsgi)
	+ [AWS SysV init system](#aws-sysv-init-system)
	+ [Local Server Systemd init system](#local-server-systemd-init-system)
- [Configuring NGINX](#configuring-nginx)
	+ [AWS SysV init system](#aws-sysv-init-system_1)
	+ [Local Server Systemd init system](#local-server-systemd-init-system_1)
- [Checking Live instance of WOFpy](#checking-live-instance-of-wofpy)

## Testing Environments

We tested WOFpy installations on Amazon Web Services and a local Ubuntu Server.
Deployment of WOFpy was done in an Ubuntu Server. WOFpy is served by using [NGINX](https://www.nginx.com/) and [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/). **These instructions assume that Amazon AWS EC2 Instance or a local Linux Ubuntu Server is already set up.**

### [Amazon Web Services (AWS)](https://aws.amazon.com/) 

Note that this installation is currently (2017-3-1) [live on the cloud](http://52.40.105.124:8080/odm2timeseries/). It will be kept live only during active testing, and will be taken down without prior notice when active testing is over. It will be reactivated in the future as needed.

Specifications:
- Ubuntu 14.04
- MySQL 5.6
- NGINX 1.10.2

The AWS Ubuntu Server is running [SysV init](http://en.wikipedia.org/wiki/Init#SysV-style) system.

### Local Ubuntu Machine

Tested on:
- Ubuntu 16.04
- MySQL 5.5.28
- NGINX 1.10.2 (*assumed but not confirmed*)

The Local Ubuntu Server is running [Systemd init](http://www.freedesktop.org/wiki/Software/systemd/) system.


## Installing WOFpy

**Note: The installation step for WOFpy should be the same for both server on AWS and local**

1. Install miniconda into the user home directory. `/home/ubuntu/miniconda`
	```bash
	$ url=https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
	$ curl $url -o miniconda.sh
	$ bash miniconda.sh -b
	$ export PATH=$HOME/miniconda2/bin:$PATH
	```

2. Create the "wofpy" conda environment: `conda create -n wofpy -c ODM2 -c conda-forge python=2.7 wofpy odm2api mysql-python uwsgi`. *Note: `mysql-python` is not installed by the wofpy package and we'll need `uwsgi` for the application*
3. Download the Little Bear River (LBR) test MySQL database

	```bash
	$ wget https://raw.githubusercontent.com/ODM2/ODM2/master/usecases/littlebearriver/sampledatabases/odm2_mysql/LBR_MySQL_SmallExample.sql
	```
4.  If MySQL database was a stand alone in Unix, add to /etc/mysql/my.cnf : `lower_case_table_names = 1` under [mysqld]
5. Create ODM2 database in MySQL. At the bash shell where the LBR SQL file was downloaded: `mysql -u root -p odm2 < LBR_MySQL_SmallExample.sql`
6. **NOTE: Sample database is missing featuregeometrywkt in samplingfeatures** In order to make WOFpy work, alter the table by adding featuregeometrywkt column, at the mysql client:

	```sql
	ALTER TABLE samplingfeatures ADD featuregeometrywkt VARCHAR (8000) NULL;
	```
7. Clone the WOFpy repository `$ git clone https://github.com/ODM2/WOFpy.git`

## Installing NGINX

**Note: The installation step for NGINX should be the same for both server on AWS and local**

1. Install nginx into the system

	``` bash
	$ sudo add-apt-repository ppa:nginx/stable
	$ sudo apt-get update && sudo apt-get upgrade
	$ sudo apt-get install nginx
	```
2. Start nginx webserver and then go to your server ip address

	``` bash
	$ sudo service nginx start
	```

	You should get a welcome page:
	![nginxhome](./img/nginxhome.png)

	**This welcome page is located in `/var/www/html/`**

3. Copy the example `odm2/timeseries` folder from WOFpy repository to `/var/www/`

	```bash
	$ sudo cp -r /home/ubuntu/WOFpy/examples/flask/odm2/timeseries /var/www/
	```

4. Currently the folder timeseries is owned by user `root` and group `root`, in order for nginx to be able to access and use this folder, change the owner and group to www-data.

	```bash
	$ sudo chown -R www-data:www-data /var/www/timeseries
	```

## Setting up runserver script and wsgi.py

**Note: This step for setting up runserver script and wsgi.py should be the same for both server on AWS and local**

1. Using `runserver_odm2_timeseries.py` as an example, create a `runserver.py` script.

	```python
	import os, sys

	import wof.flask

	import logging
	import wof

	from odm2_timeseries_dao import Odm2Dao
	#import private_config

	"""
	    python runserver_odm2_timeseries.py
	    --config=odm2_config_timeseries.cfg
	    --connection=example.connection
	"""
	#logging.basicConfig(level=logging.DEBUG)
	#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

	connection = 'mysql+mysqldb://root:password@127.0.0.1:3306/ODM2'

	dao = Odm2Dao(connection)
	config_file = 'odm2_config_timeseries.cfg'
	timeseries_conf = wof.core.wofConfig(dao, config_file)
	app = wof.flask.create_wof_flask_multiple({timeseries_conf}, templates=os.path.join(wof.__path__[0],'flask/templates'))

	def startServer(openPort = 8080):

	    app.config['DEBUG'] = True


	    url = "http://127.0.0.1:" + str(openPort)
	    print "----------------------------------------------------------------"
	    print "Acess Service endpoints at "
	    for path in wof.site_map(app):
		print "%s%s" % (url,path)

	    print "----------------------------------------------------------------"

	    app.run(host='0.0.0.0', port=openPort, threaded=True)

	if __name__ == '__main__':
	    startServer()
	```

2. Test that `runserver.py` will deploy WOFpy. Go to `ip:8080/odm2timeseries/` on your browser once it is deployed.

	```bash
	$ source activate wofpy # first activate the correct conda environment
	$ python runserver.py
	```

	![wofpy home](./img/wofpyhome.png)

3. Exit from the `runserver.py` and now we will create `wsgi.py`, a file that serves as the entry point for WOFpy.

	``` python
	#! /home/ubuntu/miniconda/envs/wofpy/bin/python
	import sys
	sys.path.insert(0,"/var/www/timeseries")

	from runserver import app as application
	application.secret_key = 'Thisismysecretkey'
	```

## Configuring WSGI

1. Testing uWSGI with WSGI. Do this by passing name of entry point, specify socket, and protocol (make sure that wofpy conda environment is still active). Go to `ip:8080/odm2timeseries/` on your browser once it is deployed.

	``` bash
	$ uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi
	```

2. If everything works, now deactivate the conda environment. `$ source deactivate`

3. Create uWSGI configuration file `timeseries.ini` in `/var/www/timeseries/`

	``` bash
	# Allows uWSGI to know to apply the settings
	[uwsgi]
	module = wsgi
	# Tells uWSGI to start up in master mode and spawn five worker processes to serve actual request
	master = true
	processes = 5
	# When we were testing, we exposed uWSGI on a network port. 
	# However, we're going to be using Nginx to handle actual client connections, which will then pass requests to uWSGI. 
	# Since these components are operating on the same computer, a Unix socket is preferred because it is more secure and faster. 
	# We'll call the socket myproject.sock and place it in this directory.
	# We'll also have to change the permissions on the socket. 
	# We'll be giving the Nginx group ownership of the uWSGI process later on, so we need to make sure the group owner of the socket can read information from it and write to it. 
	# We will also clean up the socket when the process stops by adding the "vacuum" option.
	socket = timeseries.sock
	chmod-socket = 660
	vacuum = true
	# The last thing we need to do is set the die-on-term option. 
	# This is needed because the Upstart init system and uWSGI have different ideas on what different process signals should mean.
	die-on-term = true
	```

### AWS SysV init system

1. Create an upstart script `timeseries.conf` in `/etc/init/. This will allow the init system to automatically start uwsgi and serve out WOFpy when the server boots. 

	``` bash
	# description of the script purpose
	description "uWSGI server instance configured to serve timeseries"

	# The normal system runtime numbers are 2, 3, 4, and 5, so we'll tell it to start our script when the system reaches one of those runlevels. 
	# We'll tell it to stop on any other runlevel (such as when the server is rebooting, shutting down, or in single-user mode)
	start on runlevel [2345]
	stop on runlevel [!2345]

	# The Nginx server runs under the www-data group. 
	# We need Nginx to be able to read from and write to the socket file, so we'll give this group ownership over the process
	setuid www-data
	setgid www-data

	# Set the conda environment path
	env PATH=/home/ubuntu/miniconda/envs/wofpy/bin

	# change directory to where the uWSGI configuration file is located then execute uwsgi with the config file 
	chdir /var/www/timeseries
	exec uwsgi --ini timeseries.ini
	```

2. Start the uwsgi process.

	```bash
	$ sudo start timeseries
	$ ps aux | grep timeseries.ini # This command is to check whether the process started successfully
	```

### Local Server Systemd init system

1. Create the upstart script `timeseries.service` in `/etc/systemd/system/`. Insert the following into the file:
	```bash
	[Unit]
 	Description=uWSGI instance to serve timeseries
 
 	[Service]
 	ExecStart=/bin/bash -c 'export PATH=/home/ubuntu/miniconda/bin:$PATH; source activate wofpy; cd /var/www/timeseries; uwsgi --ini timeseries.ini'
 
	[Install]
	WantedBy=multi-user.target
	```

2. Start the service by using the following command.
	```bash
	$ sudo systemctl start timeseries
	$ systemctl status timeseries # This command is to make sure the service is started and running correctly
	$ sudo systemctl enable timeseries # This command enables the code to run independently
	```

## Configuring NGINX

1. Create a new server block configuration file `timeseries` in `/etc/nginx/sites-available/`

	``` bash
	server {
	    listen 8080;
	    server_name 127.0.0.1;

	    location /odm2timeseries {
	        include uwsgi_params;
	        uwsgi_pass unix:/var/www/timeseries/timeseries.sock;
	    }
	}
	```

2. Enable the Nginx server block configuration by linking the file to the sites-enabled directory.

	```bash
	$ sudo ln -s /etc/nginx/sites-available/timeseries /etc/nginx/sites-enabled
	```

3. Test for syntax errors in the block config 

	```bash
	$ sudo nginx -t
	```

To view nginx errors checkout the log `/var/log/nginx/error.log`. Ensure that all files in the `timeseries` folder are still owned by www-data.

### AWS SysV init system

If no issues restart Nginx server 

```bash
$ sudo service nginx restart
```


### Local Server Systemd init system

After setting up nginx run the following command

```bash
$ sudo systemctl start nginx
$ sudo systemctl enable nginx
```


## Checking Live instance of WOFpy

Go to `ip:8080/odm2timeseries` and you should see WOFpy running. Click on the links available to see if the application is working properly.
