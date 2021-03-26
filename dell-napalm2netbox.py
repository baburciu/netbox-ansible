# Use NAPALM to get interfaces from Dell EMC Networking OS10 switches and create NetBox objects based on that
# Creating NetBox VLAN, interface and cable by Ansible automation (playook called by python with ansible_runner)
# Bogdan Adrian Burciu 26/03/2021

# -------------------------
# Credits:
# https://codingnetworks.blog/napalm-network-automation-python-working-with-huawei-vrp/
# https://stackoverflow.com/questions/27590039/running-ansible-playbook-using-python-api
# https://stackoverflow.com/questions/52201340/format-a-string-to-have-n-spaces-only-between-words-in-python/52201388

import xlrd
import napalm
import ansible_runner

sh = xlrd.open_workbook('/home/ubuntu/NEO_Alpha_IaC/NEO_servers_4_NetBox_IaC.xls').sheet_by_index(0)
hostname = sh.col_values(0, start_rowx=1)       # hostname of device object already in NetBox
sym_name = sh.col_values(18, start_rowx=1)      # the hostname used in interface descriptions already set for switches and SW hostname returned by NAPALM

driver_dellos = napalm.get_network_driver("dellos10")
device_list = [["SW-WE19-TOR1-B4-NEO","192.168.70.4"],["SW-WE19-TOR2-B4-NEO","192.168.70.3"]]

network_devices = []
for device in device_list:
    network_devices.append(
        driver_dellos(
            hostname=device[1],
            username="admin",
            password="admin"
        )
    )

