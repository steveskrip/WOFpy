from flask import Flask, render_template, current_app, make_response, request

import config
import datetime

#TODO: Error handlers (404, etc.)
def create_app(wof_inst, wof_inst_1_1, soap_service_url=None, soap_service_1_1_url=None):
    app = Flask(__name__)

    app.config.from_object(config.Config)
    app.wof_inst = wof_inst
    app.wof_inst_1_1 = wof_inst_1_1
    path = wof_inst.network
    servicesPath =  '/'+wof_inst.network

    #@app.route( '/')
    def index():
        return render_template('index.html',
                               rest10=path+'/rest_1_0/',
                               rest11=path+'/rest_1_1/',
                               rest2=path+'/rest_2/',
                               soap10=path+'/soap/wateroneflow.wsdl',
                               soap11=path+'/soap/wateroneflow_1_1.wsdl',
                               p=current_app.wof_inst.network)

    app.add_url_rule(servicesPath+'/', 'index', index)

    def index_2_0():
        return render_template('index_2.html',
                       path= path + '/rest/2/',
                       p=current_app.wof_inst.network,
                       s=current_app.wof_inst.default_site,
                       v=current_app.wof_inst.default_variable,
                       sd=current_app.wof_inst.default_start_date,
                       ed=current_app.wof_inst.default_end_date,
                       u=current_app.wof_inst.default_unitid,
                       sm=current_app.wof_inst.default_samplemedium)
    app.add_url_rule(servicesPath+'/rest_2/', 'index_2_0', index_2_0)

    if wof_inst is not None:
        if not 'SOAP_SERVICE_URL' in app.config and soap_service_url:
            app.config['SOAP_SERVICE_URL'] = soap_service_url

        #@app.route('/rest_1_0/')
        def index_1_0():
            return render_template('index_1_0.html',
                           path= path + '/rest/1_0/',
                           p=current_app.wof_inst.network,
                           s=current_app.wof_inst.default_site,
                           v=current_app.wof_inst.default_variable,
                           sd=current_app.wof_inst.default_start_date,
                           ed=current_app.wof_inst.default_end_date,
                           u=current_app.wof_inst.default_unitid,
                           sm=current_app.wof_inst.default_samplemedium)
        app.add_url_rule(servicesPath+'/rest_1_0/', 'index_1_0', index_1_0)

        # #@app.route('/rest/1_0/GetValuesWML2', methods=['GET'])
        # def get_values_wml2():
        #     """
        #     Experimental/Demo WaterML2-formatted Values response.
        #     """
        #
        #     #TODO: Make this better once WaterML2 Schema is better understood
        #     # and/or best practices for using it are agreed to.
        #
        #     siteArg = request.args.get('location', None)
        #     varArg = request.args.get('variable', None)
        #     startDateTime = request.args.get('startDate', None)
        #     endDateTime = request.args.get('endDate', None)
        #
        #     if (siteArg == None or varArg == None):
        #         return "Must enter a site code (location) and a variable code \
        #             (variable)"
        #
        #     siteCode = siteArg.replace(current_app.wof_inst.network + ':', '')
        #     varCode = varArg.replace(current_app.wof_inst.network + ':', '')
        #
        #     data_values = current_app.wof_inst.dao.get_datavalues(siteCode, varCode,
        #                                                   startDateTime,
        #                                                   endDateTime)
        #
        #     site_result = current_app.wof_inst.dao.get_site_by_code(siteCode)
        #     variable_result = current_app.wof_inst.dao.get_variable_by_code(varCode)
        #
        #     if (data_values is not None):
        #         firstMethod = data_values[0].MethodID
        #         method_result = current_app.wof_inst.dao.get_method_by_id(firstMethod)
        #
        #     current_date = str(datetime.datetime.now().isoformat())
        #
        #     response = make_response(render_template('wml2_values_template.xml',
        #                                     current_date=current_date,
        #                                     data_values=data_values,
        #                                     site_result=site_result,
        #                                     variable_result=variable_result,
        #                                     method_result=method_result ))
        #
        #     response.headers['Content-Type'] = 'text/xml'
        #
        #     return response
        # app.add_url_rule(servicesPath+'/rest/1_0/GetValuesWML2', 'get_values_wml2', get_values_wml2)

        #@app.route('/soap/wateroneflow.wsdl')
        def get_wsdl():
        #TODO: The WSDL should be served separately from the Flask application.
        # Come up with a better way to do this.
            network = current_app.wof_inst.network.lower()

            try:
                serv_loc = current_app.config['SOAP_SERVICE_URL']
            except KeyError:
                serv_loc = current_app.config.get(
                    'SOAP_SERVICE_URL',
                    '%s/wateroneflow/' % request.url.rsplit('/', 1)[0])

            response = make_response(render_template('wsdl_temp.wsdl',
                                             serv_loc=serv_loc,
                                             network=network))

            response.headers['Content-Type'] = 'text/xml'
            return response
        app.add_url_rule(servicesPath+'/soap/wateroneflow.wsdl', 'get_wsdl', get_wsdl)

    if wof_inst_1_1 is not None:
        if not 'SOAP_SERVICE_URL_1_1' in app.config and soap_service_1_1_url:
            app.config['SOAP_SERVICE_URL_1_1'] = soap_service_1_1_url

        #@app.route('/rest_1_1/')
        def index_1_1():
            return render_template('index_1_1.html',
                           path=path+'/rest/1_1/',
                           p=current_app.wof_inst_1_1.network,
                           s=current_app.wof_inst_1_1.default_site,
                           v=current_app.wof_inst_1_1.default_variable,
                           sd=current_app.wof_inst_1_1.default_start_date,
                           ed=current_app.wof_inst_1_1.default_end_date,
                           w=current_app.wof_inst_1_1.default_west,
                           so=current_app.wof_inst_1_1.default_south,
                           n=current_app.wof_inst_1_1.default_north,
                           e=current_app.wof_inst_1_1.default_east)
        app.add_url_rule(servicesPath+'/rest_1_1/', 'index_1_1', index_1_1)

        #@app.route('/soap/wateroneflow_1_1.wsdl')
        def get_wsdl_1_1():
        #TODO: The WSDL should be served separately from the Flask application.
        # Come up with a better way to do this.
            network = current_app.wof_inst_1_1.network.lower()

            try:
                serv_loc = current_app.config['SOAP_SERVICE_URL_1_1']
            except KeyError:
                serv_loc = current_app.config.get(
                    'SOAP_SERVICE_URL_1_1',
                    '%s/wateroneflow_1_1/' % request.url.rsplit('/', 1)[0])

            response = make_response(render_template('wsdl_1_1_template.wsdl',
                                             serv_loc=serv_loc,
                                             network=network))

            response.headers['Content-Type'] = 'text/xml'
            return response
        app.add_url_rule(servicesPath+'/soap/wateroneflow_1_1.wsdl', 'get_wsdl_1_1', get_wsdl_1_1)

        # #@app.route('/rest/1_1/GetValuesWML2', methods=['GET'])
        # def get_values_wml2_1_1():
        #     """
        #     Experimental/Demo WaterML2-formatted Values response.
        #     """
        #
        #     #TODO: Make this better once WaterML2 Schema is better understood
        #     # and/or best practices for using it are agreed to.
        #
        #     siteArg = request.args.get('location', None)
        #     varArg = request.args.get('variable', None)
        #     startDateTime = request.args.get('startDate', None)
        #     endDateTime = request.args.get('endDate', None)
        #
        #     if (siteArg == None or varArg == None):
        #         return "Must enter a site code (location) and a variable code \
        #             (variable)"
        #
        #     siteCode = siteArg.replace(current_app.wof_inst.network + ':', '')
        #     varCode = varArg.replace(current_app.wof_inst.network + ':', '')
        #
        #     data_values = current_app.wof_inst.dao.get_datavalues(siteCode, varCode,
        #                                                   startDateTime,
        #                                                   endDateTime)
        #     if isinstance(data_values,dict):
        #         for key in data_values.keys():
        #             data_values = data_values[key]
        #             break
        #
        #     site_result = current_app.wof_inst.dao.get_site_by_code(siteCode)
        #     variable_result = current_app.wof_inst.dao.get_variable_by_code(varCode)
        #
        #     if (data_values is not None):
        #         firstMethod = data_values[0].MethodID
        #         method_result = current_app.wof_inst.dao.get_method_by_id(firstMethod)
        #
        #     current_date = str(datetime.datetime.now().isoformat())
        #
        #     response = make_response(render_template('wml2_values_template.xml',
        #                                     current_date=current_date,
        #                                     data_values=data_values,
        #                                     site_result=site_result,
        #                                     variable_result=variable_result,
        #                                     method_result=method_result ))
        #
        #     response.headers['Content-Type'] = 'text/xml'
        #
        #     return response
        # app.add_url_rule(servicesPath+'/rest/1_1/GetValuesWML2', 'get_values_wml2_1_1', get_values_wml2_1_1)

    return app
