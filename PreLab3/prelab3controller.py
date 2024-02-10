# Lab 3 Skeleton
#
# Based on of_tutorial by James McCauley

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
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

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
    icmp = packet.find('icmp')
    arp = packet.find('arp')
    tcp = packet.find('tcp')
    udp = packet.find('udp')
    
    
    
    def accept():
      msg =  of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
      msg.buffer_id = packet_in.buffer_id
      self.connection.send(msg)

    def drop():
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.buffer_id = packet_in.buffer_id
      self.connection.send(msg)

    if icmp:
        accept()
    elif arp:
        accept()
    elif udp:
        accept()
    elif tcp:
          ipv4 = packet.find('ipv4')
          src = str(ipv4.srcip)
          dst = str(ipv4.dstip)
          if src == "10.0.0.1" and dst == "10.0.0.2":
            accept()
          elif src == "10.0.0.1" and dst == "10.0.0.6":
            accept()
          elif src == "10.0.0.2" and dst == "10.0.0.1":
            accept()
          elif src == "10.0.0.2" and dst == "10.0.0.3":
            accept()
          elif src == "10.0.0.2" and dst == "10.0.0.5":
            accept()
          elif src == "10.0.0.3" and dst == "10.0.0.2":
            accept()
          elif src == "10.0.0.3" and dst == "10.0.0.4":
            accept()
          elif src == "10.0.0.5" and dst == "10.0.0.2":
            accept()
          elif src == "10.0.0.6" and dst == "10.0.0.1":
            accept()
          elif src == "10.0.0.4" and dst == "10.0.0.3":
            accept()
    else:
        drop()

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
