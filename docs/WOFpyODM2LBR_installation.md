
# Installing WOFpy with Little Bear River MySQL and SQLite ODM2 test database in "testing" and "production" modes.

These notes cover installation of `WOFpy` from its `conda`; downloading and installing the Little Bear River (LBR) ODM2 MySQL and SQLite test databases; configuring WOFpy for the LBR databases; and running WOFpy. *The instructions enable the creation of "live" web services exposed to external use.* 

Most of the steps were originally copied from [WOFpyODM2LBRtest_installation_notes.md](https://github.com/ODM2/WOFpy/blob/master/docs/WOFpyODM2LBRtest_installation_notes.md) with some modifications; we're no longer actively maintaining that page, but it still has useful content, including references to relevant discussions.

## Table of Contents

<!-- MarkdownTOC depth=3 autolink="true" bracket="round" -->

- [Testing Environments](#testing-environments)
    - [Amazon Web Services \(AWS\)](#amazon-web-services-aws)
- [Installing the LBR ODM2 MySQL test database](#installing-the-lbr-odm2-mysql-test-database)
- [Downloading the LBR ODM2 SQLite test database](#downloading-the-lbr-odm2-sqlite-test-database)
- [Installing WOFpy](#installing-wofpy)
- [Installing NGINX](#installing-nginx)
- [Setting up WOFpy for Testing](#setting-up-wofpy-for-testing)
    - [Get Configuration Folder](#get-configuration-folder)
    - [Edit Configuration `.cfg` files](#edit-configuration-cfg-files)
    - [Test `.cfg` files](#test-cfg-files)
    - [Set up runserver script](#set-up-runserver-script)
- [Setting  up WOFpy for Production](#setting--up-wofpy-for-production)
    - [Setup `wsgi.py`](#setup-wsgipy)
    - [Setup upstart script](#setup-upstart-script)
    - [Setup NGINX](#setup-nginx)
- [Checking Live instance of WOFpy](#checking-live-instance-of-wofpy)

<!-- /MarkdownTOC -->

## Testing Environments

We tested WOFpy installations on Amazon Web Services.
Deployment of WOFpy was done in an Ubuntu Server version 16.04. WOFpy is served by using [NGINX](https://www.nginx.com/) and [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/). **These instructions assume that Amazon AWS EC2 Instance is already set up.**

### [Amazon Web Services (AWS)](https://aws.amazon.com/) 

Note that this installation is currently (2017-3-1) [live on the cloud](http://52.40.105.124:8080/odm2timeseries/). It will be kept live only during active testing, and will be taken down without prior notice when active testing is over. It will be reactivated in the future as needed.

Specifications:
- Ubuntu 16.04
- MySQL 5.6
- NGINX 1.10.2

The AWS Ubuntu Server is running [Systemd init](http://www.freedesktop.org/wiki/Software/systemd/) system.

## Installing the LBR ODM2 MySQL test database

**Note: Do not use MySQL 5.7. We've identified a problem in MySQL 5.7 with loading from the LBR sample database into a geometry column. MySQL 5.6 and 5.5 have been tested successfully.**


1. Download the Little Bear River (LBR) test MySQL database

	```bash
	wget https://raw.githubusercontent.com/ODM2/ODM2/master/usecases/littlebearriver/sampledatabases/odm2_mysql/LBR_MySQL_SmallExample.sql
	```
2.  If MySQL database was a stand alone in Unix, add to /etc/mysql/my.cnf : `lower_case_table_names = 1` under [mysqld]
3. Create ODM2 database in MySQL. At the bash shell where the LBR SQL file was downloaded: 

    ```bash
    mysql -u root -p odm2 < LBR_MySQL_SmallExample.sql
    ```
4. **NOTE: Sample database is missing featuregeometrywkt in samplingfeatures** In order to make WOFpy work, alter the table by adding featuregeometrywkt column, at the mysql client:

	```sql
	ALTER TABLE samplingfeatures ADD featuregeometrywkt VARCHAR (8000) NULL;
	```

## Downloading the LBR ODM2 SQLite test database

Download the Little Bear River (LBR) test SQLite database from WOFpy test directory

	```bash
	wget https://github.com/ODM2/WOFpy/raw/master/test/odm2/ODM2.sqlite
	```

## Installing WOFpy

1. Install miniconda into the user home directory. `/home/ubuntu/miniconda`
	```bash
	wget http://bit.ly/miniconda -O miniconda.sh # defaults to Python 2.7 Miniconda
    bash miniconda.sh -b -p $HOME/miniconda

    export PATH="$HOME/miniconda/bin:$PATH"
    conda update conda --yes
	```

2. Create the "wofpy" conda environment: 
    ```bash
    conda create -n wofpy -c ODM2 -c conda-forge python=2.7 wofpy
    ```

## Installing NGINX

**Note: The installation step for NGINX should be the same for both server on AWS and local**

1. Install nginx into the system

	``` bash
	sudo apt install nginx
	```
    
	`NGINX` automatically start after the installation. You should get a welcome page:
	![nginxhome](./img/nginxhome.png)

	**This welcome page is located in `/var/www/html/`**
    
You can check the status of `NGINX` server by running   
```bash
systemctl status nginx
```

*look for `Active: active (running) since Mon 2017-05-15 14:51:45 UTC; 59min ago`*

## Setting up WOFpy for Testing

The steps below are used to setup WOFpy

### Get Configuration Folder
Retrieve WOFpy configuration scripts and files with `wofpy_config` in your `$HOME` directory.

```bash
wofpy_config wofpy
```

*The command above will create a folder called `wofpy` within your `$HOME` directory*

**Note: Currently the command only provide configurations for ODM2 TimeSeries**

### Edit Configuration `.cfg` files
1. Make a copy of `odm2_config_timeseries.cfg` in the newly created `wofpy` folder, so that we can have separate config file for `MySQL` and `SQLite`.
    ```bash
    cp wofpy/odm2_config_timeseries.cfg wofpy/odm2_config_mysql.cfg
    ```
2. Rename `odm2_config_timeseries.cfg` to make things clear that this is sqlite configuration by default.
    ```bash
    mv wofpy/odm2_config_timeseries.cfg wofpy/odm2_config_sqlite.cfg
    ```
3. Edit each `.cfg` file to reflect the correct settings. Example below is for `MySQL` database
    ```ini
    [WOF]
    # Edit this to a name that reflect the db, it will be used in the URL
    Network: MySQLODM2Timeseries 
    # Edit this to same name above
    Vocabulary: MySQLODM2Timeseries
    Menu_Group_Name: ODM2
    # Assumes we are using port 8080
    Service_WSDL: http://127.0.0.1:8080/soap/wateroneflow.wsdl 
    Timezone: 00:00
    TimezoneAbbreviation: GMT
    
    # Testing parameters
    [Default_Params]
    Site: USU-LBR-Mendon
    Variable: USU3
    StartDate: 2007-09-01T00:00:00
    EndDate: 2007-09-01T02:30:00

    [WOF_1_1]
    # Assumes we are using port 8080
    Service_WSDL: http://127.0.0.1:8080/soap/wateroneflow_1_1.wsdl 
    
    # Also Testing parameters (for WOF ver. 1.1)
    [Default_Params_1_1]
    West: -114
    South: 40
    East: -110
    North: 42
    
    # Not needed for multiple server (Production), set for (Testing) or comment out to use default path
    # [WOFPY]
    # Templates: ../../../../../wof/apps/templates
    
    # Information about the Database 
    # Avoid using localhost in place of 127.0.0.1 below, to minimize problems
    [Database]
    Connection_String: mysql+mysqldb://username:password:@127.0.0.1:3306/ODM2
    ```

### Test `.cfg` files

To test `.cfg` files run the command below after activating `wofpy` conda environment `source activate wofpy`:

First change to `wofpy` directory
```bash
cd $HOME/wofpy
```
- MySQL
    ```bash
    python runserver_odm2_timeseries.py --config odm2_config_mysql.cfg
    ```
- SQLite
    ```bash
    python runserver_odm2_timeseries.py --config odm2_config_sqlite.cfg
    ```
    
**If each instance works, we are ready to deploy the two together.**

### Set up runserver script

1. Make a new script called `runserver.py` within `wofpy` folder.
    ```bash
    touch runserver.py
    ```
2. Edit the script to match the content below.
    
    ```python
    from __future__ import (absolute_import, division, print_function)

    import argparse
    import configparser
    import logging
    import os
    import tempfile
    import sys

    from werkzeug.wsgi import DispatcherMiddleware
    from werkzeug.serving import run_simple
    from werkzeug.exceptions import NotFound

    import wof
    import wof.flask
    from wof.examples.flask.odm2.timeseries.odm2_timeseries_dao import Odm2Dao as timeseries

    M_CONFIG_FILE = os.path.join(os.path.curdir,'odm2_config_mysql.cfg')
    S_CONFIG_FILE = os.path.join(os.path.curdir,'odm2_config_sqlite.cfg')

    def get_connection(conf):
        # Parse connection from config file
        config = configparser.ConfigParser()
        with open(conf, 'r') as configfile:
            config.read_file(configfile)
            connection = config['Database']['Connection_String']

        return connection

    parser = argparse.ArgumentParser(description='start WOF for an ODM2 database.')
    parser.add_argument('--port',
                       help='Open port for server."', default=8080, type=int)
    args = parser.parse_args()

    m_dao = timeseries(get_connection(M_CONFIG_FILE))
    s_dao = timeseries(get_connection(S_CONFIG_FILE))

    m_conf = wof.core.wofConfig(m_dao, M_CONFIG_FILE)
    s_conf = wof.core.wofConfig(s_dao, S_CONFIG_FILE)

    app = wof.flask.create_wof_flask_multiple({m_conf, s_conf}, templates=wof._TEMPLATES)

    if __name__ == '__main__':

        url = "http://127.0.0.1:" + str(args.port)
        print("----------------------------------------------------------------")
        print("Service endpoints")
        for path in wof.flask.site_map_flask_wsgi_mount(app):
            print("{}{}".format(url, path))

        print("----------------------------------------------------------------")
        print("----------------------------------------------------------------")
        print("Access HTML descriptions of endpoints at ")
        for path in wof.site_map(app):
            print("{}{}".format(url, path))

        print("----------------------------------------------------------------")

        app.run(host='0.0.0.0', port=args.port, threaded=True)
    ```
3. Test that `runserver.py` will deploy WOFpy. Go to one of the endpoints provided, replacing `127.0.0.1` with your server ipaddress:

    ```bash
	source activate wofpy # first activate the correct conda environment
	python runserver.py
    ...
    Access HTML descriptions of endpoints at 
    http://127.0.0.1:8080/mysqlodm2timeseries/
    http://127.0.0.1:8080/mysqlodm2timeseries/rest_1_0/
    http://127.0.0.1:8080/mysqlodm2timeseries/rest_1_1/
    http://127.0.0.1:8080/mysqlodm2timeseries/rest_2/
    http://127.0.0.1:8080/sqliteodm2timeseries/
    http://127.0.0.1:8080/sqliteodm2timeseries/rest_1_0/
    http://127.0.0.1:8080/sqliteodm2timeseries/rest_1_1/
    http://127.0.0.1:8080/sqliteodm2timeseries/rest_2/
    ...
    ```

    You should get a result like below. If so, you have successfully deployed `WOFpy` testing server:
	![wofpy home](./img/wofpyhome.png)
    


## Setting  up WOFpy for Production

Follow the same step as Test then continue here.

*Currently `wofpy_config` does not provide, low level settings for `WOFpy` production deployment. You have to clone the `WOFpy` repository to get those settings.*

1. Clone `WOFpy` repository into `$HOME` directory.
    ```bash
    git clone https://github.com/ODM2/WOFpy.git
    ```
2. Copy `production_configs` into `$HOME` directory
    ```bash
    cp -r $HOME/WOFpy/wof/examples/production_configs $HOME/
    ```
    
   *These production config files will go to multiple places, there should be 5 files.*

### Setup `wsgi.py`

1. Move `wsgi.py` and `wofpy.ini` to the same folder as your `runserver` script. In this example `$HOME/wofpy`.
    ```bash
    mv $HOME/production_configs/wsgi.py $HOME/wofpy/
    mv $HOME/production_configs/wofpy.ini $HOME/wofpy/
    ```

2. Set the secret key within `wsgi.py` and python interpreter. To create secret key, run commands below in `python`
    ```bash
    python
    ```
    
    ```python
    >>> import os
    >>> os.urandom(24)
     '4\x9eQ\xb5\xce\xf9,\xf2\x83\xa6\x96\x98o\xbf\xfb0\x1c\x1b\x97\xa0\x1d|\xd4N'
    ```
    
    Copy and paste result into `wsgi.py`
    ```python
    #! /home/ubuntu/miniconda/envs/wofpy/bin/python
    from runserver import app as application
    application.secret_key = '4\x9eQ\xb5\xce\xf9,\xf2\x83\xa6\x96\x98o\xbf\xfb0\x1c\x1b\x97\xa0\x1d|\xd4N'
    ```
3. Testing uWSGI with WSGI. Do this by passing name of entry point, specify socket, and protocol (make sure that wofpy conda environment is still active). Go to one of the previous endpoints on your browser once it is deployed.

	``` bash
	uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi
	```
4. If everything works, now deactivate the conda environment. `$ source deactivate`
5. Stage WOFpy for Production.
    - Move `$HOME/wofpy` folder to `/var/www/` and change user and group to `www-data` so that nginx can read and write to it.
        
        ```bash
        sudo mv $HOME/wofpy /var/www/
        sudo chown -R www-data:www-data /var/www/wofpy
        ```
        
6. Enhance Security for WOFpy.     
    - Move `.cfg` files to some private directory. In this example, it is moved to `wofpy_prod` in `$HOME` folder. **THIS IS HIGHLY RECOMMENDED**
        
        ```bash
        mkdir $HOME/wofpy_prod
        sudo mv /var/www/wofpy/*.cfg /home/ubuntu/wofpy_prod/
        ```
        
    - Edit `runserver.py` to use the new path.
        
        ```python
        M_CONFIG_FILE = os.path.join('/home/ubuntu', 'wofpy_prod', 'odm2_config_mysql.cfg')
        S_CONFIG_FILE = os.path.join('/home/ubuntu', 'wofpy_prod','odm2_config_sqlite.cfg')
        ```

### Setup upstart script

1. Move the upstart script `$HOME/production_configs/wofpy.service` to `/etc/systemd/system/`. 
    ```bash
    sudo mv $HOME/production_configs/wofpy.service /etc/systemd/system/
    ```

2. Edit ExecStart to match your file paths:
	```ini
	ExecStart=/bin/bash -c 'export PATH=$HOME/miniconda/bin:$PATH; source activate wofpy; cd /var/www/wofpy; uwsgi --ini wofpy.ini'
	```

3. Start the service by using the following command.
	```bash
	sudo systemctl start wofpy
	systemctl status wofpy # This command is to make sure the service is started and running correctly
	sudo systemctl enable wofpy # This command enables the code to run independently
	```


### Setup NGINX

1. Move the server block configuration `$HOME/production_configs/wofpy` to `/etc/nginx/sites-available/`.
    ```bash
    sudo mv $HOME/production_configs/wofpy /etc/nginx/sites-available/
    ```

2. Edit the server block configuration file to match the endpoints. `http://127.0.0.1:8080/mysqlodm2timeseries/` and `http://127.0.0.1:8080/sqliteodm2timeseries/`

	``` bash
	location /mysqlodm2timeseries {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/wofpy/wofpy.sock;
    }
    
    location /sqliteodm2timeseries {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/wofpy/wofpy.sock;
    }
	```

3. Enable the Nginx server block configuration by linking the file to the sites-enabled directory.

	```bash
	sudo ln -s /etc/nginx/sites-available/wofpy /etc/nginx/sites-enabled
	```

4. Test for syntax errors in the block config 

	```bash
	sudo nginx -t
	```

    To view nginx errors checkout the log `/var/log/nginx/error.log`.

5. After setting up nginx run the following command
    
    ```bash
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    ```


## Checking Live instance of WOFpy

Go to `ip:8080/mysqlodm2timeseries` and `ip:8080/sqliteodm2timeseries`. You should see WOFpy running. Click on the links available to see if the application is working properly.
