#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class Router(Node):
    """A Node with IP forwarding enabled """
    def config(self, **params):
        super(Router, self).config(**params)
        # Enable IP forwarding
        self.cmd('sysctl -w net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(Router, self).terminate()

class ThreeSubnetTopo(Topo):
    def build(self):
        # switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # router (single host with 3 interfaces)
        r0 = self.addHost('r0', ip='0.0.0.0')  # IPs set later per interface

        # hosts in subnet1 (connected to s1)
        h1 = self.addHost('h1', ip='10.0.1.1/24')
        h2 = self.addHost('h2', ip='10.0.1.2/24')

        # hosts in subnet2 (connected to s2)
        h3 = self.addHost('h3', ip='10.0.2.1/24')
        h4 = self.addHost('h4', ip='10.0.2.2/24')

        # hosts in subnet3 (connected to s3)
        h5 = self.addHost('h5', ip='10.0.3.1/24')
        h6 = self.addHost('h6', ip='10.0.3.2/24')

        # links host <-> switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)
        self.addLink(h6, s3)

        # router links to each switch (creates r0-eth0/eth1/eth2)
        self.addLink(r0, s1)  # r0-eth0 -> subnet1
        self.addLink(r0, s2)  # r0-eth1 -> subnet2
        self.addLink(r0, s3)  # r0-eth2 -> subnet3

def run_topology():
    setLogLevel('info')
    topo = ThreeSubnetTopo()
    net = Mininet(topo=topo, controller=RemoteController('c0', ip='127.0.0.1', port=6653),
                  link=TCLink, autoSetMacs=True)
    net.start()

    # configure router interfaces (r0-eth0/1/2)
    r0 = net.get('r0')
    r0.cmd('ifconfig r0-eth0 10.0.1.254/24')
    r0.cmd('ifconfig r0-eth1 10.0.2.254/24')
    r0.cmd('ifconfig r0-eth2 10.0.3.254/24')
    r0.cmd('sysctl -w net.ipv4.ip_forward=1')

    # ensure hosts use router as gateway
    net.get('h1').cmd('ifconfig h1-eth0 10.0.1.1/24; ip route add default via 10.0.1.254')
    net.get('h2').cmd('ifconfig h2-eth0 10.0.1.2/24; ip route add default via 10.0.1.254')

    net.get('h3').cmd('ifconfig h3-eth0 10.0.2.1/24; ip route add default via 10.0.2.254')
    net.get('h4').cmd('ifconfig h4-eth0 10.0.2.2/24; ip route add default via 10.0.2.254')

    net.get('h5').cmd('ifconfig h5-eth0 10.0.3.1/24; ip route add default via 10.0.3.254')
    net.get('h6').cmd('ifconfig h6-eth0 10.0.3.2/24; ip route add default via 10.0.3.254')

    print("Topology started. Hosts and router configured.")
    print("Subnets: 10.0.1.0/24 (h1,h2), 10.0.2.0/24 (h3,h4), 10.0.3.0/24 (h5,h6)")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run_topology()
