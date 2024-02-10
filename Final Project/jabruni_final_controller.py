# Final Skeleton
#
# Hints/Reminders:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number over which
# the switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
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

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code:
    #   - port_on_switch represents the port on which the packet was received
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
   icmp = packet.find('icmp')
   ipv4 = packet.find('ipv4')
  
   def accept_flood():
     msg = of.ofp_flow_mod()
     msg.match = of.ofp_match.from_packet(packet)
     msg.idle_timeout = 30
     msg.hard_timeout = 30
     msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
     msg.buffer_id = packet_in.buffer_id
     self.connection.send(msg)

   def accept(end_port):
      msg =  of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 30
      msg.hard_timeout = 30
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
       if src == '160.114.50.20':
         drop()
       elif dst == '10.0.51.1':
         end_port = 10
         accept(10)
       else:
         end_port = 14
         accept(14)
     elif switch_id == 2:
       if src == '160.114.50.20':
         drop()
       elif dst == '10.0.52.2':
         end_port = 11
         accept(11)
       else:
         end_port = 15
         accept(15)
     elif switch_id == 3:
       if src == '160.114.50.20':
         drop()
       elif dst == '10.0.53.3':
         end_port = 12
         accept(12)
       else:
         end_port = 16
         accept(16)
     elif switch_id == 4:
       if src == '160.114.50.20':
         drop()
       if dst == '10.0.54.4':
         end_port = 13
         accept(13)
       else:
         end_port = 17
         accept(17)
     elif switch_id == 5:
       if dst == '160.114.50.20':
         end_port = 5
         accept(5)
       elif src == '160.114.50.20':
         drop()
       elif dst == '10.0.51.1':
         end_port = 6
         accept(6)
       elif dst == '10.0.52.2':
         end_port = 7
         accept(7)
       elif dst == '10.0.53.3':
         end_port = 8
         accept(8)
       elif dst == '10.0.54.4':
         end_port = 9
         accept(9)
       elif dst == '160.114.50.20':
         end_port = 5
         accept(5)
       else:
         end_port = 4
         accept(4)
     elif switch_id == 6:
       if src == '160.114.50.20':
         drop()
       elif dst == '10.0.55.5':
         end_port = 1
         accept(1)
       elif dst == '10.0.56.6':
         end_port = 2
         accept(2)
       else:
         end_port = 3
         accept(3)
   elif ipv4:
     dst_udp = str(ipv4.dstip)
     src_udp = str(ipv4.srcip)
     if switch_id == 1:
       if dst_udp == '10.0.51.1':
         end_port = 10
         accept(10)
       else:
         end_port = 14
         accept(14)
     elif switch_id == 2:
       if dst_udp == '10.0.52.2':
         end_port = 11
         accept(11)
       else:
         end_port = 15
         accept(15)
     elif switch_id == 3:
       if dst_udp == '10.0.53.3':
         end_port = 12
         accept(12)
       else:
         end_port = 16
         accept(16)
     elif switch_id == 4:
       if dst_udp == '10.0.54.4':
         end_port = 13
         accept(13)
       else:
         end_port = 17
         accept(17)
     elif switch_id == 5:
       if dst_udp == '160.114.50.20':
         end_port = 5
         accept(5)
       elif dst_udp == '10.0.51.1':
         end_port = 6
         accept(6)
       elif dst_udp == '10.0.52.2':
         end_port = 7
         accept(7)
       elif dst_udp == '10.0.53.3':
         end_port = 8
         accept(8)
       elif dst_udp == '10.0.54.4':
         end_port = 9
         accept(9)
       elif dst_udp == '160.114.50.20':
         end_port = 5
         accept(5)
       else:
         end_port = 4
         accept(4)
     elif switch_id == 6:
       if src_udp == '160.114.50.20':
         drop()
       elif dst_udp == '10.0.55.5':
         end_port = 1
         accept(1)
       elif dst_udp == '10.0.56.6':
         end_port = 2
         accept(2)
       else:
         end_port = 3
         accept(3)
   else:
     accept_flood()

      
    

    
       
         


   print "Hello, World!"

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
