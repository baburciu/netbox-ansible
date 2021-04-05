# Using [Napalm](https://napalm.readthedocs.io/en/latest/index.html) to collect info from Huawei CE switches and NE router, following [this article](https://codingnetworks.blog/napalm-network-automation-python-working-with-huawei-vrp/) and using Ansible-Runner to run Ansible playbooks directly from Python

## 0. First steps:

 ### - Install Python3 venv (on Ubuntu):
boburciu@WX-5CG020BDT2:~$ ` sudo apt-get install python3-venv `
   
 ### - Creating Python venv: 
boburciu@WX-5CG020BDT2:~$ ` python3 -m venv envs/napalm-huawei `
```
boburciu@WX-5CG020BDT2:~$ ls -lt
total 0
drwxr-xr-x. 3 root root 20 Mar  3 15:34 envs
```
boburciu@WX-5CG020BDT2:~$ ` source envs/napalm-huawei/bin/activate `
```
(napalm-huawei) boburciu@WX-5CG020BDT2:~$
(napalm-huawei) boburciu@WX-5CG020BDT2:~$
```

 ### - Install Napalm:
(napalm-huawei) boburciu@WX-5CG020BDT2:~$ ` pip install --upgrade pip `
(napalm-huawei) boburciu@WX-5CG020BDT2:~$ ` pip3 install napalm `
(napalm-huawei) boburciu@WX-5CG020BDT2:~$ ` napalm --help `
```
usage: napalm [-h] [--user USER] [--password PASSWORD] --vendor VENDOR
              [--optional_args OPTIONAL_ARGS] [--debug]
              hostname {configure,call,validate} ...

Command line tool to handle configuration on devices using NAPALM.The script
will print the diff on the screen

positional arguments:
  hostname              Host where you want to deploy the configuration.

optional arguments:
  -h, --help            show this help message and exit
  --user USER, -u USER  User for authenticating to the host. Default: user
                        running the script.
  --password PASSWORD, -p PASSWORD
                        Password for authenticating to the host.If you do not
                        provide a password in the CLI you will be prompted.
  --vendor VENDOR, -v VENDOR
                        Host Operating System.
  --optional_args OPTIONAL_ARGS, -o OPTIONAL_ARGS
                        String with comma separated key=value pairs passed via
                        optional_args to the driver.
  --debug               Enables debug mode; more verbosity.

actions:
  {configure,call,validate}
    configure           Perform a configuration operation
    call                Call a napalm method
    validate            Validate configuration/state

Automate all the things!!!
(napalm-huawei) boburciu@WX-5CG020BDT2:~$
```

 ### - new Napalm drivers will be hosted under the [napalm-automation-community](https://github.com/napalm-automation-community) on GitHub

 ### - We'll use NAPALM [community driver for the Huawei CloudEngine Switch] (https://github.com/napalm-automation-community/napalm-ce):
 (napalm-huawei) boburciu@WX-5CG020BDT2:~$ ` pip3 install napalm-ce `
 (napalm-huawei) boburciu@WX-5CG020BDT2:~$ ` napalm --user orangeoln --password l0c@l@dm1n --vendor ce 192.168.201.24  call get_interfaces `
``` 
{
    "10GE1/0/1": {
        "description": "link_to_Server_R1_01_eth0",
        "is_enabled": true,
        "is_up": true,
        "last_flapped": -1.0,
        "mac_address": "C4:B8:B4:34:41:B1",
        "speed": 10000,
        "mtu": 9216
    },
:
:    
    "Eth-Trunk101": {
        "description": "link_to_Server1_bond0",
        "is_enabled": false,
        "is_up": false,
        "last_flapped": -1.0,
        "mac_address": "C4:B8:B4:34:41:B1",
        "speed": 0,
        "mtu": 9216
    },
    "MEth0/0/0": {
        "description": "",
        "is_enabled": true,
        "is_up": true,
        "last_flapped": -1.0,
        "mac_address": "C4:B8:B4:34:41:B0",
        "speed": 0,
        "mtu": 1500
:
:
    "Vlanif4001": {
        "description": "",
        "is_enabled": true,
        "is_up": true,
        "last_flapped": -1.0,
        "mac_address": "C4:B8:B4:34:41:BD",
        "speed": 0,
        "mtu": 1500
    }
}
(napalm-huawei) boburciu@WX-5CG020BDT2:~$
```

