# Use NAPALM to configure interfaces of Juniper QFX & EX switches
# Creating config file to be passed to JunOS and uploading it with NAPALM
# Bogdan Adrian Burciu 15/06/2021 v2

# -------------------------
# Credits:
# https://saidvandeklundert.net/2019-09-20-napalm/#Using%20NAPALM%20to%20configure%20devices

# -------------------------
# Prerequisite: export SW_USER=root SW_PASS=<secret_here>
# Run as: python3 junos-napalm-iface-description.py

import napalm
import os
import ast
import datetime

driver_junos = napalm.get_network_driver("junos")
network_devices = {"QFX-Juniper-SW-1": "X.X.X.1",
                   "EX-Juniper-SW-1": "X.X.X.11",
                   "EX-Juniper-SW-2": "X.X.X.12"}

# use phy connections input
# https://openstack-git-stg.itn.ftgroup/wiki/feper-admin/-/blob/master/ZTE_Testbed/README.md#phy-connections-input
extra_eq_phy = [
 {'Server': 'Dell-Server-1',
  'Server_port': 'iDRAC',
  'Server_sn': '1BLABLA',
  'Switch': 'EX-Juniper-SW-2',
  'Switch_port': 'ge-0/0/3'},
 {'Server': 'Dell-Server-1',
  'Server_bond_os': 'bond0',
  'Server_port': 'NIC1-P1',
  'Server_port_os': 'ens1f0',
  'Server_sn': '1BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/14'},
 {'Server': 'Dell-Server-1',
  'Server_bond_os': 'bond0',
  'Server_port': 'NIC1-P2',
  'Server_port_os': 'ens1f1',
  'Server_sn': '1BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/15'},
 {'Server': 'Dell-Server-1',
  'Server_port': 'intNIC-P1',
  'Server_port_os': 'eno1',
  'Server_sn': '1BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/16'},
 {'Server': 'Dell-Server-1',
  'Server_port': 'intNIC-P2',
  'Server_port_os': 'eno2',
  'Server_sn': '1BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/17'},
 {'Server': 'Dell-Server-2',
  'Server_port': 'iDRAC',
  'Server_sn': '2BLABLA',
  'Switch': 'EX-Juniper-SW-2',
  'Switch_port': 'ge-0/0/4'},
 {'Server': 'Dell-Server-2',
  'Server_bond_os': 'bond0',
  'Server_port': 'NIC1-P1',
  'Server_port_os': 'ens1f0',
  'Server_sn': '2BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/18'},
 {'Server': 'Dell-Server-2',
  'Server_bond_os': 'bond0',
  'Server_port': 'NIC1-P2',
  'Server_port_os': 'ens1f1',
  'Server_sn': '2BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/19'},
 {'Server': 'Dell-Server-2',
  'Server_port': 'intNIC-P1',
  'Server_port_os': 'eno1',
  'Server_sn': '2BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/20'},
 {'Server': 'Dell-Server-2',
  'Server_port': 'intNIC-P2',
  'Server_port_os': 'eno2',
  'Server_sn': '2BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/21'},
 {'Server': 'Dell-Server-3',
  'Server_port': 'iDRAC',
  'Server_sn': '3BLABLA',
  'Switch': 'EX-Juniper-SW-2',
  'Switch_port': 'ge-0/0/5'},
 {'Server': 'Dell-Server-3',
  'Server_bond_os': 'bond0',
  'Server_port': 'NIC1-P1',
  'Server_port_os': 'ens1f0',
  'Server_sn': '3BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/22'},
 {'Server': 'Dell-Server-3',
  'Server_bond_os': 'bond0',
  'Server_port': 'NIC1-P2',
  'Server_port_os': 'ens1f1',
  'Server_sn': '3BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/23'},
 {'Server': 'Dell-Server-3',
  'Server_port': 'intNIC-P1',
  'Server_port_os': 'eno1',
  'Server_sn': '3BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/24'},
 {'Server': 'Dell-Server-3',
  'Server_port': 'intNIC-P2',
  'Server_port_os': 'eno2',
  'Server_sn': '3BLABLA',
  'Switch': 'QFX-Juniper-SW-1',
  'Switch_port': 'et-0/0/25'},
 {'Server': 'Dell-Server-4',
  'Server_port': 'iDRAC',
  'Server_sn': '4BLABLA',
  'Switch': 'EX-Juniper-SW-1',
  'Switch_port': 'ge-0/0/1'},
 {'Server': 'Dell-Server-4',
  'Server_port': 'pciNIC2-P2',
  'Server_sn': '4BLABLA',
  'Switch': 'EX-Juniper-SW-1',
  'Switch_port': 'xe-0/1/2'}
]

# get unique dict values for the key "Switch" from input phy connection matrix
sw_list = list(set([ast.literal_eval(el1)["Switch"] for el1 in set([str(el2) for el2 in extra_eq_phy])]))
# sw_list = ['QFX-Juniper-SW-1', 'EX-Juniper-SW-2', 'EX-Juniper-SW-1']

