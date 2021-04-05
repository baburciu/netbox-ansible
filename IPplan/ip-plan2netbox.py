# Parse XLS for IP plan and create NetBox objects based on that
# Creating NetBox IP addresses, vlan interfaces and prefixes by Ansible automation (playook called by python with ansible_runner)
# Bogdan Adrian Burciu 31/03/2021

# -------------------------
# Credits:
# https://stackoverflow.com/questions/27590039/running-ansible-playbook-using-python-api

import xlrd
import ansible_runner

sh = xlrd.open_workbook('/home/ubuntu/NEO_Alpha_IaC/NEO_IP_plan_4_NetBox.xls').sheet_by_index(0)
assigned_host = sh.col_values(0, start_rowx=1)
ip_addr = sh.col_values(1, start_rowx=1)
prefix_vlan = sh.col_values(2, start_rowx=1)
assigned_role = sh.col_values(3, start_rowx=1)  # <== lists of all values in 4th column D (#3, first being #0) of input .xlsx
assigned_interface = sh.col_values(4, start_rowx=1)
assigned_tenant = sh.col_values(5, start_rowx=1)
prefix = sh.col_values(6, start_rowx=1)
prefix_description = sh.col_values(7, start_rowx=1)
assigned_host_vlans_mac = sh.col_values(8, start_rowx=1)
vm_host = sh.col_values(9, start_rowx=1)
vm_vcpu = sh.col_values(10, start_rowx=1)
vm_ram = sh.col_values(11, start_rowx=1)
vm_disk = sh.col_values(12, start_rowx=1)
vm_tenant = sh.col_values(13, start_rowx=1)

for i in range(len(ip_addr)):
    if "nope" not in prefix[i]:
        # NetBox: create the prefix
        print(f"******* Now we'll create NetBox prefix object {prefix[i]} for VLAN {str(int(prefix_vlan[i]))}")
        r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                               playbook='create_prefix.yml',
                               inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                               extravars={'prefix': prefix[i], 'site_name': "Labs",
                                          'tenant_name': assigned_tenant[i], 'vlan_id': str(int(prefix_vlan[i])),
                                          'prefix_description': prefix_description[i],
                                          'external_vars': './external_vars.yml',
                                          'ansible_python_interpreter': '/usr/bin/python3'})

    if "nope" not in vm_host[i]:
        # NetBox: create the VM
        print(f"******* Now we'll create NetBox VM object {assigned_host[i]}, hosted by {vm_host[i]}")
        r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                               playbook='create_vm.yml',
                               inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                               extravars={'vm_cluster_type': 'libvirt', 'vm_cluster': str('KVM_'+str(vm_host[i])),
                                          'vm_host': vm_host[i], 'vm_name': assigned_host[i],
                                          'vm_vcpu': int(vm_vcpu[i]), 'vm_ram': int(vm_ram[i]),
                                          'vm_disk': int(vm_disk[i]), 'vm_tenant': vm_tenant[i],
                                          'external_vars': './external_vars.yml',
                                          'ansible_python_interpreter': '/usr/bin/python3'})

        # NetBox: create the interface for the VM
        print(f"******* Now we'll create NetBox VMI object {assigned_interface[i]} for {assigned_host[i]}")
        r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                               playbook='create_vm_interface.yml',
                               inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                               extravars={'vmi_name': assigned_interface[i], 'vm_name': assigned_host[i],
                                          'external_vars': './external_vars.yml',
                                          'ansible_python_interpreter': '/usr/bin/python3'})


    if "vlan" in assigned_interface[i] and "nope" in vm_host[i]:
        int_type = "Virtual"
        # NetBox: create the interface for a physical device
        print(f"******* Now we'll create NetBox interface {assigned_interface[i]} for device {assigned_host[i]}")
        r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                               playbook='create_interface.yml',
                               inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                               extravars={'interface_device': assigned_host[i], 'interface_name': assigned_interface[i],
                                          'interface_mac_address': assigned_host_vlans_mac[i],
                                          'interface_enabled': 'yes',
                                          'interface_type': int_type, 'interface_mtu': 9200,
                                          'interface_mgmt_only': 'no',
                                          'interface_description': assigned_interface[i],
                                          'external_vars': './external_vars.yml',
                                          'ansible_python_interpreter': '/usr/bin/python3'})


    if "nope" not in assigned_role[i]:
        if "nope" not in vm_host[i]:
            # NetBox: create the IP address (with a role) and assign it to an interface of VM
            print(f"******* Now we'll create NetBox IP address {ip_addr[i]} for device {assigned_host[i]}'s interface {assigned_interface[i]}")
            r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                   playbook='create_ip_addr.yml',
                                   inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                   extravars={'ip_addr_address': ip_addr[i], 'ip_addr_tenant': assigned_tenant[i],
                                              'ip_addr_status': 'Active', 'ip_addr_description': assigned_interface[i],
                                              'ip_addr_interface_name': assigned_interface[i], 'ip_addr_interface_vm': assigned_host[i],
                                              'ip_addr_role': assigned_role[i],
                                              'external_vars': './external_vars.yml',
                                              'ansible_python_interpreter': '/usr/bin/python3'})
        else:
            # NetBox: create the IP address (with a role) and assign it to an interface of physical appliance
            print(f"******* Now we'll create NetBox IP address {ip_addr[i]} for device {assigned_host[i]}'s interface {assigned_interface[i]}")
            r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                   playbook='create_ip_addr.yml',
                                   inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                   extravars={'ip_addr_address': ip_addr[i], 'ip_addr_tenant': assigned_tenant[i],
                                              'ip_addr_status': 'Active', 'ip_addr_description': assigned_interface[i],
                                              'ip_addr_interface_name': assigned_interface[i], 'ip_addr_interface_device': assigned_host[i],
                                              'ip_addr_role': assigned_role[i],
                                              'external_vars': './external_vars.yml',
                                              'ansible_python_interpreter': '/usr/bin/python3'})
    else:
        if "nope" not in vm_host[i]:
            # NetBox: create the IP address (without a role) and assign it to an interface of VM
            print(f"******* Now we'll create NetBox IP address {ip_addr[i]} for device {assigned_host[i]}'s interface {assigned_interface[i]}")
            r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                   playbook='create_ip_addr.yml',
                                   inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                   extravars={'ip_addr_address': ip_addr[i], 'ip_addr_tenant': assigned_tenant[i],
                                              'ip_addr_status': 'Active', 'ip_addr_description': assigned_interface[i],
                                              'ip_addr_interface_name': assigned_interface[i], 'ip_addr_interface_vm': assigned_host[i],
                                              'external_vars': './external_vars.yml',
                                              'ansible_python_interpreter': '/usr/bin/python3'})
        else:
            # NetBox: create the IP address (without a role) and assign it to an interface of physical appliance
            print(f"******* Now we'll create NetBox IP address {ip_addr[i]} for device {assigned_host[i]}'s interface {assigned_interface[i]}")
            r = ansible_runner.run(private_data_dir='/home/ubuntu/netbox-ansible/',
                                   playbook='create_ip_addr.yml',
                                   inventory='/home/ubuntu/netbox-ansible/hosts.yml',
                                   extravars={'ip_addr_address': ip_addr[i], 'ip_addr_tenant': assigned_tenant[i],
                                              'ip_addr_status': 'Active', 'ip_addr_description': assigned_interface[i],
                                              'ip_addr_interface_name': assigned_interface[i], 'ip_addr_interface_device': assigned_host[i],
                                              'external_vars': './external_vars.yml',
                                              'ansible_python_interpreter': '/usr/bin/python3'})
