from spyne.interface import InterfaceDocumentBase
import logging
from jinja2 import Environment, Template, PackageLoader, FileSystemLoader

# from sypne/interface/wsdl/wsdl1.py
TEMPLATES = 'D:/dev_odm/WOFpy/wof/apps/templates'
def check_method_port(service, method):
    if len(service.__port_types__) != 0 and method.port_type is None:
        raise ValueError("""
            A port must be declared in the RPC decorator if the service
            class declares a list of ports
            Method: %r
            """ % method.name)

    if (not method.port_type is None) and len(service.__port_types__) == 0:
        raise ValueError("""
            The rpc decorator has declared a port while the service class
            has not.  Remove the port declaration from the rpc decorator
            or add a list of ports to the service class
            """)
    try:
        if (not method.port_type is None):
            index = service.__port_types__.index(method.port_type)

    except ValueError as e:
        raise ValueError("""
            The port specified in the rpc decorator does not match any of
            the ports defined by the service class
            """)

class WofWSDL_1_0(InterfaceDocumentBase):
    def __init__(self, interface=None, _with_partnerlink=False):
        super(WofWSDL_1_0, self).__init__(interface)

    def build_interface_document(self, url):
        """This function is supposed to be called just once, as late as possible
        into the process start. It builds the interface document and caches it
        somewhere. The overriding function should never call the overridden
        function as this may result in the same event firing more than once.
        """
        # cb_binding = None
        # for s in self.interface.services:
        #     if not s.is_auxiliary():
        #         # cb_binding = self.add_bindings_for_methods(s, root,
        #         #                                    service_name, cb_binding)
        #         cb_binding = self.add_bindings_for_methods(s, None,
        #                                            None, cb_binding)
        doc = self.get_wsdl_1_0( url )
        return doc

    def get_interface_document(self):
        """This function is called by server transports that try to satisfy the
        request for the interface document. This should just return a previously
        cached interface document.
        """

        raise NotImplementedError('Extend and override.')

    def add_bindings_for_methods(self, service, root, service_name,
                                     cb_binding):

        pref_tns = self.interface.get_namespace_prefix(self.interface.get_tns())

        # def inner(method, binding):
        #     operation = etree.Element(WSDL11("operation"))
        #     operation.set('name', method.operation_name)
        #
        #     soap_operation = SubElement(operation, WSDL11_SOAP("operation"))
        #     soap_operation.set('soapAction', method.operation_name)
        #     soap_operation.set('style', 'document')
        #
        #     # get input
        #     input = SubElement(operation, WSDL11("input"))
        #     input.set('name', method.in_message.get_element_name())
        #
        #     soap_body = SubElement(input, WSDL11_SOAP("body"))
        #     soap_body.set('use', 'literal')
        #
        #     # get input soap header
        #     in_header = method.in_header
        #     if in_header is None:
        #         in_header = service.__in_header__
        #
        #     if not (in_header is None):
        #         if isinstance(in_header, (list, tuple)):
        #             in_headers = in_header
        #         else:
        #             in_headers = (in_header,)
        #
        #         if len(in_headers) > 1:
        #             in_header_message_name = ''.join((method.name,
        #                                               _in_header_msg_suffix))
        #         else:
        #             in_header_message_name = in_headers[0].get_type_name()
        #
        #         for header in in_headers:
        #             soap_header = SubElement(input, WSDL11_SOAP('header'))
        #             soap_header.set('use', 'literal')
        #             soap_header.set('message', '%s:%s' % (
        #                         header.get_namespace_prefix(self.interface),
        #                         in_header_message_name))
        #             soap_header.set('part', header.get_type_name())
        #
        #     if not (method.is_async or method.is_callback):
        #         output = SubElement(operation, WSDL11("output"))
        #         output.set('name', method.out_message.get_element_name())
        #
        #         soap_body = SubElement(output, WSDL11_SOAP("body"))
        #         soap_body.set('use', 'literal')
        #
        #         # get output soap header
        #         out_header = method.out_header
        #         if out_header is None:
        #             out_header = service.__out_header__
        #
        #         if not (out_header is None):
        #             if isinstance(out_header, (list, tuple)):
        #                 out_headers = out_header
        #             else:
        #                 out_headers = (out_header,)
        #
        #             if len(out_headers) > 1:
        #                 out_header_message_name = ''.join((method.name,
        #                                                 _out_header_msg_suffix))
        #             else:
        #                 out_header_message_name = out_headers[0].get_type_name()
        #
        #             for header in out_headers:
        #                 soap_header = SubElement(output, WSDL11_SOAP("header"))
        #                 soap_header.set('use', 'literal')
        #                 soap_header.set('message', '%s:%s' % (
        #                         header.get_namespace_prefix(self.interface),
        #                         out_header_message_name))
        #                 soap_header.set('part', header.get_type_name())
        #
        #         if not (method.faults is None):
        #             for f in method.faults:
        #                 wsdl_fault = SubElement(operation, WSDL11("fault"))
        #                 wsdl_fault.set('name', f.get_type_name())
        #
        #                 soap_fault = SubElement(wsdl_fault, WSDL11_SOAP("fault"))
        #                 soap_fault.set('name', f.get_type_name())
        #                 soap_fault.set('use', 'literal')
        #
        #     if method.is_callback:
        #         relates_to = SubElement(input, WSDL11_SOAP("header"))
        #
        #         relates_to.set('message', '%s:RelatesToHeader' % pref_tns)
        #         relates_to.set('part', 'RelatesTo')
        #         relates_to.set('use', 'literal')
        #
        #         cb_binding.append(operation)
        #
        #     else:
        #         if method.is_async:
        #             rt_header = SubElement(input, WSDL11_SOAP("header"))
        #             rt_header.set('message', '%s:ReplyToHeader' % pref_tns)
        #             rt_header.set('part', 'ReplyTo')
        #             rt_header.set('use', 'literal')
        #
        #             mid_header = SubElement(input, WSDL11_SOAP("header"))
        #             mid_header.set('message', '%s:MessageIDHeader' % pref_tns)
        #             mid_header.set('part', 'MessageID')
        #             mid_header.set('use', 'literal')
        #
        #         binding.append(operation)

        port_type_list = service.get_port_types()
        # if len(port_type_list) > 0:
        #     for port_type_name in port_type_list:
        #
        #         # create binding nodes
        #         binding = SubElement(root, WSDL11("binding"))
        #         binding.set('name', port_type_name)
        #         binding.set('type', '%s:%s'% (pref_tns, port_type_name))
        #
        #         transport = SubElement(binding, WSDL11_SOAP("binding"))
        #         transport.set('style', 'document')
        #
        #         for m in service.public_methods.values():
        #             if m.port_type == port_type_name:
        #                 inner(m, binding)
        #
        # else:
        #     # here is the default port.
        #     if cb_binding is None:
        #         cb_binding = SubElement(root, WSDL11("binding"))
        #         cb_binding.set('name', service_name)
        #         cb_binding.set('type', '%s:%s'% (pref_tns, service_name))
        #
        #         transport = SubElement(cb_binding, WSDL11_SOAP("binding"))
        #         transport.set('style', 'document')
        #         transport.set('transport', self.interface.app.transport)
        #
        #     for m in service.public_methods.values():
        #         inner(m, cb_binding)

        return cb_binding
    # def _add_port_to_service(self, service, port_name, binding_name):
    #     """ Builds a wsdl:port for a service and binding"""
    #
    #     pref_tns = self.interface.get_namespace_prefix(self.interface.tns)
    #
    #     wsdl_port = SubElement(service, WSDL11("port"))
    #     wsdl_port.set('name', port_name)
    #     wsdl_port.set('binding', '%s:%s' % (pref_tns, binding_name))
    #
    #     addr = SubElement(wsdl_port, WSDL11_SOAP("address"))
    #     addr.set('location', self.url)

    def get_wsdl_1_0(self, url ):
            env = Environment(loader=FileSystemLoader(TEMPLATES))
            template = env.get_template('wsdl_temp.wsdl')
            response = template.render(serv_loc=url)
            response = response.encode('utf-8')
            #response.headers['Content-Type'] = 'text/xml'

            return response