## 1. Using NAPALM Python library in python3 shell:
 (napalm-huawei) boburciu@WX-5CG020BDT2:~$ ` python3 `
``` 
Python 3.6.9 (default, Jan 26 2021, 15:33:00)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
```
>>> ` import napalm `
>>> ` driver=napalm.get_network_driver("ce") `
>>> ` device=driver(hostname="192.168.201.24", username="orangeoln", password="l0c@l@dm1n") `
>>> ` device.open() `
>>> ` device.get_facts() `
```
{'uptime': 17780100, 'vendor': 'Huawei', 'os_version': 'V200R002C50SPC800', 'serial_number': 'C                                      E6851HI', 'model': 'CE6851-48S6Q-HI', 'hostname': 'SWH-TOR-R1', 'fqdn': 'Unknown', 'interface_l                                      ist': ['10GE1/0/1', '10GE1/0/2', '10GE1/0/3', '10GE1/0/4', '10GE1/0/5', '10GE1/0/6', '10GE1/0/7                                      ', '10GE1/0/8', '10GE1/0/9', '10GE1/0/10', '10GE1/0/11', '10GE1/0/12', '10GE1/0/13', '10GE1/0/1                                      5', '10GE1/0/16', '10GE1/0/17', '10GE1/0/18', '10GE1/0/19', '10GE1/0/20', '10GE1/0/21', '10GE1/                                      0/22', '10GE1/0/23', '10GE1/0/24', '10GE1/0/25', '10GE1/0/27', '10GE1/0/28', '10GE1/0/30', '10G                                      E1/0/31', '10GE1/0/34', '10GE1/0/35', '10GE1/0/36', '10GE1/0/39', '10GE1/0/43', '10GE1/0/44', '                                      10GE1/0/45', '10GE1/0/46', '10GE2/0/1', '10GE2/0/2', '10GE2/0/3', '10GE2/0/4', '10GE2/0/5', '10                                      GE2/0/6', '10GE2/0/7', '10GE2/0/8', '10GE2/0/9', '10GE2/0/10', '10GE2/0/11', '10GE2/0/12', '10G                                      E2/0/13', '10GE2/0/15', '10GE2/0/16', '10GE2/0/17', '10GE2/0/18', '10GE2/0/19', '10GE2/0/20', '                                      10GE2/0/21', '10GE2/0/22', '10GE2/0/23', '10GE2/0/24', '10GE2/0/25', '10GE2/0/27', '10GE2/0/28'                                      , '10GE2/0/30', '10GE2/0/31', '10GE2/0/34', '10GE2/0/35', '10GE2/0/36', '10GE2/0/39', '10GE2/0/                                      40', '10GE2/0/43', '10GE2/0/44', '10GE2/0/45', '10GE2/0/46', '40GE1/0/4', '40GE1/0/5', '40GE1/0                                      /6', '40GE2/0/4', '40GE2/0/5', '40GE2/0/6', 'Eth-Trunk1', '10GE1/0/41', '10GE1/0/42', '10GE2/0/                                      41', '10GE2/0/42', 'Eth-Trunk2', '10GE1/0/47', '10GE1/0/48', '10GE2/0/47', '10GE2/0/48', 'Eth-T                                      runk3', 'Eth-Trunk4', 'Eth-Trunk7', 'Eth-Trunk10', 'Eth-Trunk13', 'Eth-Trunk14', '10GE1/0/14',                                       '10GE2/0/14', 'Eth-Trunk16', 'Eth-Trunk19', 'Eth-Trunk22', 'Eth-Trunk25', 'Eth-Trunk26', '10GE1                                      /0/26', '10GE2/0/26', 'Eth-Trunk27', 'Eth-Trunk28', 'Eth-Trunk29', '10GE1/0/29', '10GE2/0/29',                                       'Eth-Trunk30', 'Eth-Trunk31', 'Eth-Trunk32', '10GE1/0/32', '10GE2/0/32', 'Eth-Trunk33', '10GE1/                                      0/33', '10GE2/0/33', 'Eth-Trunk34', 'Eth-Trunk37', '10GE1/0/37', '10GE2/0/37', 'Eth-Trunk38', '                                      10GE1/0/38', '10GE2/0/38', 'Eth-Trunk40', '40GE1/0/3', '40GE2/0/3', 'Eth-Trunk44', '10GE1/0/40'                                      , 'Eth-Trunk101', 'MEth0/0/0', 'NULL0', 'Stack-Port1/1', '40GE1/0/1', '40GE1/0/2', 'Stack-Port2                                      /1', '40GE2/0/1', '40GE2/0/2', 'Vlanif5', 'Vlanif8', 'Vlanif1100', 'Vlanif1400', 'Vlanif4001']}
>>>
>>> 
>>>
```
>>> ` device.get_facts()['hostname'] `
```
'SWH-TOR-R1'
>>>
```
>>> ` ifs = device.get_interfaces() `
```
>>>
```
>>> ` for int in ifs.keys(): `
... `    print(f"{int} <=> {ifs[int]['description']} <=> {ifs[int]['mtu']}") `
```
10GE1/0/1 <=> link_to_Server_R1_01_eth0 <=> 9216
10GE1/0/2 <=> link_to_Server_R1_01_eth2 <=> 9216
10GE1/0/3 <=> link_to_Server_R1_01_eth4 <=> 9216
10GE1/0/4 <=> link_to_Server_R1_02_eth0 <=> 9216
10GE1/0/5 <=> link_to_Server_R1_02_eth2 <=> 9216
10GE1/0/6 <=> link_to_Server_R1_02_eth4 <=> 9216
10GE1/0/7 <=> link_to_Server_R1_03_eth0 <=> 9216
```

