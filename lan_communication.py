from dhcppython import client as cl
class lan_communication:
    def __init__(self) -> None:
        self.dhcp=cl.DHCPClient()
        self.ip=0
    
    def setup_connection(self):
        self.dhcp.send_discover("FFFFFFFFFFFF", )
        