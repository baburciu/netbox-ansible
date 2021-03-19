# Use NAPALM to get interfaces from Huawei OOB Mgmg switches and create NetBox objects based on that
# Creating NetBox interface by Ansible automation (playook called by python)
# Bogdan Adrian Burciu 04/03/2021 vers 1

# -------------------------
# Credits:
# https://codingnetworks.blog/napalm-network-automation-python-working-with-huawei-vrp/
# https://stackoverflow.com/questions/27590039/running-ansible-playbook-using-python-api

import xlrd
import napalm
import ansible_runner

sh = xlrd.open_workbook('/home/boburciu/netbox-ansible-automation/Feper_servers_4_NetBox_IaC.xls').sheet_by_index(0)
hostname = sh.col_values(0, start_rowx=2)       # hostname of device object already in NetBox
sym_name = sh.col_values(25, start_rowx=2)      # the hostname used in interface descriptions already set for Huawei switches

driver_vrp = napalm.get_network_driver("ce")
# device_list = [["SWH-OoB-R1","192.168.201.23"],["SWH-OoB-R2","192.168.201.27"],
#                ["SWH-TOR-R1","192.168.201.24"],["SWH-TOR-R2","192.168.201.25"]]

device_list = [["SWH-TOR-R1","192.168.201.24"],["SWH-TOR-R2","192.168.201.25"]]

network_devices = []
for device in device_list:
    network_devices.append(
        driver_vrp(
            hostname=device[1],
            username="orangeoln",
            password="l0c@l@dm1n"
        )
    )

for device in network_devices:
    print("Connecting to {} ...".format(device.hostname))
    device.open()

    print("Getting device interfaces")
    device_interfaces = device.get_interfaces()

    print("Getting device facts to extract its hostname")
    device_hostname = device.get_facts()['hostname']

    for int in device_interfaces.keys():
        if device_interfaces[int]['speed'] == 1000:
            int_type = "1000BASE-T"
            cable_type = "cat5e"
        elif device_interfaces[int]['speed'] == 10000:
            int_type = "10GBASE-T"
            cable_type = "mmf-om4"

        if "Eth-Trunk" in int:
            int_type = "LAG"

        if "MEth" in int:
            int_mgmt_flag = "True"
        else:
            int_mgmt_flag = "False"

        if "NULL" not in int and "Vlan" not in int:
            if device_hostname in sym_name:
                this_end_host = hostname[sym_name.index(device_hostname)]
                print(f"******* Now we'll create NetBox interface {int} for device {this_end_host}")
                r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                       playbook='create_interface.yml',
                                       inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                       extravars={'interface_device': this_end_host, 'interface_name': str(int),
                                                  'interface_mac_address': str(device_interfaces[int]['mac_address']),
                                                  'interface_enabled': str(device_interfaces[int]['is_enabled']),
                                                  'interface_type': int_type, 'interface_mtu': device_interfaces[int]['mtu'],
                                                  'interface_mgmt_only': int_mgmt_flag,
                                                  'interface_description': str(device_interfaces[int]['description']),
                                                  'external_vars': './external_vars.yml',
                                                  'ansible_python_interpreter':'/usr/bin/python3'})

            # for each interface collect the configuration by NAPALM and update trunking mode, VLAN and LAG for Huawei interface
            cmd = "display current-configuration interface " + str(int)
            intcfg = device.cli([cmd])[cmd]
            untagged_vlan_id=None
            tagged_vlan_list=[]
            # check if assigned to LAG and get it
            if "eth-trunk" in intcfg:
                lag_name = "Eth-Trunk" + intcfg.split(" eth-trunk ")[1].split("\n", 2)[0]
            # check the trunking mode (access, trunk) and get VLAN
            if "port default vlan" in intcfg:
                untagged_vlan_id = intcfg.split(" ort default vlan ")[1].split("\n", 2)[0]
                dot1q_mode = "Access"
            if "port trunk allow-pass vlan" in intcfg:
                intcfg_tagged_vlan_list = intcfg.split(" port trunk allow-pass vlan ")[1].split("\n", 2)[0]
                tagged_vlan_list = []
                dot1q_mode = "Tagged"
                if "to" in intcfg_tagged_vlan_list:
                    # add to the list of passed VLANs the ones prior to VLAN range (x y in "port trunk allow-pass vlan x y z to zz tt uu")
                    tagged_vlan_list = intcfg_tagged_vlan_list.split(" to ")[0].rsplit(" ")[0:-1]
                    # for the range, append the elements of it
                    tagged_vlan_list.extend( list( range( int(intcfg_tagged_vlan_list.split(" to ")[0].rsplit(" ")[-1]), int(intcfg_tagged_vlan_list.split(" to ")[1].rsplit(" ")[0])+1 ) ) )
                    # add to the list of passed VLANs the ones following the VLAN range (tt uu)
                    tagged_vlan_list.extend( intcfg_tagged_vlan_list.split(" to ")[1].rsplit(" ")[1:] )
                else:
                    tagged_vlan_list = intcfg.split(" port trunk allow-pass vlan ")[1].split("\n", 2)[0]
            # create the VLANs in NetBox
            if tagged_vlan_list.append(untagged_vlan_id):
                for vlan in tagged_vlan_list.append(untagged_vlan_id):
                    print(f"******* Now we'll create NetBox VLAN object for VID={vlan}")
                    r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                           playbook='create_vlan.yml',
                                           inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                           extravars={'vlan_id': vlan,
                                                      'external_vars': './external_vars.yml',
                                                      'ansible_python_interpreter': '/usr/bin/python3'})

            # check if the interface description collecting by NAPALM contains a known host in NetBox, if so configure its interface and cable them
            if "link_to" in device_interfaces[int]['description']:
                # other_end <=> list of ['Server_R2_04', 'mgmt'] from interface description (got via NAPALM driver) parsing
                other_end = str(device_interfaces[int]['description']).split('link_to_')[1].rsplit("_", 1)
                if other_end[0] in sym_name:
                    other_end_host = hostname[sym_name.index(other_end[0])]
                    if str(other_end[1]) == "mgmt":
                        int_mgmt_flag = "True"
                        if "88H" in other_end_host:
                            other_end_if = "iBMC"
                        elif "Dell" in other_end_host:
                            other_end_if = "iDRAC"
                    else:
                        other_end_if = other_end[1]
                        int_mgmt_flag = "False"

                    print(f"******* Now we'll create NetBox interface {other_end_if} for device {other_end_host}")
                    r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                           playbook='create_interface.yml',
                                           inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                           extravars={'interface_device': other_end_host, 'interface_name': other_end_if,
                                                      'interface_mac_address': 'FC:48:EF:00:00:00',
                                                      'interface_enabled': 'yes',
                                                      'interface_type': int_type, 'interface_mtu': device_interfaces[int]['mtu'],
                                                      'interface_mgmt_only': int_mgmt_flag,
                                                      'interface_description': str('to_'+device_hostname),
                                                      'external_vars': './external_vars.yml',
                                                      'ansible_python_interpreter': '/usr/bin/python3'})

                    print(f"******* Now we'll create NetBox cable between {other_end_host}'s {other_end_if} and {this_end_host}'s {int} ")
                    r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                           playbook='create_cable.yml',
                                           inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                           extravars={'cable_end_a_host': this_end_host, 'cable_end_a_if': int,
                                                      'cable_end_b_host': other_end_host, 'cable_end_b_if': other_end_if,
                                                      'cable_type': cable_type,
                                                      'external_vars': './external_vars.yml',
                                                      'ansible_python_interpreter': '/usr/bin/python3'})
    device.close()
    print("Done for {} .".format(device.hostname))