## 2. Using Ansible-Runner to call Ansible playbook in Py script:
 ### - Installing
(napalm-huawei) boburciu@WX-5CG020BDT2:~$ ` pip3 install ansible-runner `
```
(napalm-huawei) boburciu@WX-5CG020BDT2:~$ pwd
/home/boburciu
(napalm-huawei) boburciu@WX-5CG020BDT2:~$

boburciu@WX-5CG020BDT2:~$ python3
Python 3.6.9 (default, Jan 26 2021, 15:33:00)
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
 ### - Using (with methods from [doc](https://ansible-runner.readthedocs.io/en/latest/source/ansible_runner.html#ansible_runner.runner_config.RunnerConfig))
>>> ` import ansible_runner `

 ### - Playbook path is relative to _private_data_dir_ value
>>> ` ansible_runner.utils.isinventory('/home/boburciu/netbox-ansible-automation/hosts.yml') `
```
True
>>>
```
>>> ` r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/', playbook='create_vrf.yml', inventory='/home/boburciu/netbox-ansible-automation/hosts.yml') `
```
PLAY [Create VRF] **************************************************************

TASK [Create vrf with all information] *****************************************
fatal: [docker_netbox_19216820023]: FAILED! => {"msg": "The task includes an option with an undefined variable. The error was: 'url_var' is undefined\n\nThe error appears to be in '/home/boburciu/netbox-ansible-automation/create_vrf.yml': line 30, column 7, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\n    - name: Create vrf with all information\n      ^ here\n"}
...ignoring

PLAY RECAP *********************************************************************
docker_netbox_19216820023  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=1

>>>
```

 ### - Per [Ansible Runner doc](https://ansible-runner.readthedocs.io/en/latest/source/ansible_runner.html#ansible_runner.runner_config.RunnerConfig), you can either send a dict to _extravars_ param of _ansible_runner.run()_ method or have the extra-var key:value pairs in _env/extravars_ in _private_data_dir_
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$ ` cat env/extravars `
```
#"/home/boburciu/netbox-ansible-automation/external_vars.yml"
url_var: "http://192.168.200.23:8001/"
token_var: "2d1d02344364e823b95928730b75042d9b87914e"
vrf_name: ByAnsibleRunner
vrf_rd: 65001:92063
vrf_description: "Test for underlay switches and firewalls and IPMI network of servers"
vrf_tag: oiaas
tenant_name: Underlay
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$ pwd
/home/boburciu/netbox-ansible-automation
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$
```
>>> ` r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/', playbook='create_vrf.yml', inventory='/home/boburciu/netbox-ansible-automation/hosts.yml') `
```
PLAY [Create VRF] **************************************************************

TASK [Create vrf with all information] *****************************************
changed: [docker_netbox_19216820023]

PLAY RECAP *********************************************************************
docker_netbox_19216820023  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

>>>
```
![Netbox change](./images/vrf_by_ansiblerunner.PNG)


 ### - Need to send all extra-var params as dictionary elements in _extravars_ argument of the _ansible_runner.run()_ method and also have _env/extravars_ in _private_data_dir_ formatted as dictionary (the 'external_vars':'./external_vars.yml' is not sent to playbook import, don't know why)
