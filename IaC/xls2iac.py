#! /usr/bin/env python3

# Declaring physical devices as IaC for addition in NetBox by Ansible automation
# Bogdan Adrian Burciu 24/08/2021 vers 2

# How to run:
# [root@NetboX netbox-ansible-automation]# python3 IaC/xls2iac.py --help
# usage: xls2iac.py [-h] --xls-path XLS_PATH --template-path TEMPLATE_PATH
#                   --output-dir OUTPUT_DIR
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --xls-path XLS_PATH   the absolute path where input xls is kept;
#   --template-path TEMPLATE_PATH
#                         the absolute path where input
#                         external_vars_template.yml is kept;
#   --output-dir OUTPUT_DIR
#                         the absolute path for the dir where obtained
#                         external_vars_XX.yml are to be saved;
# [root@NetboX netbox-ansible-automation]#
# [root@NetboX netbox-ansible-automation]# python3 IaC/xls2iac.py \
# > --xls-path /root/Farm_IaC_netbox-ansible_19082021/Farm_NetBox_IaC_19082021.xls \
# > --template-path /root/netbox-ansible-automation/external_vars_template.yml \
# > --output-dir /root/Farm_IaC_netbox-ansible_19082021
# [root@NetboX netbox-ansible-automation]#

import sys
import ruamel.yaml
import xlrd
import hashlib
import argparse


def main():
    # Main parser
    parser = argparse.ArgumentParser()

    # Usual arguments which are applicable for the whole script / top-level args;
    parser.add_argument('--xls-path',
                        dest='xls_path',
                        action='store',
                        required=True,
                        help='the absolute path where input xls is kept;')

    parser.add_argument('--template-path',
                        dest='template_path',
                        action='store',
                        required=True,
                        help='the absolute path where input external_vars_template.yml is kept;')

    parser.add_argument('--output-dir',
                        dest='output_dir',
                        action='store',
                        required=True,
                        help='the absolute path for the dir where obtained external_vars_XX.yml are to be saved;')

    args = parser.parse_args()

    sh = xlrd.open_workbook(args.xls_path).sheet_by_index(0)
    hostname = sh.col_values(0, start_rowx=2)
    oob_ip = sh.col_values(1, start_rowx=2)
    sn = sh.col_values(2, start_rowx=2)
    model = sh.col_values(3, start_rowx=2)
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
        with open(args.template_path) as fp:
            elem = yaml.load(fp)
            elem['rack_name'] = rack[i]
            elem['rack_comments'] = '--'
            elem['rack_facility_id'] = hash(rack[i]) % 10 ** 8
            elem['rack_serial'] = hash(rack[i]) % 10 ** 4
            elem['tenant_name'] = tenant[i]
            elem['tenant_description'] = tenant[i]
            elem['device_primary_ip4'] = oob_ip[i] + "/25"
            elem['device_serial'] = sn[i]
            elem['device_manufacturer_name'] = model[i].split(' ', 1)[0]
            elem['device_model'] = model[i].split(' ', 1)[1]
            elem['device_hw_set_id'] = (hashlib.md5(pn[i].encode())).hexdigest()[0:6]
            elem['device_rack_name'] = rack[i]
            if form_factor[i] == 'blade':
                elem['device_subdevice_role'] = 'child'
                elem['device_u_height'] = '0'
                elem['device_bay_blade'] = blade_bay[i].split("-")[0]
                elem['device_position_in_rack'] = blade_bay[i]
                if blade_bay[i].split("-")[1] == 'Chassis 1':
                    elem['device_bay_chassis'] = 'HP_c7000_Chassis1'
                elif blade_bay[i].split("-")[1] == 'Chassis 2':
                    elem['device_bay_chassis'] = 'HP_c7000_Chassis2'
            else:
                elem['device_subdevice_role'] = 'parent'
                elem['device_position_in_rack'] = int(rack_ru[i])
                elem['device_u_height'] = form_factor[i].split("U")[0]
            # set the device_role_color as first 6 digits of its Hex hash,
            # calculated after encoding and MD5 hashing of device_role_name
            elem['device_role_name'] = role[i]
            elem['device_role_color'] = (hashlib.md5(elem['device_role_name'].encode())).hexdigest()[0:6]
            elem['device_comments'] = '{0}; {1}; {2}; {3}; {4}; {5}'.format(str(specs_cpu[i]), str(specs_cores[i]),
                                                                            str(specs_ram_proc[i]),
                                                                            str(specs_ram_total[i]),
                                                                            str(specs_storage[i]), str(specs_nic[i]))
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
        f = open(args.output_dir + "/external_vars_" + str(hostname[i]) + ".yml", 'wb+')
        yaml.dump(elem, f)
        f.close()


if __name__ == '__main__':
    main()
