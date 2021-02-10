# Parsing Feper servers 25-11-2020.xlsx
# Parsing Feper servers 25-11-2020.xlsx
# Creating IaC for NetBox servers addition by Ansible automation
# Bogdan Adrian Burciu 06/02/2021 vers 1

# -------------------------
# Credits:
# https://stackoverflow.com/questions/29518833/editing-yaml-file-by-python
# https://buildmedia.readthedocs.org/media/pdf/yaml/latest/yaml.pdf
# https://stackoverflow.com/questions/3583265/compare-result-from-hexdigest-to-a-string

import sys
import ruamel.yaml
import xlrd
import hashlib

sh = xlrd.open_workbook('/home/boburciu/parse_excel_servers/Feper_servers_25-11-2020_plus.xls').sheet_by_index(0)
hostname = sh.col_values(0, start_rowx=2)
oob_ip = sh.col_values(1, start_rowx=2)
sn = sh.col_values(2, start_rowx=2)
model = sh.col_values(3, start_rowx=2)  # <== lists of all values in 4th column D (#3, first being #0) of input .xlsx
blade_bay = sh.col_values(4, start_rowx=2)
form_factor = sh.col_values(5, start_rowx=2)
rack = sh.col_values(6, start_rowx=2)
rack_ru = sh.col_values(7, start_rowx=2)
role = sh.col_values(8, start_rowx=2)
pn = sh.col_values(9, start_rowx=2)
mgmt_if = sh.col_values(10, start_rowx=2)
specs_cpu = sh.col_values(11, start_rowx=2)
specs_cores = sh.col_values(12, start_rowx=2)
specs_ram_proc = sh.col_values(13, start_rowx=2)
specs_ram_total = sh.col_values(14, start_rowx=2)
specs_storage = sh.col_values(15, start_rowx=2)
specs_nic = sh.col_values(16, start_rowx=2)
tenant = sh.col_values(17, start_rowx=2)

yaml = ruamel.yaml.YAML()
# yaml.preserve_quotes = True

for i in range(len(oob_ip)):
    with open('/home/boburciu/netbox-ansible-automation/external_vars.yml') as fp:
        elem = yaml.load(fp)
        elem['rack_name'] = rack[i]
        elem['rack_comments'] = '--'
        elem['rack_facility_id'] = hash(sn[i]) % 10**8
        elem['tenant_name'] = tenant[i]
        elem['tenant_description'] = tenant[i]
        elem['device_primary_ip4'] = oob_ip[i]+"/24"
        elem['device_serial'] = sn[i]
        elem['device_manufacturer_name'] = model[i].split(' ',1)[0]
        elem['device_model'] = model[i].split(' ',1)[1]
        elem['device_hw_set_id'] = "xx"+ model[i].split(' ',1)[0] + model[i].split(' ',1)[1]
        elem['device_rack_name'] = rack[i]
        if form_factor[i] == 'blade':
            elem['device_subdevice_role'] = 'child'
            elem['device_u_height'] = '0'
            elem['device_bay_blade'] = blade_bay[i].split("-")[0]
            elem['device_position_in_rack'] = blade_bay[i]
            if blade_bay[i].split("-")[1] == 'Chassis 1':
                elem['device_bay_chassis'] = 'c7000_Enclosure_CZ00CHASSIS1'
            elif blade_bay[i].split("-")[1] == 'Chassis 2':
                elem['device_bay_chassis'] = 'c7000_Enclosure_CZ270100G5'
        else:
            elem['device_subdevice_role'] = 'parent'
            elem['device_position_in_rack'] = int(rack_ru[i])
            elem['device_u_height'] = form_factor[i].split("U")[0]
        # set the device_role_color as first 6 digits of its Hex hash, calculated after encoding and MD5 hashing of device_role_name
        elem['device_role_name'] = role[i]
        elem['device_role_color'] = (hashlib.md5(elem['device_role_name'].encode())).hexdigest()[0:6]
        elem['device_comments'] = str(specs_cpu[i]) + '; ' + str(specs_ram_proc[i]) + '; ' + str(specs_ram_total[i]) + '; ' + str(specs_storage[i]) + '; ' + str(specs_nic[i])
        elem['device_hostname'] = hostname[i]
        elem['device_tenant'] = tenant[i]
        elem['interface_device'] = elem['device_hostname']
        elem['ip_addr_interface_device'] = elem['device_hostname']
        elem['ip_addr_address'] = elem['device_primary_ip4']
        elem['ip_addr_tenant'] = tenant[i]
        elem['interface_name'] = mgmt_if[i]
        elem['ip_addr_interface_name'] = mgmt_if[i]
        elem['device_part_number'] = pn[i]
    # yaml.dump(elem, sys.stdout)
    f = open("/home/boburciu/parse_excel_servers/external_vars_"+str(hostname[i])+".yml", 'wb+')
    yaml.dump(elem, f)
    f.close()




