"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""
from mininet.topo import Topo
class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        server1 = self.addHost( 'server1')
        server2 = self.addHost( 'server2')
        alexa = self.addHost( 'alexa')
        laptop = self.addHost( 'laptop')
        smartTV = self.addHost( 'smartTV')
        desktop1 = self.addHost( 'desktop1')
        desktop2 = self.addHost( 'desktop2')
        desktop3 = self.addHost( 'desktop3')
        switch1 = self.addSwitch( 's1')
        switch2 = self.addSwitch( 's2' )
        switch3 = self.addSwitch ( 's3' )
        switch4 = self.addSwitch( 's4' )

        # Add links
        self.addLink( server1, switch4)
        self.addLink( server2, switch4)
        self.addLink( switch4, switch2)
        self.addLink( switch2, switch1)
        self.addLink( alexa, switch1)
        self.addLink( laptop, switch1)
        self.addLink( smartTV, switch1)
        self.addLink( switch2, switch3)
        self.addLink(desktop1, switch3)
        self.addLink(desktop2, switch3)
        self.addLink(desktop3, switch3)
        self.addLink(server1, switch4)

        


topos = { 'mytopo': ( lambda: MyTopo() ) }