>>> ` r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/', playbook='create_vrf.yml', inventory='/home/boburciu/netbox-ansible-automation/hosts.yml', extravars={'vrf_name': 'ByAnsibleRunner-inlineArg', 'vrf_rd': '65001:92065', 'vrf_description': 'Test', 'vrf_tag': 'oiaas', 'tenant_name': 'Underlay', 'external_vars':'./external_vars.yml'}) `
```
PLAY [Create VRF] **************************************************************

TASK [Create vrf with all information] *****************************************
changed: [docker_netbox_19216820023]

PLAY RECAP *********************************************************************
docker_netbox_19216820023  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

>>>
```

 ### - Call to create interface in NetBox, running playbook from Py shell:
>>> ` r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/', playbook='create_interface.yml', inventory='/home/boburciu/netbox-ansible-automation/hosts.yml', extravars={'interface_device':'SWH-OoB-R2', 'interface_name':'GE1/0/1', 'interface_mac_address':'48:F8:DB:D4:AB:11', 'interface_enabled':'yes', 'interface_type': "1000BASE-T", 'interface_mtu': 9216, 'interface_mgmt_only': 'false', 'interface_description':'link_to_Server_R2_01_mgmt','external_vars':'./external_vars.yml'}) `
```
PLAY [Create interface] ********************************************************

TASK [include_vars] ************************************************************
ok: [docker_netbox_19216820023]

TASK [Create interface] ********************************************************
changed: [docker_netbox_19216820023]

PLAY RECAP *********************************************************************
docker_netbox_19216820023  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

>>>
```

 ### - Call to create cable connection in NetBox, running playbook from Py shell (with verbosity level):
>>> ` r = ansible_runner.run(private_data_dir='/home/boburciu/netbox-ansible-automation/', playbook='create_cable.yml', inventory='/home/boburciu/netbox-ansible-automation/hosts.yml', extravars={'cable_end_a_host':'SWH-OoB-R2', 'cable_end_a_if': 'GE1/0/1', 'cable_end_b_host': '2288H_V5_2102311XBSN0JA000034', 'cable_end_b_if': 'iBMC', 'cable_type':'mmf-om3', 'external_vars':'./external_vars.yml'}, verbosity=1) `
```
TASK [Create cable connection] *************************************************
changed: [docker_netbox_19216820023] => {"cable": {"color": "", "custom_fields": {}, "id": 8, "label": "", "    length": null, "length_unit": null, "status": "connected", "tags": [], "termination_a": 381, "termination_a_    id": 381, "termination_a_type": "dcim.interface", "termination_b": 203, "termination_b_id": 203, "terminatio    n_b_type": "dcim.interface", "type": "mmf-om3", "url": "http://192.168.200.23:8001/api/dcim/cables/8/"}, "ch    anged": true, "msg": "cable dcim.interface GE1/0/1 <> dcim.interface iBMC updated"}

PLAY RECAP *********************************************************************
docker_netbox_19216820023  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ign    ored=0

>>>
```

