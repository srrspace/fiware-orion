# -*- coding: utf-8 -*-
"""
 Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U

 This file is part of Orion Context Broker.

 Orion Context Broker is free software: you can redistribute it and/or
 modify it under the terms of the GNU Affero General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.

 Orion Context Broker is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
 General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.

 For those usages not covered by this license please contact with
 iot_support at tid dot es
"""
__author__ = 'Iván Arias León (ivan dot ariasleon at telefonica dot com)'

import behave
from behave import step

from iotqautils.fabric_utils import FabricSupport
from iotqautils.mongo_utils import Mongo
from iotqautils.CB_v2_utils import CB
from iotqautils.helpers_utils import *

from tools.properties_config import Properties  # methods in properties class

behave.use_step_matcher("re")
__logger__ = logging.getLogger("steps")


@step(u'update properties test file from "([^"]*)" and sudo local "([^"]*)"')
def update_properties_file(context, properties_file, sudo_run):
    """
    update properties.py file from setting folder or jenkins console
    :param context:
    :param properties_file: file to get data to update properties.py
    """
    global properties_class
    __logger__.info(" >> config file used: '%s'", properties_file)
    properties_class = Properties()
    properties_class.update_properties_json_file(properties_file, sudo_run)
    __logger__.info(" >> properties.json is updated")


@step(u'update contextBroker config file and restart service')
def update_context_broker_config_file_and_restart_service(context):
    """
    updating /etc/sysconfig/contextBroker file an restarting service
    :param context:
    """
    global properties_class, props_cb, props_mongo
    __logger__.debug(" >> updating /etc/sysconfig/contextBroker file")
    props = properties_class.read_properties()  # properties dict
    props_cb = props["context_broker_env"]  # context broker properties dict
    props_mongo = props["mongo_env"]  # mongo properties dict
    __logger__.debug("properties dict: %s " % str(props))
    my_fab = FabricSupport(host=props_cb["CB_HOST"], user=props_cb["CB_FABRIC_USER"],
                           password=props_cb["CB_FABRIC_PASS"], cert_file=props_cb["CB_FABRIC_CERT"],
                           retry=props_cb["CB_FABRIC_RETRY"], hide=True, sudo=props_cb["CB_FABRIC_SUDO"])
    properties_class.update_context_broker_file(my_fab)
    __logger__.info(" >> updated /etc/sysconfig/contextBroker file")
    __logger__.debug(" >> restarting contextBroker service")
    my_fab.run("service contextBroker restart")
    __logger__.info(" >> restarted contextBroker service")


@step(u'verify contextBroker is installed successfully')
def verify_context_broker_is_installed_successfully(context):
    """
    verify contextBroker is installed successfully
    :param context:
    """
    global props_cb
    __logger__.debug(" >> verify if contextBroker is installed successfully")
    __logger__.debug("Sending a version request...")

    cb = CB(protocol=props_cb["CB_PROTOCOL"], host=props_cb["CB_HOST"], port=props_cb["CB_PORT"])
    resp = cb.get_version_request()
    if props_cb["CB_VERIFY_VERSION"].lower() == "true":
        resp_dict = convert_str_to_dict(str(resp.text), "JSON")
        assert resp_dict["orion"]["version"].find(
            props_cb["CB_VERSION"]) >= 0, " ERROR in context broker version  value, \n " \
                                          " expected: %s \n" \
                                          " installed: %s" % (props_cb["CB_VERSION"], resp_dict["orion"]["version"])
        __logger__.debug("-- version %s is correct in base request v2" % props_cb["CB_VERSION"])
    __logger__.info(" >> verified that contextBroker is installed successfully")


@step(u'verify mongo is installed successfully')
def verify_mongo_is_installed_successfully(context):
    """
    verify contextBroker is installed successfully
    :param context:
    """
    global props_mongo
    __logger__.debug(" >> verify if mongo is installed successfully")
    m = Mongo(host=props_mongo["MONGO_HOST"], port=props_mongo["MONGO_PORT"], user=props_mongo["MONGO_USER"],
              password=props_mongo["MONGO_PASS"], version=props_mongo["MONGO_VERSION"],
              verify_version=props_mongo["MONGO_VERIFY_VERSION"])
    m.connect()
    m.eval_version()
    m.disconnect()
    __logger__.info(" >> verified that mongo is installed successfully")