# the MAC addresses for the 25G NICs of the PowerEdge servers, collected oob by Ansible
dell_server_25g_nics={
"Dell_Compute-1": {
            "NIC1-P1": "40:A6:B7:43:A1:90",
            "NIC1-P2": "40:A6:B7:43:A1:91",
            "NIC2-P1": "40:A6:B7:43:A9:20",
            "NIC2-P2": "40:A6:B7:43:A9:21",
            "NIC3-P1": "40:A6:B7:43:A7:D0",
            "NIC3-P2": "40:A6:B7:43:A7:D1"
        },
"Dell_Compute-2": {
            "NIC1-P1": "40:A6:B7:43:AA:80",
            "NIC1-P2": "40:A6:B7:43:AA:81",
            "NIC2-P1": "40:A6:B7:43:AA:60",
            "NIC2-P2": "40:A6:B7:43:AA:61",
            "NIC3-P1": "40:A6:B7:43:A9:A0",
            "NIC3-P2": "40:A6:B7:43:A9:A1"
        },
"Dell_Compute-3": {
            "NIC1-P1": "40:A6:B7:43:B8:80",
            "NIC1-P2": "40:A6:B7:43:B8:81",
            "NIC2-P1": "40:A6:B7:43:BD:00",
            "NIC2-P2": "40:A6:B7:43:BD:01",
            "NIC3-P1": "40:A6:B7:43:94:10",
            "NIC3-P2": "40:A6:B7:43:94:11"
        },
"Dell_Compute-4": {
            "NIC1-P1": "40:A6:B7:43:92:D0",
            "NIC1-P2": "40:A6:B7:43:92:D1",
            "NIC2-P1": "40:A6:B7:43:3B:A0",
            "NIC2-P2": "40:A6:B7:43:3B:A1",
            "NIC3-P1": "40:A6:B7:43:A1:40",
            "NIC3-P2": "40:A6:B7:43:A1:41"
        },
"Dell_Compute-5": {
            "NIC1-P1": "40:A6:B7:44:AA:70",
            "NIC1-P2": "40:A6:B7:44:AA:71",
            "NIC2-P1": "40:A6:B7:43:92:30",
            "NIC2-P2": "40:A6:B7:43:92:31",
            "NIC3-P1": "40:A6:B7:44:A5:D0",
            "NIC3-P2": "40:A6:B7:44:A5:D1"
        },
"Dell_Compute-6": {
            "NIC1-P1": "40:A6:B7:44:9F:80",
            "NIC1-P2": "40:A6:B7:44:9F:81",
            "NIC2-P1": "40:A6:B7:44:9E:B0",
            "NIC2-P2": "40:A6:B7:44:9E:B1",
            "NIC3-P1": "40:A6:B7:44:BA:B0",
            "NIC3-P2": "40:A6:B7:44:BA:B1"
        },
"Dell_Compute-7": {
            "NIC1-P1": "40:A6:B7:43:93:80",
            "NIC1-P2": "40:A6:B7:43:93:81",
            "NIC2-P1": "40:A6:B7:43:A0:10",
            "NIC2-P2": "40:A6:B7:43:A0:11",
            "NIC3-P1": "40:A6:B7:43:92:40",
            "NIC3-P2": "40:A6:B7:43:92:41"
        },
"Dell_Compute-8": {
            "NIC1-P1": "40:A6:B7:43:92:E0",
            "NIC1-P2": "40:A6:B7:43:92:E1",
            "NIC2-P1": "40:A6:B7:45:5F:B0",
            "NIC2-P2": "40:A6:B7:45:5F:B1",
            "NIC3-P1": "40:A6:B7:43:A1:30",
            "NIC3-P2": "40:A6:B7:43:A1:31"
        },
"Dell_Compute-9": {
            "NIC1-P1": "40:A6:B7:43:A7:C0",
            "NIC1-P2": "40:A6:B7:43:A7:C1",
            "NIC2-P1": "40:A6:B7:43:A7:20",
            "NIC2-P2": "40:A6:B7:43:A7:21",
            "NIC3-P1": "40:A6:B7:43:A0:E0",
            "NIC3-P2": "40:A6:B7:43:A0:E1"
        },
"Dell_Compute-10": {
            "NIC1-P1": "40:A6:B7:43:A7:10",
            "NIC1-P2": "40:A6:B7:43:A7:11",
            "NIC2-P1": "40:A6:B7:43:A8:50",
            "NIC2-P2": "40:A6:B7:43:A8:51",
            "NIC3-P1": "40:A6:B7:45:53:70",
            "NIC3-P2": "40:A6:B7:45:53:71"
        },
"Dell_Compute-11": {
            "NIC1-P1": "40:A6:B7:45:5F:F0",
            "NIC1-P2": "40:A6:B7:45:5F:F1",
            "NIC2-P1": "40:A6:B7:45:5E:90",
            "NIC2-P2": "40:A6:B7:45:5E:91",
            "NIC3-P1": "40:A6:B7:45:61:40",
            "NIC3-P2": "40:A6:B7:45:61:41"
        },
"Dell_Compute-12": {
            "NIC1-P1": "40:A6:B7:43:BB:F0",
            "NIC1-P2": "40:A6:B7:43:BB:F1",
            "NIC2-P1": "40:A6:B7:43:AB:70",
            "NIC2-P2": "40:A6:B7:43:AB:71",
            "NIC3-P1": "40:A6:B7:43:AA:30",
            "NIC3-P2": "40:A6:B7:43:AA:31"
        },
"Dell_Compute-13": {
            "NIC1-P1": "40:A6:B7:43:AA:40",
            "NIC1-P2": "40:A6:B7:43:AA:41",
            "NIC2-P1": "40:A6:B7:43:BC:00",
            "NIC2-P2": "40:A6:B7:43:BC:01",
            "NIC3-P1": "40:A6:B7:45:56:50",
            "NIC3-P2": "40:A6:B7:45:56:51"
        },
"Dell_Ceph-1": {
            "NIC1-P1": "40:A6:B7:3E:83:E0",
            "NIC1-P2": "40:A6:B7:3E:83:E1",
            "NIC2-P1": "40:A6:B7:3D:C9:B0",
            "NIC2-P2": "40:A6:B7:3D:C9:B1"
        },
"Dell_Ceph-2": {
            "NIC1-P1": "40:A6:B7:3E:B1:90",
            "NIC1-P2": "40:A6:B7:3E:B1:91",
            "NIC2-P1": "40:A6:B7:3E:94:40",
            "NIC2-P2": "40:A6:B7:3E:94:41"
        },
"Dell_Ceph-3": {
            "NIC1-P1": "40:A6:B7:3D:D9:A0",
            "NIC1-P2": "40:A6:B7:3D:D9:A1",
            "NIC2-P1": "40:A6:B7:3D:C7:20",
            "NIC2-P2": "40:A6:B7:3D:C7:21"
        },
"Dell_Control-1": {
            "NIC1-P1": "40:A6:B7:45:55:50",
            "NIC1-P2": "40:A6:B7:45:55:51",
            "NIC2-P1": "40:A6:B7:45:42:00",
            "NIC2-P2": "40:A6:B7:45:42:01"
        },
"Dell_Control-2": {
            "NIC1-P1": "40:A6:B7:43:8F:70",
            "NIC1-P2": "40:A6:B7:43:8F:71",
            "NIC2-P1": "40:A6:B7:43:AC:E0",
            "NIC2-P2": "40:A6:B7:43:AC:E1"
        },
"Dell_Control-3": {
            "NIC1-P1": "40:A6:B7:43:8F:80",
            "NIC1-P2": "40:A6:B7:43:8F:81",
            "NIC2-P1": "40:A6:B7:43:AC:B0",
            "NIC2-P2": "40:A6:B7:43:AC:B1"
        }
}

