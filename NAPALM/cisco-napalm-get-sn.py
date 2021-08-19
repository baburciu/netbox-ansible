#! /usr/bin/env python3

import napalm

device_list = [["R01-SPINE-1","X.X.X.11"],["R01-SPINE-2","X.X.X.12"],
               ["R01-LEAF-01","X.X.X.13"],["R01-LEAF-02","X.X.X.14"],
               ["R01-LEAF-03","X.X.X.15"],["R01-LEAF-04","X.X.X.16"]]

driver_ios = napalm.get_network_driver("nxos_ssh")
network_devices = []
for device in device_list:
    network_devices.append(
        driver_ios(
            hostname=device[1],
            username="admin",
            password="password"
        )
    )

for device in network_devices:
    print("Connecting to {} ...".format(device.hostname))
    device.open()

    print("Getting device facts to extract its SN")
    device_facts = device.get_facts()
    device_sn = device_facts['serial_number']
    device_hostname = device_facts['hostname']
    print("The SN of {} is: {}".format(device_hostname, device_sn))

    device.close()
    print("Done for {} .".format(device.hostname))
    
# Example of facts:
# {'uptime': 1919036, 'vendor': 'Cisco', 'os_version': '10.1(1)', 'serial_number': 'FDO25250EJN', 'model0 C93180YC-FX3 Chassis', 'hostname': 'R01-LEAF-01', 'fqdn': '', 'interface_list': ['Management0', 'EthEthernet1/2', 'Ethernet1/3', 'Ethernet1/4', 'Ethernet1/5', 'Ethernet1/6', 'Ethernet1/7', 'Ethernet1/8'/9', 'Ethernet1/10', 'Ethernet1/11', 'Ethernet1/12', 'Ethernet1/13', 'Ethernet1/14', 'Ethernet1/15', '', 'Ethernet1/17', 'Ethernet1/18', 'Ethernet1/19', 'Ethernet1/20', 'Ethernet1/21', 'Ethernet1/22', 'Et 'Ethernet1/24', 'Ethernet1/25', 'Ethernet1/26', 'Ethernet1/27', 'Ethernet1/28', 'Ethernet1/29', 'EtheEthernet1/31', 'Ethernet1/32', 'Ethernet1/33', 'Ethernet1/34', 'Ethernet1/35', 'Ethernet1/36', 'Ethernhernet1/38', 'Ethernet1/39', 'Ethernet1/40', 'Ethernet1/41', 'Ethernet1/42', 'Ethernet1/43', 'Ethernetrnet1/45', 'Ethernet1/46', 'Ethernet1/47', 'Ethernet1/48', 'Ethernet1/49', 'Ethernet1/50', 'Ethernet1/et1/52', 'Ethernet1/53', 'Ethernet1/54', 'Port-channel1', 'Port-channel2', 'Port-channel3', 'Port-chant-channel12', 'Port-channel13', 'Port-channel21', 'Port-channel22', 'Port-channel23', 'Port-channel51'nel53', 'Port-channel54', 'Port-channel55', 'Port-channel56', 'Port-channel57', 'Port-channel58', 'Por, 'Port-channel60', 'Port-channel81', 'Port-channel84', 'Vlan1', 'Vlan1001', 'Vlan1002', 'Vlan1003', 'Vlan1005', 'Vlan1006', 'Vlan1007', 'Vlan1008', 'Vlan1009']}
  
