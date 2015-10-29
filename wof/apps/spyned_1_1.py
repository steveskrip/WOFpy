__author__ = 'cyoun'

import StringIO
import logging

from spyne.decorator import rpc
from spyne.model.complex import Array
from spyne.model.primitive import Unicode, AnyXml, Float, Boolean
from spyne.service import ServiceBase
from spyne.model.fault import Fault
from spyne.util import memoize
import wof

logger = logging.getLogger(__name__)

NSDEF = 'xmlns="http://www.cuahsi.org/waterML/1.1/"'

@memoize
def TWOFService(wof_inst,T, T_name):
    class WOFService(ServiceBase):

        @rpc(Array(Unicode), Unicode, _returns=AnyXml)
        def GetSitesObject(ctx, site=None, authToken=None):
            try:
                if site is not None:
                    siteArg = ','.join(str(s) for s in site)
                else:
                    siteArg = None
                logging.debug(site)
                logging.debug(siteArg)
                siteResponse = wof_inst.create_get_site_response(siteArg)
                outStream = StringIO.StringIO()
                siteResponse.export(outStream, 0, name_="sitesResponse",
                                    namespacedef_=NSDEF)
                return outStream.getvalue()
            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        # This is the one that returns WITH <![CDATA[...]]>
        @rpc(Array(Unicode), Unicode, _returns=T)
        def GetSites(ctx, site=None, authToken=None):
            siteResult = WOFService.GetSitesObject(ctx,site,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return siteResult
            return siteResult.replace('\n', '')

        @rpc(Float, Float, Float, Float, Boolean, Unicode, _returns=AnyXml)
        def GetSitesByBoxObject(ctx, west,south,north,east, IncludeSeries, authToken=None):
            try:
                siteResponse = \
                    wof_inst.create_get_site_box_response(west,south,north,east,IncludeSeries)
                outStream = StringIO.StringIO()
                siteResponse.export(outStream, 0, name_="sitesResponse",
                                    namespacedef_=NSDEF)
                return outStream.getvalue()
            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @rpc(Float, Float, Float, Float, Boolean, Unicode, _returns=T)
        def GetSitesByBox(ctx, west,south,north,east, IncludeSeries, authToken=None):
            sitesResult = WOFService.GetSitesByBoxObject(ctx,west,south,north,east,IncludeSeries,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return sitesResult
            return sitesResult.replace('\n', '')

        @rpc(Unicode, Unicode, _returns=AnyXml)
        def GetSiteInfoObject(ctx, site, authToken):
            try:
                siteInfoResponse = \
                    wof_inst.create_get_site_info_response(site)
                outStream = StringIO.StringIO()
                siteInfoResponse.export(outStream, 0, name_="sitesResponse",
                                    namespacedef_=NSDEF)
                return outStream.getvalue()
            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @rpc(Unicode, Unicode, _returns=T)
        def GetSiteInfo(ctx, site, authToken):
            siteinfoResult = WOFService.GetSiteInfoObject(ctx,site,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return siteinfoResult
            return siteinfoResult.replace('\n', '')

        @rpc(Array(Unicode), Unicode, _returns=AnyXml)
        def GetSiteInfoMultipleObject(ctx, site, authToken):
            if site is not None:
                siteArg = ','.join(str(s) for s in site)
            else:
                siteArg = None
            try:
                siteInfoResponse = \
                    wof_inst.create_get_site_info_multiple_response(siteArg)
                outStream = StringIO.StringIO()
                siteInfoResponse.export(outStream, 0, name_="sitesResponse",
                                    namespacedef_=NSDEF)
                return outStream.getvalue()
            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @rpc(Array(Unicode), Unicode, _returns=T)
        def GetSiteInfoMultiple(ctx, site, authToken):
            sitesinfoResult = WOFService.GetSiteInfoMultipleObject(ctx,site,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return sitesinfoResult
            return sitesinfoResult.replace('\n', '')

        @rpc(Unicode, Unicode, _returns=AnyXml)
        def GetVariableInfoObject(ctx, variable, authToken):
            try:
                variableInfoResponse = \
                    wof_inst.create_get_variable_info_response(variable)
                outStream = StringIO.StringIO()
                variableInfoResponse.export(outStream, 0,
                                            name_="variablesResponse",
                                            namespacedef_=NSDEF)
                return outStream.getvalue()
            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @rpc(Unicode, Unicode, _returns=T)
        def GetVariableInfo(ctx, variable, authToken):
            varinfoResult = WOFService.GetVariableInfoObject(ctx,variable,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return varinfoResult
            return varinfoResult.replace('\n', '')

        @rpc(Unicode, _returns=AnyXml)
        def GetVariablesObject(ctx,authToken=None):
            try:
                variableInfoResponse = \
                    wof_inst.create_get_variable_info_response()
                outStream = StringIO.StringIO()
                variableInfoResponse.export(outStream, 0,
                                            name_="variablesResponse",
                                            namespacedef_=NSDEF)
                return outStream.getvalue()
            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @rpc(Unicode, _returns=T)
        def GetVariables(ctx,authToken=None):
            varsResult = WOFService.GetVariablesObject(ctx,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return varsResult
            return varsResult.replace('\n', '')

        @rpc(Unicode, Unicode, Unicode, Unicode, _returns=AnyXml)
        def GetValuesObject(ctx, location, variable, startDate, endDate):
            try:
                timeSeriesResponse = wof_inst.create_get_values_response(
                        location, variable, startDate, endDate)
                outStream = StringIO.StringIO()
                timeSeriesResponse.export(
                    outStream, 0, name_="timeSeriesResponse",
                    namespacedef_=NSDEF)
                return outStream.getvalue()
            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @rpc(Unicode, Unicode, Unicode, Unicode, _returns=T)
        def GetValues(ctx, location, variable, startDate, endDate):
            valuesResult = WOFService.GetValuesObject(ctx,location,variable,startDate,endDate)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return valuesResult
            return valuesResult.replace('\n', '')

        @rpc(Unicode, Unicode, Unicode, Unicode, _returns=AnyXml)
        def GetValuesForASiteObject(ctx, site, startDate, endDate, authToken=None):
            try:
                timeSeriesResponse = wof_inst.create_get_values_site_response(
                        site, startDate, endDate)
                outStream = StringIO.StringIO()
                timeSeriesResponse.export(
                    outStream, 0, name_="timeSeriesResponse",
                    namespacedef_=NSDEF)
                return outStream.getvalue()
            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @rpc(Unicode, Unicode, Unicode, Unicode, _returns=T)
        def GetValuesForASite(ctx, site, startDate, endDate, authToken=None):
            valuesResult = WOFService.GetValuesForASiteObject(ctx,site,startDate,endDate,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return valuesResult
            return valuesResult.replace('\n', '')

    def _on_method_return_xml(ctx):
        # whatever etree element you return is the final xml
        # response, so to prevent the extraneous ("%sResult" %
        # method_name) result element, we just need to return an
        # element that has that element removed and replaced with
        # its child, which was the original response

        #TODO: how do we determine which method is being returned from?
        # Since I don't know, I am doing a dumb test for each one

        if wof._SERVICE_PARAMS["s_type"] in list(ctx.out_protocol.type):
            result_element_name_list = [
                'GetSitesObjectResult',
                'GetSiteInfoObjectResult',
                'GetVariableInfoObjectResult',
                'GetValuesObjectResult',
                'GetSitesByBoxObjectResult',
                'GetSiteInfoMultipleObjectResult',
                'GetVariablesObjectResult',
                'GetValuesForASiteObjectResult']
            element = ctx.out_document
            for result_element_name in result_element_name_list:
                result_element = element.find(
                        './/{%s}%s' % (element.nsmap['tns'], result_element_name))

                if result_element is not None:
                    parent = result_element.getparent()
                    children = result_element.getchildren()
                    parent.replace(result_element, children[0])
                    return ctx
        return

    WOFService.event_manager.add_listener('method_return_document', _on_method_return_xml)

    return WOFService