# for each Dell switch device, open a NAPALM session and parse returned output
for device in network_devices:
    print("Connecting to {} ...".format(device.hostname))
    device.open()

    print("Getting device interfaces")
    device_interfaces = device.get_interfaces()

    print("Getting device facts to extract its hostname")
    device_hostname = device.get_facts()['hostname']

    # create all the VLANs for a Huawei device in NetBox
    # first fetch the cmd output and parse it to a list
    cmd = "show running-configuration | grep vlan | grep interface"
    vlancfg = device.cli([cmd])[cmd]
    device_vlan_list = []
    device_vlan_list = vlancfg.replace("interface vlan", "").split('\n')

    for vlan in device_vlan_list:
        print(f"******* Now we'll create NetBox VLAN object for VID={vlan}, based on device {device_hostname}'s VLAN list")
        r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                               playbook='create_vlan.yml',
                               inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                               extravars={'vlan_id': vlan, 'vlan_site': "Lannion-TGI-Labs",
                                          'external_vars': './external_vars.yml',
                                          'ansible_python_interpreter': '/usr/bin/python3'})
    # open again Napalm connection, in case it timesout while creating VLAN objects in NetBox
    # device.open()

    for iface in device_interfaces.keys():
        if device_interfaces[iface]['speed'] == 25000000000:
            int_type = "SFP28"
            cable_type = "mmf-om4"
        elif device_interfaces[iface]['speed'] == 100000000000:
            int_type = "QSFP28"
            cable_type = "smf-os2"
        elif device_interfaces[iface]['speed'] == 200000000000:
            int_type = "QSFP56"
            cable_type = "aoc" # Active Optical Cabling

        # check if interface name is Po, mgmt, null or vlan
        if "port-channel" in iface:
            int_type = "LAG"

        if "mgmt1/1" in iface:
            int_mgmt_flag = "True"
        else:
            int_mgmt_flag = "False"

        # only for non-mgmt phy interaces:
        if "null" not in iface and "vlan" not in iface:
            if device_hostname in sym_name:
                this_end_host = hostname[sym_name.index(device_hostname)]
                # NetBox: create the interface
                print(f"******* Now we'll create NetBox interface {iface} for device {this_end_host}")
                r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                       playbook='create_interface.yml',
                                       inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                       extravars={'interface_device': this_end_host, 'interface_name': str(iface),
                                                  'interface_mac_address': str(device_interfaces[iface]['mac_address']),
                                                  'interface_enabled': str(device_interfaces[iface]['is_enabled']),
                                                  'interface_type': int_type, 'interface_mtu': device_interfaces[iface]['mtu'],
                                                  'interface_mgmt_only': int_mgmt_flag,
                                                  'interface_description': str(device_interfaces[iface]['description']),
                                                  'external_vars': './external_vars.yml',
                                                  'ansible_python_interpreter':'/usr/bin/python3'})

            # for each interface collect the configuration by NAPALM and update trunking mode, VLAN and LAG for Dell SW interface
            cmd = "show running-configuration interface " + str(iface)
            ifcfg = device.cli([cmd])[cmd]
            untagged_vlan_id=None
            tagged_vlan_list=[]

            # check if assigned to LAG and get it, then update interface in NetBox
            if "channel-group" in ifcfg:
                lag_name = "port-channel" + ifcfg.split(" channel-group ")[1].split("\n", 2)[0].split(" mode ")[0]

                # NetBox: first create the LAG interface, to exclude erros with LAG not found, even though it will overwritten later
                # by the main loop over interfaces returned by NAPALM
                print(f"******* Now we'll create NetBox interface {lag_name} for device {this_end_host}")
                r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                       playbook='create_interface.yml',
                                       inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                       extravars={'interface_device': this_end_host, 'interface_name': str(lag_name),
                                                  'interface_type': 'LAG',
                                                  'external_vars': './external_vars.yml',
                                                  'ansible_python_interpreter':'/usr/bin/python3'})
                # NetBox: now assign interface to LAG
                print(f"******* Now we'll assign NetBox interface {iface} for device {this_end_host} to the LAG {lag_name}")
                r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                       playbook='update_interface.yml',
                                       inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                       extravars={'interface_device': this_end_host, 'interface_name': str(iface),
                                                  'lag_name': lag_name,
                                                  'external_vars': './external_vars.yml',
                                                  'ansible_python_interpreter':'/usr/bin/python3'})

            # check the trunking mode (access, trunk) and get VLAN
            # and ensure cmd is not with "no"
            # then update interface in NetBox with trunking mode and VLAN
            if "no switchport access vlan" in ifcfg:
                ifcfg = ifcfg.replace("no switchport access vlan", "dummy text")

            if "no switchport trunk allowed vlan" in ifcfg:
                ifcfg = ifcfg.replace("no switchport trunk allowed vlan", "dummy text")

            if "switchport mode access" in ifcfg:
                untagged_vlan_id = ifcfg.split(" switchport access vlan ")[1].split("\n", 2)[0]
                dot1q_mode = "Access"
                # NetBox: update the interface found in access mode
                print(f"******* Now we'll update NetBox interface {str(iface)} as access port in VLAN {untagged_vlan_id}")
                r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                       playbook='update_interface.yml',
                                       inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                       extravars={'interface_device': this_end_host, 'interface_name': str(iface),
                                                  'dot1q_mode': dot1q_mode,
                                                  'untagged_vlan_id': untagged_vlan_id,
                                                  'external_vars': './external_vars.yml',
                                                  'ansible_python_interpreter':'/usr/bin/python3'})

            if "switchport mode trunk" in ifcfg:
                ifcfg_tagged_vlan_list = ifcfg.split(" switchport trunk allowed vlan ")[1].split("\n", 2)[0].split(",")
                dot1q_mode = "Tagged"
                for ifcfg_tagged_vlan_range in ifcfg_tagged_vlan_list:
                    if "-" in ifcfg_tagged_vlan_range:
                        tagged_vlan_list.extend( list( range( int(ifcfg_tagged_vlan_range.split("-")[0]), int(ifcfg_tagged_vlan_range.split("-")[1]) + 1 ) ) )
                    else:
                        tagged_vlan_list.extend( ifcfg_tagged_vlan_range )

                for tagged_vlan_id in tagged_vlan_list:
                    # NetBox: update the interface found in trunk mode
                    print(f"******* Now we'll update NetBox interface {str(iface)} as trunk port which passes VLAN {str(tagged_vlan_id)}")
                    r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                           playbook='update_interface.yml',
                                           inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                           extravars={'interface_device': this_end_host, 'interface_name': str(iface),
                                                      'dot1q_mode': dot1q_mode,
                                                      'tagged_vlan_id': str(tagged_vlan_id),
                                                      'external_vars': './external_vars.yml',
                                                      'ansible_python_interpreter':'/usr/bin/python3'})

            # check if the interface description collecting by NAPALM contains a known host in NetBox, if so configure its interface and cable them
            if "Dell" in device_interfaces[iface]['description']:
                # other_end <=> list of ['Dell_Compute-4', 'NIC1-P1--MAVENIR', 'USE'] from interface description (got via NAPALM driver) parsing
                other_end = descr.rsplit("_", descr.count("_")-1 )
                if other_end[0] in sym_name:
                    other_end_host = hostname[sym_name.index(other_end[0])]
                    other_end_if = other_end[1][0:7]

                    print(f"******* Now we'll create NetBox interface {other_end_if} for device {other_end_host}")
                    r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                           playbook='create_interface.yml',
                                           inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                           extravars={'interface_device': other_end_host, 'interface_name': other_end_if,
                                                      'interface_mac_address': dell_server_25g_nics[other_end_host][other_end_if],
                                                      'interface_enabled': 'yes',
                                                      'interface_type': int_type, 'interface_mtu': device_interfaces[iface]['mtu'],
                                                      'interface_mgmt_only': "False",
                                                      'interface_description': str(this_end_host+'_'+iface),
                                                      'external_vars': './external_vars.yml',
                                                      'ansible_python_interpreter': '/usr/bin/python3'})

                    print(f"******* Now we'll create NetBox cable between {other_end_host}'s {other_end_if} and {this_end_host}'s {iface} ")
                    r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                           playbook='create_cable.yml',
                                           inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                           extravars={'cable_end_a_host': this_end_host, 'cable_end_a_if': iface,
                                                      'cable_end_b_host': other_end_host, 'cable_end_b_if': other_end_if,
                                                      'cable_type': cable_type,
                                                      'external_vars': './external_vars.yml',
                                                      'ansible_python_interpreter': '/usr/bin/python3'})

    device.close()
    print("Done for {} .".format(device.hostname))

