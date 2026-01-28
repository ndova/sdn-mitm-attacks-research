#!/usr/bin/python3

from mininet.topo import Topo
from mininet.node import Node

class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        # Disable forwarding when the router is terminated
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class LabTopology(Topo):
    """A topology with a central router connecting three subnets."""

    def build(self, **_opts):
        # Define gateway IPs for each subnet
        gw1 = '10.0.1.254'
        gw2 = '10.0.2.254'
        gw3 = '10.0.3.254'

        # Add the central router
        router = self.addNode('r0', cls=LinuxRouter, ip=f'{gw1}/24')

        # Add switches for each subnet
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Link switches to the router and configure the router's interfaces
        self.addLink(s1, router, intfName2='r0-eth1', params2={'ip': f'{gw1}/24'})
        self.addLink(s2, router, intfName2='r0-eth2', params2={'ip': f'{gw2}/24'})
        self.addLink(s3, router, intfName2='r0-eth3', params2={'ip': f'{gw3}/24'})

        # Add hosts to Subnet 1 and set their default route
        h1 = self.addHost('h1', ip='10.0.1.1/24', defaultRoute=f'via {gw1}')
        h2 = self.addHost('h2', ip='10.0.1.2/24', defaultRoute=f'via {gw1}')

        # Add hosts to Subnet 2 and set their default route
        h3 = self.addHost('h3', ip='10.0.2.1/24', defaultRoute=f'via {gw2}')
        h4 = self.addHost('h4', ip='10.0.2.2/24', defaultRoute=f'via {gw2}')

        # Add hosts to Subnet 3 and set their default route
        h5 = self.addHost('h5', ip='10.0.3.1/24', defaultRoute=f'via {gw3}')
        h6 = self.addHost('h6', ip='10.0.3.2/24', defaultRoute=f'via {gw3}')

        # Link hosts to their respective switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)
        self.addLink(h6, s3)
        
        # Add direct inter-switch links for L2 discovery by the controller
        self.addLink(s1, s2)
        self.addLink(s2, s3)

# Expose the topology to the 'mn' command
topos = {'labtopo': (lambda: LabTopology())}
