# Installing WOFpy on Linux with Little Bear River MySQL ODM2 test database

Notes mostly from @lsetiawan (with minor edits by @emiliom) on steps followed to successfully install WOFpy on Linux (Ubuntu 14) with the Little Bear MySQL ODM2 time series test database. Completed on 11/4/2016, with WOFpy and dependencies installed between 10/28 and 10/31/2016. No attempt has been made to expose the service endpoint to the internet.

These notes include installation of WOFpy from its `conda` package; downloading and installing the Litter Bear River (LBR) test database; configuring WOFpy for the LBR database; running WOFpy; and installing the WOFpy Docker image we created.

Note that this installation was in "testing" mode, not as a live service.

## Installing WOFpy:
1. Create the conda environment (after installing Anaconda or miniconda): `conda create -n wofpy -c ODM2 python=2.7 wofpy odm2api mysql-python`. *Note: `mysql-python` is not installed by the wofpy package*
2. Download the Little Bear River (LBR) test database from https://github.com/ODM2/ODM2/tree/master/usecases/littlebearriver
3.  If MySQL database was a stand alone in Unix, add to /etc/mysql/my.cnf : `lower_case_table_names = 1` under [mysqld]
4. Create ODM2 database in MySQL. At the bash shell where the LBR SQL file was downloaded: `mysql < LBR_MySQL_SmallExample.sql`
5. **NOTE: Sample database is missing featuregeometrywkt in samplingfeatures** In order to make WOFpy work, alter the table by adding featuregeometrywkt column, at the mysql client:
```sql
ALTER TABLE samplingfeatures ADD featuregeometrywkt VARCHAR (8000) NULL;
```
6. Clone https://github.com/ODM2/WOFpy.git
7. Change directory to `../WOFpy/examples/flask/odm2/timeseries/`
8. Activate the wofpy conda environment: `source activate wofpy`
9. Create a connection string: `nano private_config` and insert
``` bash
mysql+mysqldb://root:password@localhost:3306/ODM2
```
10. Run the wofpy server:
``` bash
$ python runserver_odm2_timeseries.py --config=odm2_config_timeseries.cfg --connection=private_config
```

## Extra Notes

### Non-fatal error messages
- On http://127.0.0.1:8080/odm2timeseries/rest/1_1/GetSiteInfo?site=odm2timeseries:USU-LBR-Mendon and http://127.0.0.1:8080/odm2timeseries/rest/1_1/GetSiteInfoMultple?site=odm2timeseries:USU-LBR-Mendon I am getting these non-fatal errors
``` bash
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
ERROR:root:bad datetime conversion
```

### Links to relevant WOFpy resources and documentation
- [Notes from Aug 12 weekly BiGCZ meeting, on Google Drive](https://docs.google.com/document/d/1Ok_lN37hdDXjD8H_ElOIRYbAHJ4_WPAPyxx0iiuSR8k/edit#bookmark=kix.iiqm28wbiruz). There are lots of links here to WOFpy documentation, plus other guidance and comments.
- A [github issue](https://github.com/ODM2/WOFpy/issues/59) that includes a lot of discussions and error reports. 
Initially it was focused on how to install the WOFpy package (and how to install and use miniconda ...). Then it got into installation and configuration errors people were running into.

## Installing WOFpy Docker image
We created a Docker Image for this WOFpy MySQL Example. It's [available here.](https://hub.docker.com/r/lsetiawan/wofpy/) On Mac or Linux, if you have Docker installed and have the docker engine running, just run this statement:
```bash
docker run --name test_wofpy -i -t -p 8080:8080 lsetiawan/wofpy /bin/bash
```
It's possible to instal the image on Windows as well, but we don't have instructions at this time.

The command above will initiate a docker container named `test_wofpy` with an open port of 8080, which matches with host port of 8080 so that you will be able to open WOFpy in `localhost:8080`

Once inside the docker container:
```bash
$ service mysql start
$ source activate wofpy
$ python /resources/WOFpy/examples/flask/odm2/timeseries/runserver_odm2_timeseries.py --config=/resources/WOFpy/examples/flask/odm2/timeseries/odm2_config_timeseries.cfg --connection=/resources/WOFpy/examples/flask/odm2/timeseries/private_config --port=8080
```

The series of commands above will run an instance of WOFpy at port 8080, follow the instruction by placing the given URL onto your host machine web browser.
