# Use NAPALM to get interfaces from Huawei OOB Mgmg switches and create NetBox objects based on that
# Creating NetBox interface by Ansible automation (playook called by python)
# Bogdan Adrian Burciu 22/03/2021 vers 112

# -------------------------
# Credits:
# https://codingnetworks.blog/napalm-network-automation-python-working-with-huawei-vrp/
# https://stackoverflow.com/questions/27590039/running-ansible-playbook-using-python-api
# https://stackoverflow.com/questions/52201340/format-a-string-to-have-n-spaces-only-between-words-in-python/52201388

import xlrd
import napalm
import ansible_runner

sh = xlrd.open_workbook('/home/boburciu/netbox-ansible-automation/Feper_servers_4_NetBox_IaC.xls').sheet_by_index(0)
hostname = sh.col_values(0, start_rowx=2)       # hostname of device object already in NetBox
sym_name = sh.col_values(25, start_rowx=2)      # the hostname used in interface descriptions already set for Huawei switches

driver_vrp = napalm.get_network_driver("ce")
device_list = [["SWH-TOR-R2","192.168.201.25"],["SWH-OoB-R2","192.168.201.27"],
               ["SWH-TOR-R1","192.168.201.24"],["SWH-OoB-R1","192.168.201.23"]]
# device_list = [["SWH-TOR-R1","192.168.201.24"],["SWH-TOR-R2","192.168.201.25"]] # <= just for T-Shoot

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

    # create all the VLANs for a Huawei device in NetBox
    cmd = "display vlan summary"
    vlancfg = device.cli([cmd])[cmd]
    device_vlan_list = []
    vlancfg_vlan = (' ' * 1).join( vlancfg.split("Number of static VLAN:")[1].split("Number of dynamic VLAN:")[0].split("VLAN ID: ")[1].split() )
    vlancfg_vlan_list = vlancfg_vlan.rsplit(" to ",vlancfg_vlan.count(" to "))
    for j in range(len(vlancfg_vlan_list)-1):
        device_vlan_list.extend(vlancfg_vlan_list[j].split())
        device_vlan_list.extend( list( range( 1+int(vlancfg_vlan_list[j].split()[-1]), int(vlancfg_vlan_list[j+1].split()[0]) ) ) )

    device_vlan_list.extend(vlancfg_vlan_list[len(vlancfg_vlan_list)-1].split())
    for vlan in device_vlan_list:
        print(f"******* Now we'll create NetBox VLAN object for VID={vlan}")
        r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                               playbook='create_vlan.yml',
                               inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                               extravars={'vlan_id': vlan, 'vlan_site': "Feper-Bucharest",
                                          'external_vars': './external_vars.yml',
                                          'ansible_python_interpreter': '/usr/bin/python3'})
    # open again Napalm connection, in case it timesout while creating VLAN objects in NetBox
    device.open()

    for iface in device_interfaces.keys():
        if device_interfaces[iface]['speed'] == 1000:
            int_type = "1000BASE-T"
            cable_type = "cat5e"
        elif device_interfaces[iface]['speed'] == 10000:
            int_type = "10GBASE-T"
            cable_type = "mmf-om4"

        if "Eth-Trunk" in iface:
            int_type = "LAG"

        if "MEth" in iface:
            int_mgmt_flag = "True"
        else:
            int_mgmt_flag = "False"

        if "NULL" not in iface and "Vlan" not in iface:
            if device_hostname in sym_name:
                this_end_host = hostname[sym_name.index(device_hostname)]
                # NetBox: create the interface
                print(f"******* Now we'll create NetBox interface {iface} for device {this_end_host}")
                r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                       playbook='create_interface.yml',
                                       inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                       extravars={'interface_device': this_end_host, 'interface_name': str(int),
                                                  'interface_mac_address': str(device_interfaces[iface]['mac_address']),
                                                  'interface_enabled': str(device_interfaces[iface]['is_enabled']),
                                                  'interface_type': int_type, 'interface_mtu': device_interfaces[iface]['mtu'],
                                                  'interface_mgmt_only': int_mgmt_flag,
                                                  'interface_description': str(device_interfaces[iface]['description']),
                                                  'external_vars': './external_vars.yml',
                                                  'ansible_python_interpreter':'/usr/bin/python3'})

            # for each interface collect the configuration by NAPALM and update trunking mode, VLAN and LAG for Huawei interface
            cmd = "display current-configuration interface " + str(iface)
            ifcfg = device.cli([cmd])[cmd]
            untagged_vlan_id=None
            tagged_vlan_list=[]

            # check if assigned to LAG and get it, then update interface in NetBox
            if "eth-trunk" in ifcfg:
                lag_name = "Eth-Trunk" + ifcfg.split(" eth-trunk ")[1].split("\n", 2)[0]

                # NetBox: first create the LAG interface, to exclude erros with LAG not found, even though it will overwritten later
                # by the main loop over interfaces returned by NAPALM
                print(f"******* Now we'll create NetBox interface {lag_name} for device {this_end_host}")
                r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                       playbook='create_interface.yml',
                                       inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                       extravars={'interface_device': this_end_host, 'interface_name': str(lag_name),
                                                  'interface_type': 'LAG',
                                                  'external_vars': './external_vars.yml',
                                                  'ansible_python_interpreter':'/usr/bin/python3'})
                # NetBox: now assign interface to LAG
                print(f"******* Now we'll assign NetBox interface {iface} for device {this_end_host} to the LAG {lag_name}")
                r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                       playbook='update_interface.yml',
                                       inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                       extravars={'interface_device': this_end_host, 'interface_name': str(int),
                                                  'lag_name': lag_name,
                                                  'external_vars': './external_vars.yml',
                                                  'ansible_python_interpreter':'/usr/bin/python3'})

            # check the trunking mode (access, trunk) and get VLAN
            # and ensure cmd is not with "undo"
            # then update interface in NetBox with trunking mode and VLAN
            if "undo port default vlan" in ifcfg:
                ifcfg = ifcfg.replace("undo port default vlan", "dummy text")

            if "undo port trunk allow-pass vlan" in ifcfg:
                ifcfg = ifcfg.replace("undo port trunk allow-pass vlan", "dummy text")

            if "port default vlan" in ifcfg:
                untagged_vlan_id = ifcfg.split(" port default vlan ")[1].split("\n", 2)[0]
                dot1q_mode = "Access"
                # NetBox: update the interface found in access mode
                print(f"******* Now we'll update NetBox interface {str(int)} as access port in VLAN {untagged_vlan_id}")
                r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                       playbook='update_interface.yml',
                                       inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                       extravars={'interface_device': this_end_host, 'interface_name': str(int),
                                                  'dot1q_mode': dot1q_mode,
                                                  'untagged_vlan_id': untagged_vlan_id,
                                                  'external_vars': './external_vars.yml',
                                                  'ansible_python_interpreter':'/usr/bin/python3'})

            if "port trunk allow-pass vlan" in ifcfg:
                ifcfg_tagged_vlan_list = ifcfg.split(" port trunk allow-pass vlan ")[1].split("\n", 2)[0]
                dot1q_mode = "Tagged"
                if "to" in ifcfg_tagged_vlan_list:
                    # add to the list of passed VLANs the ones prior to VLAN range (x y in "port trunk allow-pass vlan x y z to zz tt uu")
                    tagged_vlan_list.extend(ifcfg_tagged_vlan_list.split(" to ")[0].rsplit(" ")[0:-1])
                    # for the range, append the elements of it
                    tagged_vlan_list.extend( list( range( int(ifcfg_tagged_vlan_list.split(" to ")[0].rsplit(" ")[-1]),
                                                          int(ifcfg_tagged_vlan_list.split(" to ")[1].rsplit(" ")[0]) + 1 ) ) )
                    # add to the list of passed VLANs the ones following the VLAN range (tt uu)
                    tagged_vlan_list.extend(ifcfg_tagged_vlan_list.split(" to ")[1].rsplit(" ")[1:])
                else:
                    tagged_vlan_list = (ifcfg.split(" port trunk allow-pass vlan ")[1].split("\n", 2)[0] ).split(" ")

                for tagged_vlan_id in tagged_vlan_list:
                    # NetBox: update the interface found in trunk mode
                    print(f"******* Now we'll update NetBox interface {str(int)} as trunk port which passes VLAN {str(tagged_vlan_id)}")
                    r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                           playbook='update_interface.yml',
                                           inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                           extravars={'interface_device': this_end_host, 'interface_name': str(int),
                                                      'dot1q_mode': dot1q_mode,
                                                      'tagged_vlan_id': str(tagged_vlan_id),
                                                      'external_vars': './external_vars.yml',
                                                      'ansible_python_interpreter':'/usr/bin/python3'})


            # check if the interface description collecting by NAPALM contains a known host in NetBox, if so configure its interface and cable them
            if "link_to" in device_interfaces[iface]['description']:
                # other_end <=> list of ['Server_R2_04', 'mgmt'] from interface description (got via NAPALM driver) parsing
                other_end = str(device_interfaces[iface]['description']).split('link_to_')[1].rsplit("_", 1)
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
                                                      'interface_type': int_type, 'interface_mtu': device_interfaces[iface]['mtu'],
                                                      'interface_mgmt_only': int_mgmt_flag,
                                                      'interface_description': str('to_'+device_hostname),
                                                      'external_vars': './external_vars.yml',
                                                      'ansible_python_interpreter': '/usr/bin/python3'})

                    print(f"******* Now we'll create NetBox cable between {other_end_host}'s {other_end_if} and {this_end_host}'s {iface} ")
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
# >>> for iface in device_interfaces.keys():
# ...   if "NULL" not in iface and "Vlan" not in iface:
# ...     cmd = "display current-configuration interface " + str(int)
# ...     ifcfg = device.cli([cmd])[cmd]
# ...     print(ifcfg)
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
# >>> ifcfg='#\ninterface 10GE2/0/42\n description Link_to_SWH-TOR-R2-2_10GE2/0/42\n eth-trunk 112\n device transceiver 10GBASE-FIBER\n#\nreturn'
# >>> ifcfg.split("eth-trunk")[1].split("\n",2)[0][1:]
# '112'
# >>>

