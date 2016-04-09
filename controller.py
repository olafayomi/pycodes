# Name: MyController.py
# Author : Dimeji Fayomi
# Created : 8 April 2016
# Last Modified :
# Version : 1.0
# Description: This Ryu application can be used to turn 
#              an OpenFlow switch(specifically a Zodiac FX
#              network development board) into a transparent
#              intercept or monitor device between an Optical
#              Network Termination device and a home gateway
#              device.

#!/usr/bin/env python
#-*- coding:utf-8 -*-
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import *
from ryu.topology import switches, event
from ryu.ofproto import ofproto_v1_3 as ofproto
from ryu.lib import hub
from ryu.lib.mac import *
from ryu.lib.dpid import *
from ryu.lib import hub
from ryu.lib.packet.ethernet import ethernet
from ryu.lib.packet.vlan import *
from ryu.lib.packet import ether_types as ether
from ryu.lib.packet.ipv4 import  *
from ryu.lib.packet.ipv6 import  *
from ryu.lib.packet import packet
from ryu.lib.packet.icmp import *
from ryu.lib.packet.icmpv6 import *
from ryu import cfg
import logging
import time
# Logging
log  = logging.getLogger('Controller')
handler = logging.StreamHandler()
log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
formatter = logging.Formatter(log_format, '%b %d %H:%M:%S')
handler.setFormatter(formatter)
log.addHandler(handler)
log.propagate = 0
log.setLevel(logging.INFO)




# RYU application class
class MyController(app_manager.RyuApp):
    #Listen to the Ryu topology change events
    _CONTEXTS = {'switches': switches.Switches }
    OFP_VERSIONS = [ofproto.OFP_VERSION]

    def __init__(self,*args,**kwargs):
       super(MyController, self).__init__(*args,**kwargs)
       self._switches = kwargs['switches']


    #Configure flow table to install
    #rules
    def configure_flow_table(self, dp):
       ofp_parser = dp.ofproto_parser
       ofp = dp.ofproto
       ofreq = ofp_parser.OFPTableMod(dp, ofp.OFPTT_ALL,3)
       dp.send_msg(ofreq)

    # Install a flow on the datapath
    def add_flow(self,dp,match,actions):
       ofp_parser = dp.ofproto_parser
       table_id = 0
       ofp = dp.ofproto
       cookie = cookie_mask = tabled_id = 0
       priority = 100
       idle_timeout = hard_timeout = 0
       buffer_id = ofp.OFP_NO_BUFFER
       inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                                actions)]
       msg = ofp_parser.OFPFlowMod(dp,cookie,cookie_mask,\
                                   table_id,ofp.OFPFC_ADD,\
                                   idle_timeout,hard_timeout,\
                                   priority,buffer_id,\
                                   ofp.OFPP_ANY,ofp.OFPG_ANY,\
                                   ofp.OFPFF_SEND_FLOW_REM,\
                                   match,inst)
       dp.send_msg(msg)





    # Event handler for switch start up
    @set_ev_cls(event.EventSwitchEnter, MAIN_DISPATCHER)
    def handler_datapath_enter(self, ev):
       dp = ev.switch.dp
       dp_id = dp.id
       ofp_parser  = dp.ofproto_parser
       ofp = dp.ofproto

       log.info("INFO:MyController:Datapath is up (dp_id=%s)",\
                dpid_to_str(dp_id))
       #Configure table
       self.configure_flow_table(dp)
       # Install simple rules for ports
       for port in dp.ports:
          if port <= dp.ofproto.OFPP_MAX:
             port_name = dp.ports[port].name
             port_no  = dp.ports[port].port_no
             port_hw_addr = dp.ports[port].hw_addr
             port_state = dp.ports[port].state
             log.info("INFO:MyController: Port:%s,\
                       Number:%s, Addr:%s is up,\
                       Port-State:%s",\
                       port_name, port_no,port_hw_addr,\
                       port_state)
             log.info("INFO:ofp.OFPPS_LINK_DOWN: %s,\
                            ofp.OFPPS_BLOCKED: %s,\
                            ofp.OFPPS_LIVE: %s",\
                            ofp.OFPPS_LINK_DOWN,\
                            ofp.OFPPS_BLOCKED,\
                            ofp.OFPPS_LIVE)
             if port_no == 1:
                match = ofp_parser.OFPMatch(in_port=1)
                actions = [ofp_parser.OFPActionSetField(eth_src=('90:e2:ba:8f:a8:c4')),\
                           ofp_parser.OFPActionSetField(eth_dst=('24:00:ba:dc:5c:78')),\
                           ofp_parser.OFPActionOutput(port=2)]
                self.add_flow(dp,match,actions)
                log.info("INFO:Rule installed for port 1")

                #match=ofp_parser.OFPMatch(None)
                #actions = [ofp_parser.OFPActionOutput(ofp.OFPP_CONTROLLER, 65509)]
                #self.add_flow(dp,match,actions)


             if port_no == 2:
                match = ofp_parser.OFPMatch(in_port=2)
                actions = [ofp_parser.OFPActionSetField(eth_dst=('90:e2:ba:8f:a8:c4')),\
                           ofp_parser.OFPActionSetField(eth_src=('24:00:ba:dc:5c:78'))]
                actions += [ofp_parser.OFPActionOutput(ofp.OFPP_CONTROLLER, 65509)]
                self.add_flow(dp,match,actions)
                log.info("INFO:Rule installed for port 2")




    # Handle packet-in  to the controller
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def on_packet_in(self,ev):
       msg = ev.msg
       dp = msg.datapath
       ofp = dp.ofproto
       ofp_parser = dp.ofproto_parser
       pkt = packet.Packet(data=msg.data)
       pkt_eth =  pkt.get_protocol(ethernet)
       pkt_vlan = pkt.get_protocol(vlan)
       in_port = msg.match['in_port']
       log.info("Packet came from port:%s",in_port)
       for protocol in pkt.protocols:
          log.info("Protocol: %s",protocol)


       if in_port == 2:
          out_port = 1
          #TODO: 
          # Good things like monitor incoming packets,
          # log and/or drop suspicious incoming 
          # packets, apply QoS to certain packets.

          #  Bad things like modifying packets going out
          #  of the network, writing packets to disk for 
          #  later analysis and/or just being generally malicious
          self.send_pkt_out(dp,out_port,msg.data)
          log.info("Sent packet to port: %s",out_port)


    def send_pkt_out(self,dp,port,msg_data):
       ofp = dp.ofproto
       ofp_parser = dp.ofproto_parser
       actions = [ofp_parser.OFPActionOutput(port, len(msg_data))]
       buffer_id = ofp.OFP_NO_BUFFER
       in_port = ofp.OFPP_CONTROLLER
       packet_out = ofp_parser.OFPPacketOut(dp,
                               buffer_id,
                               in_port,
                               actions,msg_data)
       dp.send_msg(packet_out)