### How other_end is found from description:
# >>> descr = "Dell_Compute-4_NIC1-P1--MAVENIR_USE"
# >>> descr.rsplit("_", descr.count("_")-1)
# ['Dell_Compute-4', 'NIC1-P1--MAVENIR', 'USE']
# >>>
# >>> other_end_if=descr.rsplit("_", descr.count("_")-1 )[1][0:7]
# >>> other_end_if
# 'NIC1-P1'
# >>>


### How the vlan list of Trunk interface is found from Dell OS10 interface configuration:
# >>> cmd = "show running-configuration interface port-channel1"
# >>> ifcfg = device.cli([cmd])[cmd]
# >>> ifcfg
# '!\ninterface port-channel1\n description Dell_Control-3_Bond_0\n no shutdown\n switchport mode trunk\n switchport access vlan 1\n switchport trunk allowed vlan 270-276,701-708,1021-1026,1028-1032\n mtu 9216\n lacp fallback enable\n lacp fallback timeout 0\n vlt-port-channel 1\n spanning-tree port type edge'
# >>>
# >>> ifcfg.split(" switchport trunk allowed vlan ")[1].split("\n", 2)[0]
# '270-276,701-708,1021-1026,1028-1032'
# >>> ifcfg_tagged_vlan_list = ifcfg.split(" switchport trunk allowed vlan ")[1].split("\n", 2)[0].split(",")
# >>> ifcfg_tagged_vlan_list
# ['270-276', '701-708', '1021-1026', '1028-1032']
# >>>
# >>> for ifcfg_tagged_vlan_range in ifcfg_tagged_vlan_list:
# ...   if "-" in ifcfg_tagged_vlan_range:
# ...     print(list( range( int(ifcfg_tagged_vlan_range.split("-")[0]), int(ifcfg_tagged_vlan_range.split("-")[1]) + 1 ) ) )
# ...
# [270, 271, 272, 273, 274, 275, 276]
# [701, 702, 703, 704, 705, 706, 707, 708]
# [1021, 1022, 1023, 1024, 1025, 1026]
# [1028, 1029, 1030, 1031, 1032]
# >>>
# >>> tagged_vlan_list=[]
# >>> for ifcfg_tagged_vlan_range in ifcfg_tagged_vlan_list:
# ...   if "-" in ifcfg_tagged_vlan_range:
# ...     tagged_vlan_list.extend( list( range( int(ifcfg_tagged_vlan_range.split("-")[0]), int(ifcfg_tagged_vlan_range.split("-")[1]) + 1 ) ) )
# ...
# >>> tagged_vlan_list
# [270, 271, 272, 273, 274, 275, 276, 701, 702, 703, 704, 705, 706, 707, 708, 1021, 1022, 1023, 1024, 1025, 1026, 1028, 1029, 1030, 1031, 1032]
# >>>


