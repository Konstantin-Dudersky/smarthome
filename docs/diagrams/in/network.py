# from konstantin_docs.dia.nwdiag import (
#     Diagram,
#     Group,
#     Network,
#     Node,
#     PeerNetwork,
# )

# # nodes
# inet = Node("inet")
# terminal = Node(name="terminal")
# router = Node(name="router")
# pc = Node(name="PC")
# tv = Node(name="TV")
# rasp = Node(name="Raspberry")
# yeelight_bathroom = Node(name="light_batchroom")

# net = Network(address="192.168.100.x")
# net.add_node(terminal, ["192.168.100.1"])
# net.add_node(router, ["192.168.100.2"])

# net_eth = Network(address="192.168.101.x", name="Ethernet")
# net_eth.add_node(router, ["192.168.101.1"])
# net_eth.add_node(rasp, ["192.168.101.10"])
# net_eth.add_node(pc, ["192.168.101.12"])
# net_eth.add_node(tv, ["192.168.101.14"])

# net_wifi = Network(address="192.168.101.x", name="WiFi")
# net_wifi.add_node(router, ["192.168.101.1"])
# net_wifi.add_node(rasp, ["192.168.101.11"])
# net_wifi.add_node(pc, ["192.168.101.13"])
# net_wifi.add_node(tv, ["192.168.101.15"])
# net_wifi.add_node(yeelight_bathroom, ["192.168.101.20"])

# net_zigbee = Network(name="Zigbee")
# net_zigbee.add_node(rasp)

# dia = Diagram(
#     filename="network",
#     networks=[net, net_eth, net_wifi, net_zigbee],
#     peer_networks=[PeerNetwork(inet, terminal)],
# )