for j in range(len(sw_list)):
    # first clear previous JunOS config file contents to start fresh
    open(f"junos_if_description_{sw_list[j]}.cfg", 'w').close()

    junos_cfg = open(f"junos_if_description_{sw_list[j]}.cfg", 'w+')
    for i in range(len(extra_eq_phy)):
        if extra_eq_phy[i]["Switch"] == sw_list[j]:
            if "Server_port_os" in extra_eq_phy[i].keys():
                (junos_cfg.write(f'set interfaces {extra_eq_phy[i]["Switch_port"]} description '
                                 f'link_to__{extra_eq_phy[i]["Server"]}<{extra_eq_phy[i]["Server_sn"]}>'
                                 f'__{extra_eq_phy[i]["Server_port"]}<{extra_eq_phy[i]["Server_port_os"]}> \n'))
            else:
                (junos_cfg.write(f'set interfaces {extra_eq_phy[i]["Switch_port"]} '
                                 f'description link_to__{extra_eq_phy[i]["Server"]}<{extra_eq_phy[i]["Server_sn"]}>'
                                 f'__{extra_eq_phy[i]["Server_port"]} \n'))

            if "Server_bond_os" in extra_eq_phy[i].keys():
                device = driver_junos(hostname=network_devices[extra_eq_phy[i]["Switch"]],
                                      username=str(os.environ.get("SW_USER")),
                                      password=str(os.environ.get("SW_PASS")))
                print("Connecting to {} for checking interface {} configuration ..."
                      .format(device.hostname, extra_eq_phy[i]["Switch_port"]))
                device.open()

                # for each switch interface collect the configuration by NAPALM
                # and if LAG member, set LAG with description
                cmd = "show configuration interfaces " + str(extra_eq_phy[i]["Switch_port"])
                iface_cfg = device.cli([cmd])[cmd]
                sw_lag = iface_cfg.split(" 802.3ad ")[1].split("\n", 2)[0].split(";")[0]
                # if LAG is configured with LACP in JunOS
                if len(sw_lag) < 3:
                    cmd = "show lacp interfaces " + str(extra_eq_phy[i]["Switch_port"])
                    iface_cfg = device.cli([cmd])[cmd]
                    sw_lag = iface_cfg.split("Aggregated interface: ")[1].split("\n", 2)[0]

                (junos_cfg.write(f'set interfaces {sw_lag} '
                                 f'description link_to__{extra_eq_phy[i]["Server"]}<{extra_eq_phy[i]["Server_sn"]}>'
                                 f'__{extra_eq_phy[i]["Server_bond_os"]} \n'))

                device.close()
                print("Done for {} .".format(device.hostname))

    junos_cfg.close()

    # keep only unique lines in JunOS config file
    with open(f"junos_if_description_{sw_list[j]}.cfg") as junos_cfg:
        junos_cfg_content = junos_cfg.read().split('\n')
    junos_cfg_content = set([line for line in junos_cfg_content if line != ''])
    junos_cfg_content = '\n'.join(junos_cfg_content)+'\n'
    with open(f"junos_if_description_{sw_list[j]}.cfg", 'w') as junos_cfg:
        junos_cfg.writelines(junos_cfg_content)

    # sort lines in JunOS config file
    with open(f"junos_if_description_{sw_list[j]}.cfg") as junos_cfg:
        junos_cfg_content_sorted = sorted(junos_cfg.readlines())
    with open(f"junos_if_description_{sw_list[j]}.cfg", 'w') as junos_cfg:
        junos_cfg.writelines(junos_cfg_content_sorted)

    # first save backup of running config and then load new configuration to each device
    device = driver_junos(hostname=network_devices[sw_list[j]],
                          username=str(os.environ.get("SW_USER")),
                          password=str(os.environ.get("SW_PASS")))
    print("Connecting to {} ...".format(device.hostname))
    device.open()

    run_config = device.get_config(retrieve='running')
    run_config = run_config['running']
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_cfg = open('backup_' + device.hostname + '_' + date + '_' + 'running-config', 'w')
    backup_cfg.write(run_config)
    backup_cfg.close()
    print("Done backing-up running configuration for {} .".format(device.hostname))

    device.load_merge_candidate(filename=f"junos_if_description_{sw_list[j]}.cfg")
    print(device.compare_config())
    device.commit_config()

    device.close()
    print("Done loading configuration for {} .".format(device.hostname))

# root@QFX-Juniper-SW-1> show configuration interfaces et-0/0/29
# ether-options {
#     802.3ad ae28;
# }
#
# {master:0}
# root@QFX-Juniper-SW-1> show configuration interfaces ae28
# mtu 9216;
# aggregated-ether-options {
#     lacp {
#         active;
#     }
# }
#
# {master:0}
# root@QFX-Juniper-SW-1>

# root@QFX-Juniper-SW-1> show configuration interfaces et-0/0/18
# ether-options {
#     802.3ad {
#         lacp {
#             force-up;
#         }
#         ae18;
#     }
# }
#
# {master:0}
# root@QFX-Juniper-SW-1>