## 3. Using [Mitogen for Ansible](https://mitogen.networkgenomics.com/ansible_detailed.html) to decrease Ansible execution time is currently supported only for Ansible 2.9:

boburciu@WX-5CG020BDT2:~$ ` python3 -m venv envs/ansible2.9 `
boburciu@WX-5CG020BDT2:~$ ` source envs/ansible2.9/bin/activate `
(ansible2.9) boburciu@WX-5CG020BDT2:~$ ansible --version
ansible 2.10.3
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/boburciu/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/boburciu/.local/lib/python3.6/site-packages/ansible
  executable location = /home/boburciu/.local/bin/ansible
  python version = 3.6.9 (default, Jan 26 2021, 15:33:00) [GCC 8.4.0]
(ansible2.9) boburciu@WX-5CG020BDT2:~$
(ansible2.9) boburciu@WX-5CG020BDT2:~$ ` pip install --upgrade pip `
Cache entry deserialization failed, entry ignored
Collecting pip
  Using cached https://files.pythonhosted.org/packages/fe/ef/60d7ba03b5c442309ef42e7d69959f73aacccd0d86008362a681c4698e83/pip-21.0.1-py3-none-any.whl
Installing collected packages: pip
  Found existing installation: pip 9.0.1
    Uninstalling pip-9.0.1:
      Successfully uninstalled pip-9.0.1
Successfully installed pip-21.0.1
(ansible2.9) boburciu@WX-5CG020BDT2:~$ ` pip3 install ansible==2.9.19rc1 `
Collecting ansible==2.9.19rc1
  Using cached ansible-2.9.19rc1.tar.gz (14.3 MB)


 ### - To measure execution time for Ansible one needs to add ` callback_whitelist = profile_tasks ` in ` [default] ` section in your _ansible.cfg_:
```
boburciu@WX-5CG020BDT2:~$ cat /etc/ansible/ansible.cfg -n | grep callback_whitelist
    83  #callback_whitelist = timer, mail
boburciu@WX-5CG020BDT2:~$ vi +83 /etc/ansible/ansible.cfg
boburciu@WX-5CG020BDT2:~$
boburciu@WX-5CG020BDT2:~$ sudo vi +83 /etc/ansible/ansible.cfg
[sudo] password for boburciu:
boburciu@WX-5CG020BDT2:~$ cat /etc/ansible/ansible.cfg -n | grep callback_whitelist
    83  #callback_whitelist = timer, mail
    84  callback_whitelist = ansible.posix.profile_tasks
boburciu@WX-5CG020BDT2:~$
```

 ### - Download and extract _mitogen-0.2.9.tar.gz_