class WofWSDL_1_1(InterfaceDocumentBase):
    def __init__(self, interface=None, _with_partnerlink=False):
        super(WofWSDL_1_1, self).__init__(interface)

    def build_interface_document(self, url):
        """This function is supposed to be called just once, as late as possible
        into the process start. It builds the interface document and caches it
        somewhere. The overriding function should never call the overridden
        function as this may result in the same event firing more than once.
        """
        doc = self.get_wsdl_1_1( url )
        return doc

    def get_interface_document(self):
        """This function is called by server transports that try to satisfy the
        request for the interface document. This should just return a previously
        cached interface document.
        """

        raise NotImplementedError('Extend and override.')

    # def _add_port_to_service(self, service, port_name, binding_name):
    #     """ Builds a wsdl:port for a service and binding"""
    #
    #     pref_tns = self.interface.get_namespace_prefix(self.interface.tns)
    #
    #     wsdl_port = SubElement(service, WSDL11("port"))
    #     wsdl_port.set('name', port_name)
    #     wsdl_port.set('binding', '%s:%s' % (pref_tns, binding_name))
    #
    #     addr = SubElement(wsdl_port, WSDL11_SOAP("address"))
    #     addr.set('location', self.url)

    def get_wsdl_1_1(self, url ):
            env = Environment(loader=FileSystemLoader(TEMPLATES))
            template = env.get_template('wsdl_1_1_template.wsdl')
            response = template.render(serv_loc=url)
            response = response.encode('utf-8')
            #response.headers['Content-Type'] = 'text/xml'

            return response