### How other_end is found:
#
# >>> if 'Server_R2_06' in sym_name:
# ...   sym_name.index('Server_R2_06')
# ...   hostname[sym_name.index('Server_R2_06')]
# ...
# 61
# '1288H_V5_2102311XDB10KA000168'
# >>>
# >>> 'link_to_Server_R2_04_mgmt'.split('link_to_')
# ['', 'Server_R2_04_mgmt']
# >>>
# >>> 'link_to_Server_R2_04_mgmt'.split('link_to_')[1]
# 'Server_R2_04_mgmt'
# >>>
# >>> 'link_to_Server_R2_04_mgmt'.split('link_to_')[1].rsplit("_", 1)
# ['Server_R2_04', 'mgmt']
# >>>

### How to collect interface configuration from Huawei VRP interface configuration:
# >>>
# >>> for int in device_interfaces.keys():
# ...   if "NULL" not in int and "Vlan" not in int:
# ...     cmd = "display current-configuration interface " + str(int)
# ...     intcfg = device.cli([cmd])[cmd]
# ...     print(intcfg)
# ...
# #
# interface 10GE1/0/1
#  description link_to_Server_R1_01_eth0
#  port link-type trunk
#  port trunk pvid vlan 100
#  undo port trunk allow-pass vlan 1
#  port trunk allow-pass vlan 100 202 to 206 300
#  device transceiver 10GBASE-COPPER
# #
# return
# #
# interface 10GE1/0/2
#  description link_to_Server_R1_01_eth2
#  port link-type trunk
#  undo port trunk allow-pass vlan 1
#  port trunk allow-pass vlan 100 202 to 206 300
#  device transceiver 10GBASE-COPPER
# #

### How the Eth-Trunk id is found from Huawei VRP interface configuration:
# >>> intcfg='#\ninterface 10GE2/0/42\n description Link_to_SWH-TOR-R2-2_10GE2/0/42\n eth-trunk 112\n device transceiver 10GBASE-FIBER\n#\nreturn'
# >>> intcfg.split("eth-trunk")[1].split("\n",2)[0][1:]
# '112'
# >>>