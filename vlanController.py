#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls, MAIN_DISPATCHER
from ryu.topology import switches, event
from ryu.ofproto import ofproto_v1_3 as ofproto
from ryu.lib.dpid import dpid_to_str, str_to_dpid
from ryu.lib import hub
from ryu import cfg
import argparse
# either take dpid from  terminal or read from yaml
config_parser = argparse.ArgumentParser(description='InterVLAN Routing Controller')
config_parser.add_argument('-c', action='store', dest='config_file',
                           default='/usr/local/etc/ryu/janus.yaml',
                           help='Pass a YAML config file to the app')

config_parser.add_argument('-p', action='store_true', default=False,
                           dest='enable_pbr',
                           help='Enable policy based routing')
config_parser.add_argument('-f', action='store', dest='flowtable_type',
                           default='multiple-flowtables',
                           help='Use single or multiple flow table')
config_parser.add_argument('-O', action='store', dest='OpenFlow_version',
                           default='1.3', help='Set OpenFlow protocl version')