### How to get the list of VLANs from the "display vlan summary" output in Huawei VRP:
# >>> device_vlan_list=[]
# >>> device.open()
# >>> cmd = "display vlan summary"
# >>> vlancfg = device.cli([cmd])[cmd]
# >>> device_vlan_list=[]
# >>> vlancfg_vlan = (' ' * 1).join( vlancfg.split("Number of static VLAN:")[1].split("Number of dynamic VLAN:")[0].split("VLAN ID: ")[1].split() )
# >>> vlancfg_vlan
# '1 5 to 8 100 110 202 to 206 212 to 216 222 300 310 400 to 405 410 to 416 480 490 501 504 to 505 555 1000 1010 to 1011 1038 1100 1202 to 1205 1300 1400 to 1405 2000 2005 to 2030 3000 4001'
# >>> vlancfg_vlan_list = vlancfg_vlan.rsplit(" to ",vlancfg_vlan.count(" to "))
# >>> vlancfg_vlan_list
# ['1 5', '8 100 110 202', '206 212', '216 222 300 310 400', '405 410', '416 480 490 501 504', '505 555 1000 1010', '1011 1038 1100 1202', '1205 1300 1400', '1405 2000 2005', '2030 3000 4001']
#
# >>> for j in range(len(vlancfg_vlan_list)-1):
# ...    device_vlan_list.extend(vlancfg_vlan_list[j].split())
# ...    device_vlan_list.extend( list( range( 1+int(vlancfg_vlan_list[j].split()[-1]), int(vlancfg_vlan_list[j+1].split()[0]) ) ) )
# ...
# >>> device_vlan_list
# ['1', '5', 6, 7, '8', '100', '110', '202', 203, 204, 205, '206', '212', 213, 214, 215, '216', '222', '300', '310', '400', 401, 402, 403, 404, '405', '410', 411, 412, 413, 414, 415, '416', '480', '490', '501', '504', '505', '555', '1000', '1010', '1011', '1038', '1100', '1202', 1203, 1204, '1205', '1300', '1400', 1401, 1402, 1403, 1404, '1405', '2000', '2005', 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029]
# >>> device_vlan_list.extend(vlancfg_vlan_list[len(vlancfg_vlan_list)-1].split())
# >>> device_vlan_list
# ['1', '5', 6, 7, '8', '100', '110', '202', 203, 204, 205, '206', '212', 213, 214, 215, '216', '222', '300', '310', '400', 401, 402, 403, 404, '405', '410', 411, 412, 413, 414, 415, '416', '480', '490', '501', '504', '505', '555', '1000', '1010', '1011', '1038', '1100', '1202', 1203, 1204, '1205', '1300', '1400', 1401, 1402, 1403, 1404, '1405', '2000', '2005', 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, '2030', '3000', '4001']
# >>>

