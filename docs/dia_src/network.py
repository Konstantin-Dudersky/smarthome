from konstantin_docs.dia.nwdiag import (
    Diagram,
    Group,
    Network,
    Node,
    PeerNetwork,
) 

# nodes
inet = Node("inet")
terminal = Node(name="terminal")
router = Node(name="router")
pc = Node(name="PC")
tv = Node(name="TV")
rasp = Node(name="Raspberry")


net1 = Network(address="192.168.100.x")
net1.add_node(terminal, ["192.168.100.1"])
net1.add_node(router, ["192.168.100.2"])

net2 = Network(address="192.168.101.x")
net2.add_node(router, ["192.168.101.1"])
net2.add_node(rasp, ["192.168.101.10", "192.168.101.11"])
net2.add_node(pc, ["192.168.101.11", "192.168.101.13"])
net2.add_node(tv, ["192.168.101.14", "192.168.101.15"])

dia = Diagram(
    filename='network',
    networks=[net1, net2],
    peer_networks=[PeerNetwork(inet, terminal)]
)