### How to get the list of VLANs from the "show running-configuration | grep vlan | grep interface" output in Dell OS10:
# >>> import napalm
# >>> driver=napalm.get_network_driver("dellos10")
# >>> device=driver(hostname="192.168.70.4", username="admin", password="admin")
# >>> device.open()
# >>> cmd = "show running-configuration | grep vlan | grep interface"
# >>> cfg = device.cli([cmd])[cmd]
# >>> cfg
# 'interface vlan1\ninterface vlan270\ninterface vlan271\ninterface vlan272\ninterface vlan273\ninterface vlan274\ninterface vlan275\ninterface vlan276\ninterface vlan701\ninterface vlan702\ninterface vlan703\ninterface vlan704\ninterface vlan705\ninterface vlan706\ninterface vlan707\ninterface vlan708\ninterface vlan1021\ninterface vlan1022\ninterface vlan1023\ninterface vlan1024\ninterface vlan1025\ninterface vlan1026\ninterface vlan1028\ninterface vlan1029\ninterface vlan1030\ninterface vlan1031\ninterface vlan1032'
# >>> vlancfg=cfg.replace("interface vlan","").split('\n')
# >>> vlancfg
# ['1', '270', '271', '272', '273', '274', '275', '276', '701', '702', '703', '704', '705', '706', '707', '708', '1021', '1022', '1023', '1024', '1025', '1026', '1028', '1029', '1030', '1031', '1032']
# >>>