```
 boburciu@WX-5CG020BDT2:~$ mv /mnt/c/Users/bogdan.burciu/Downloads/mitogen-0.2.9.tar.gz .
boburciu@WX-5CG020BDT2:~$ ls -lt
total 288
-rwxrwxrwx 1 boburciu boburciu 210868 Mar 11 15:55 mitogen-0.2.9.tar.gz
drwxrwxrwx 1 boburciu boburciu   4096 Mar 11 13:41 netbox-ansible-automation
drwxrwxrwx 1 boburciu boburciu   4096 Mar  9 14:57 libvirt-vm
drwxrwxrwx 1 boburciu boburciu   4096 Mar  4 13:45 NAPALM
drwxrwxrwx 1 boburciu boburciu   4096 Mar  4 09:20 envs
drwxrwxrwx 1 boburciu boburciu   4096 Feb 25 15:17 FLOATING_IP_cfg
-rw-rw-rw- 1 boburciu boburciu    274 Feb 15 10:49 1
drwxrwxrwx 1 boburciu boburciu   4096 Feb 10 18:28 parse_excel_servers
drwxrwxrwx 1 boburciu boburciu   4096 Feb  6 13:25 dell-ansible-automation
drwxrwxrwx 1 boburciu boburciu   4096 Aug 26  2020 bin
-rw-rw-rw- 1 boburciu boburciu      0 Aug 25  2020 set
boburciu@WX-5CG020BDT2:~$ tar -xf mitogen-0.2.9.tar.gz
boburciu@WX-5CG020BDT2:~$ ls -lt
total 288
-rwxrwxrwx 1 boburciu boburciu 210868 Mar 11 15:55 mitogen-0.2.9.tar.gz
drwxrwxrwx 1 boburciu boburciu   4096 Mar 11 13:41 netbox-ansible-automation
drwxrwxrwx 1 boburciu boburciu   4096 Mar  9 14:57 libvirt-vm
drwxrwxrwx 1 boburciu boburciu   4096 Mar  4 13:45 NAPALM
drwxrwxrwx 1 boburciu boburciu   4096 Mar  4 09:20 envs
drwxrwxrwx 1 boburciu boburciu   4096 Feb 25 15:17 FLOATING_IP_cfg
-rw-rw-rw- 1 boburciu boburciu    274 Feb 15 10:49 1
drwxrwxrwx 1 boburciu boburciu   4096 Feb 10 18:28 parse_excel_servers
drwxrwxrwx 1 boburciu boburciu   4096 Feb  6 13:25 dell-ansible-automation
drwxrwxrwx 1 boburciu boburciu   4096 Aug 26  2020 bin
-rw-rw-rw- 1 boburciu boburciu      0 Aug 25  2020 set
drwxr-xr-x 1 boburciu boburciu   4096 Nov  2  2019 mitogen-0.2.9
boburciu@WX-5CG020BDT2:~$ 
boburciu@WX-5CG020BDT2:~$ cat mitogen-0.2.9/ansible_mitogen/plugins/strategy/
__init__.py             mitogen_free.py         mitogen_linear.py
mitogen.py              mitogen_host_pinned.py
boburciu@WX-5CG020BDT2:~$
```
 ### - Modify _ansible.cfg_ params for _strategy_plugins_ and _strategy_ to *mitogen_linear*:
```
[defaults]
strategy_plugins = /path/to/mitogen-0.2.9/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```
```
boburciu@WX-5CG020BDT2:~$
boburciu@WX-5CG020BDT2:~$ cat /etc/ansible/ansible.cfg -n | grep strategy_plugins
   203  #strategy_plugins   = /usr/share/ansible/plugins/strategy
boburciu@WX-5CG020BDT2:~$
boburciu@WX-5CG020BDT2:~$ cat /etc/ansible/ansible.cfg -n | grep strategy
   203  #strategy_plugins   = /usr/share/ansible/plugins/strategy
   206  # by default, ansible will use the 'linear' strategy but you may want to try
   208  #strategy = free
boburciu@WX-5CG020BDT2:~$
boburciu@WX-5CG020BDT2:~$ sudo vi +203 /etc/ansible/ansible.cfg
[sudo] password for boburciu:
boburciu@WX-5CG020BDT2:~$ 
boburciu@WX-5CG020BDT2:~$ sed -n 203p /etc/ansible/ansible.cfg
strategy_plugins   = ~/mitogen-0.2.9/ansible_mitogen/plugins/strategy
boburciu@WX-5CG020BDT2:~$
boburciu@WX-5CG020BDT2:~$ sed -n 208p /etc/ansible/ansible.cfg
strategy = mitogen_linear
boburciu@WX-5CG020BDT2:~$
```