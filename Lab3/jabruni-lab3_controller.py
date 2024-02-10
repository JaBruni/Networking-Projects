# Lab3 Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)

#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core

# You can check if IP is in subnet with 
# IPAddress("192.168.0.1") in IPNetwork("192.168.0.0/24")
# install with:
# sudo apt install python-netaddr
from netaddr import IPNetwork, IPAddress

import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Routing (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)
  
  # Given an IP (either an IP object or a string) and a subnet ID
  # (as a string representing a number or an actual number), this
  # function returns whether the given IP is in the subnet
  # 10.0.[subnet ID].0/24.
  def inSubnet(self, ip_obj, subnet_id):
    return IPAddress(str(ip_obj)) in IPNetwork("10.0." + str(subnet_id) + ".0/24")

  def do_routing (self, packet, packet_in, port_on_switch, switch_id):
    # port_on_swtich - the port on which this packet was received
    # switch_id - the switch which received this packet

    # Your code here
    icmp = packet.find('icmp')
    tcp = packet.find('tcp')
    ipv4 = packet.find('ipv4')

    def accept(end_port):
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.actions.append(of.ofp_action_output(port = end_port))
      msg.data = packet_in
      self.connection.send(msg)

    def drop():
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.data = packet_in
      self.connection.send(msg)


    if icmp:
      dst = str(ipv4.dstip)
      src = str(ipv4.srcip)
      if switch_id == 1:
        if self.inSubnet(dst, 0):
          if dst == '10.0.0.1':
            end_port = 1
            accept(1)
          elif dst == '10.0.0.2':
            end_port = 2
            accept(2)
        if self.inSubnet(dst, 1):
            end_port = 8
            accept(8)
       
      elif switch_id == 2:
        if self.inSubnet(dst,0):
            end_port = 11
            accept(11)
        if self.inSubnet(dst,1):
            end_port = 9
            accept(9)
        else:
          drop()
      elif switch_id == 3:
        if self.inSubnet(dst, 2):
          if dst == '10.0.2.1':
            end_port = 5
            accept(5)
          elif dst == '10.0.2.2':
            end_port = 6
            accept(6)
        if self.inSubnet(dst, 1):
          end_port = 7
          accept(7)
      elif switch_id == 4:
          if self.inSubnet(dst, 0):
            end_port = 13
            accept(13)
          if self.inSubnet(dst,1):
            if dst == '10.0.1.1':
              end_port = 12
              accept(12)
    elif tcp:
      dst_tcp = str(ipv4.dstip)
      if switch_id == 1:
        if self.inSubnet(dst_tcp, 0):
          if dst_tcp == '10.0.0.1':
            end_port = 1
            accept(1)
          elif dst_tcp == '10.0.0.2':
            end_port = 2
            accept(2)
        if self.inSubnet(dst_tcp, 2):
          end_port = 3
          accept(3)
      elif switch_id == 3:
        if self.inSubnet(dst_tcp, 2):
          if dst_tcp == '10.0.2.1':
            end_port = 5
            accept(5)
          elif dst_tcp == '10.0.2.2':
            end_port = 6
            accept(6)
        if self.inSubnet(dst_tcp, 0):
          end_port = 4
          accept(4)
    else:
      drop()
            

   

    pass

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_routing(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
