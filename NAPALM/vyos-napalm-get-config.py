#! /usr/bin/env python3

import napalm
import os
import datetime


path = os.getcwd()

try:
  os.stat(path+'/backup_config')
except:
  os.mkdir(path+'/backup_config')

device_list = [["VYOS-Proxy","192.168.X.X"]]

driver_vyos = napalm.get_network_driver("vyos")
network_devices = []
for device in device_list:
    network_devices.append(
        driver_vyos(
            hostname=device[1],
            username="vyos",
            password="vyos"
        )
    )

for device in network_devices:
    print("Connecting to {} ...".format(device.hostname))
    device.open()

    print("Getting device configuration to extract running config")
    # per https://github.com/napalm-automation-community/napalm-vyos/blob/a5d3b946637f536879c33a758f94b133dc2e67bd/napalm_vyos/vyos.py#L923
    device_config = device.get_config(retrieve='running')
    run_config = device_config['running']
    device_facts = device.get_facts()
    device_hostname = device_facts['hostname']
    date = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    # create file with running config in backup_config folder
    file = open(path+'/backup_config/'+device_hostname+'_'+date+'_'+'running-config','w')
    file.write(run_config)
    file.close()

    device.close()
    print("Done for {} .".format(device.hostname))
