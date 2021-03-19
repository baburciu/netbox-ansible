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

        if "MEth" in int:
            int_mgmt_flag = "True"
        else:
            int_mgmt_flag = "False"

        if "NULL" not in int and "Vlan" not in int:
            print(f"******* Now we'll create NetBox interface {int} for device {device_hostname}")
            r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                   playbook='create_interface.yml',
                                   inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                   extravars={'interface_device': device_hostname, 'interface_name': str(int),
                                              'interface_mac_address': str(device_interfaces[int]['mac_address']),
                                              'interface_enabled': str(device_interfaces[int]['is_enabled']),
                                              'interface_type': int_type, 'interface_mtu': device_interfaces[int]['mtu'],
                                              'interface_mgmt_only': int_mgmt_flag,
                                              'interface_description': str(device_interfaces[int]['description']),
                                              'external_vars': './external_vars.yml',
                                              'ansible_python_interpreter':'/usr/bin/python3'})

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

                    print(f"******* Now we'll create NetBox cable between {other_end_host}'s {other_end_if} and {device_hostname}'s {int} ")
                    r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/',
                                           playbook='create_cable.yml',
                                           inventory='/home/boburciu/netbox-ansible-automation/hosts.yml',
                                           extravars={'cable_end_a_host': device_hostname, 'cable_end_a_if': int,
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

