# netbox-ansible  [![HitCount](http://hits.dwyl.com/bogdanadrian-burciu/netbox-ansible.svg)](http://hits.dwyl.com/bogdanadrian-burciu/netbox-ansible)
## Ansible playbooks usage for Netbox automation, based on [Galaxy collection](https://docs.ansible.com/ansible/latest/collections/netbox/netbox/).
[![Inline docs](http://inch-ci.org/github/bogdanadrian-burciu/netbox-ansible.svg?branch=master)](http://inch-ci.org/github/bogdanadrian-burciu/netbox-ansible)
## 0. How to install Ansible Galaxy collection to correct path:

boburciu@WX-5CG020BDT2:~$ ` ansible-config list | grep COLLECTIONS_PATHS -C1 ` _# verify default location for the collections, so that the new modules can be read by Ansible cfg_
```
    Ansible version
COLLECTIONS_PATHS:
  default: ~/.ansible/collections:/usr/share/ansible/collections
--
  env:
  - name: ANSIBLE_COLLECTIONS_PATHS
  - name: ANSIBLE_COLLECTIONS_PATH
 
boburciu@WX-5CG020BDT2:~$
boburciu@WX-5CG020BDT2:~$
``` 
boburciu@WX-5CG020BDT2:~$ ` ansible-galaxy collection install netbox.netbox --collections-path ~/.ansible/collections ` _# installing the collection of roles in proper location_

## 1. How to add/remove NetBox WebUI Organization tab objects:

boburciu@WX-5CG020BDT2: $  `cd ~/netbox-ansible-automation`  <br/>
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$ `cat external_vars.yml `  <br/>
```
---
# external_vars.yml to be used in playbooks called in order by import_playbook

url_var: "http://192.168.200.23:8001/"
token_var: "97dab58500f94c141d63fb78b6406f9b53a119ac"

 ======== variables used for NetBox WebUI Organization tab objects ======== ##
tag1_name: mgmt
tag1_description: "Management port"
tag1_color: 0000FF  # RGB color in hexadecimal
tag2_name: srv
tag2_description: Server
tag2_color: FF00FF
tag3_name: oiaas
tag3_description: "Orange IaaS deployment"
tag3_color: FFA500

region_name: "EMEA"

site_name: Feper-Bucharest
site_status: Planned
site_region: "EMEA"
site_facility: Hyperscale DC
site_asn: 8953    # found by trail and error that needs to be integer
site_time_zone: Europe/Bucharest
site_description: ORANGE/TGI/OLN/CISS/ITE DC in Romania
site_physical_address: Blvd Dimitrie Pompeiu 8, Bucharest, 020337
site_shipping_address: Blvd Dimitrie Pompeiu 8, Bucharest, 020337
site_latitude: '44.480367'    # found by trail and error the need to ensure  there are no more than 8 digits in total
site_longitude: '26.117824'    # found by trail and error the need to ensure  there are no more than 9 digits in total
site_contact_name: Mihai Olteanu
site_contact_phone:     0040744441242
site_contact_email: Mihai.Olteanu@orange.com

tenant_group_name: IaaS4Telco
tenant_name: HuaweiContrailcalif    # found by trail and error that does not support underscore, for VRF to be referenced to its name
tenant_description: "OIaaS G4R2 w/ Contrail SDN backend"
tenant_comments: "OIaaS G4R2 w/ Contrail SDN backend"
tenant_tag: oiaas

rack_group_name: Huawei
rack_site: Feper-Bucharest
rack_role_name: "Hyperscale infra"
rack_role_color: DF2E08
rack_name: R1
rack_desc_units: no   # rack units will be numbered top-to-bottom, yes or no
rack_outer_unit: Millimeters   # whether the rack unit is in Millimeters or Inches and is required if outer_width/outer_depth is specified
rack_outer_width: 605   # per https://www.ibm.com/support/pages/overview-ibm-42u-and-47u-1200-mm-deep-static-and-deep-dynamic-rack
rack_outer_depth: 1200
rack_type: 4-post cabinet    # Choices: 2-post frame, 4-post frame, 4-post cabinet, Wall-mounted frame, Wall-mounted cabinet
rack_u_height: 42
rack_width: 23     # The rail-to-rail width, choices: 10, 19, 21, 23
rack_serial: 00000000
rack_facility_id: 00000000
rack_comments: "Room E203, Row#4 Rack#1"

 ======== variables used for NetBox WebUI IPAM tab objects ======== ##
vrf_name: PUB_API
vrf_rd: 65000:92062
vrf_description: "Interconnect VRF between OIaaS FW and IP Fabric Leaf SWs"
vrf_tag: oiaas



boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$
```
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$ ` ansible-playbook -i ./hosts -v main_organization.yml -e 'site_description="Orange DC in Romania, Bucharest"' ` 

### Results in Netbox WebUI > Racks page:
![Netbox ](./images/rack_image.PNG)


## 2. How to add all servers with management IPs:

boburciu@WX-5CG020BDT2: /netbox-ansible-automation$ ` cd ../parse_excel_servers/; python3 xls2iac.py; cd ../netbox-ansible-automation/ ` <br/>
boburciu@WX-5CG020BDT2: /netbox-ansible-automation$ ` ls -lt ~/parse_excel_servers/ | grep external_vars_ ` <br/>
```
-rw-rw-rw- 1 boburciu boburciu   4589 Feb  7 01:42 external_vars_BQM6Y53.yml
-rw-rw-rw- 1 boburciu boburciu   4585 Feb  7 01:42 external_vars_CQM6Y53.yml
-rw-rw-rw- 1 boburciu boburciu   4635 Feb  7 01:42 external_vars_CZ20340JGZ.yml
-rw-rw-rw- 1 boburciu boburciu   4631 Feb  7 01:42 external_vars_CZJ03404LC.yml
-rw-rw-rw- 1 boburciu boburciu   4646 Feb  7 01:42 external_vars_CZJ03501PV.yml
-rw-rw-rw- 1 boburciu boburciu   4651 Feb  7 01:42 external_vars_CZJ03501PT.yml
-rw-rw-rw- 1 boburciu boburciu   4652 Feb  7 01:42 external_vars_CZJ03501PS.yml
-rw-rw-rw- 1 boburciu boburciu   4701 Feb  7 01:42 external_vars_2102311XDB10KA000161.yml
-rw-rw-rw- 1 boburciu boburciu   4702 Feb  7 01:42 external_vars_2102311XDB10KA000151.yml
-rw-rw-rw- 1 boburciu boburciu   4718 Feb  7 01:42 external_vars_2102311XDB10KA000264.yml
-rw-rw-rw- 1 boburciu boburciu   4717 Feb  7 01:42 external_vars_2102311XDB10KA000159.yml
-rw-rw-rw- 1 boburciu boburciu   4726 Feb  7 01:42 external_vars_2102311XDB10KA000162.yml
-rw-rw-rw- 1 boburciu boburciu   4727 Feb  7 01:42 external_vars_2102311XDB10KA000168.yml
-rw-rw-rw- 1 boburciu boburciu   4753 Feb  7 01:42 external_vars_2102311XBS10K9000827.yml
-rw-rw-rw- 1 boburciu boburciu   4753 Feb  7 01:42 external_vars_2102311XBS10K9000872.yml
-rw-rw-rw- 1 boburciu boburciu   4753 Feb  7 01:42 external_vars_2102311XBS10K9000873.yml
-rw-rw-rw- 1 boburciu boburciu   4691 Feb  7 01:42 external_vars_2102311XBSN0JA000033.yml
-rw-rw-rw- 1 boburciu boburciu   4693 Feb  7 01:42 external_vars_2102311XBSN0JA000034.yml
-rw-rw-rw- 1 boburciu boburciu   4699 Feb  7 01:42 external_vars_2102311XBSN0JA000038.yml
-rw-rw-rw- 1 boburciu boburciu   4712 Feb  7 01:42 external_vars_2102311XBSN0JA000037.yml
-rw-rw-rw- 1 boburciu boburciu   4699 Feb  7 01:42 external_vars_2102311XBSN0JA000036.yml
-rw-rw-rw- 1 boburciu boburciu   4699 Feb  7 01:42 external_vars_2102311XBSN0JA000035.yml
-rw-rw-rw- 1 boburciu boburciu   4713 Feb  7 01:42 external_vars_2102311XBSN0JA000031.yml
-rw-rw-rw- 1 boburciu boburciu   4713 Feb  7 01:42 external_vars_2102311XBSN0JA000027.yml
-rw-rw-rw- 1 boburciu boburciu   4713 Feb  7 01:42 external_vars_2102311XBSN0JA000032.yml
-rw-rw-rw- 1 boburciu boburciu   4728 Feb  7 01:42 external_vars_2102311XBS10JC000068.yml
-rw-rw-rw- 1 boburciu boburciu   4698 Feb  7 01:42 external_vars_2102311XBS10JC000070.yml
-rw-rw-rw- 1 boburciu boburciu   4699 Feb  7 01:42 external_vars_2102311XBSN0JA000030.yml
-rw-rw-rw- 1 boburciu boburciu   4698 Feb  7 01:42 external_vars_2102311XBSN0JA000028.yml
-rw-rw-rw- 1 boburciu boburciu   4699 Feb  7 01:42 external_vars_2102311XBSN0JA000029.yml
-rw-rw-rw- 1 boburciu boburciu   4762 Feb  7 01:42 external_vars_CZ28410LW5.yml
-rw-rw-rw- 1 boburciu boburciu   4764 Feb  7 01:42 external_vars_CZ28410LW7.yml
-rw-rw-rw- 1 boburciu boburciu   4762 Feb  7 01:42 external_vars_CZ28410LW6.yml
-rw-rw-rw- 1 boburciu boburciu   4731 Feb  7 01:42 external_vars_CZJ73516QP.yml
-rw-rw-rw- 1 boburciu boburciu   4746 Feb  7 01:42 external_vars_CZJ73516QN.yml
-rw-rw-rw- 1 boburciu boburciu   4813 Feb  7 01:42 external_vars_CZJ70503GN.yml
-rw-rw-rw- 1 boburciu boburciu   4813 Feb  7 01:42 external_vars_CZJ70503GM.yml
-rw-rw-rw- 1 boburciu boburciu   4813 Feb  7 01:42 external_vars_CZJ70503GL.yml
-rw-rw-rw- 1 boburciu boburciu   4798 Feb  7 01:42 external_vars_CZJ701089K.yml
-rw-rw-rw- 1 boburciu boburciu   4801 Feb  7 01:42 external_vars_CZJ701089M.yml
-rw-rw-rw- 1 boburciu boburciu   4799 Feb  7 01:42 external_vars_CZJ73516PH.yml
-rw-rw-rw- 1 boburciu boburciu   4799 Feb  7 01:42 external_vars_CZJ73516PJ.yml
-rw-rw-rw- 1 boburciu boburciu   4799 Feb  7 01:42 external_vars_CZJ73516PL.yml
-rw-rw-rw- 1 boburciu boburciu   4799 Feb  7 01:42 external_vars_CZJ73516PK.yml
-rw-rw-rw- 1 boburciu boburciu   4879 Feb  7 01:42 external_vars_CZ28410LW1.yml
-rw-rw-rw- 1 boburciu boburciu   4879 Feb  7 01:42 external_vars_CZ28410LW3.yml
-rw-rw-rw- 1 boburciu boburciu   4879 Feb  7 01:42 external_vars_CZ28410LW4.yml
-rw-rw-rw- 1 boburciu boburciu   4879 Feb  7 01:42 external_vars_CZ28410LW2.yml
-rw-rw-rw- 1 boburciu boburciu   4878 Feb  7 01:42 external_vars_CZ28410LW0.yml
-rw-rw-rw- 1 boburciu boburciu   4854 Feb  7 01:42 external_vars_CZ273609YH.yml
-rw-rw-rw- 1 boburciu boburciu   4861 Feb  7 01:42 external_vars_CZ273609YJ.yml
-rw-rw-rw- 1 boburciu boburciu   4866 Feb  7 01:42 external_vars_CZ270203QV.yml
-rw-rw-rw- 1 boburciu boburciu   4869 Feb  7 01:42 external_vars_CZ270203QR.yml
-rw-rw-rw- 1 boburciu boburciu   4861 Feb  7 01:42 external_vars_CZ270203QN.yml
-rw-rw-rw- 1 boburciu boburciu   4861 Feb  7 01:42 external_vars_CZ270203QW.yml
-rw-rw-rw- 1 boburciu boburciu   4876 Feb  7 01:42 external_vars_CZ270203QS.yml
-rw-rw-rw- 1 boburciu boburciu   4885 Feb  7 01:42 external_vars_CZ273609YL.yml
-rw-rw-rw- 1 boburciu boburciu   4876 Feb  7 01:42 external_vars_CZ273609YM.yml
-rw-rw-rw- 1 boburciu boburciu   4883 Feb  7 01:42 external_vars_CZ273609YK.yml
-rw-rw-rw- 1 boburciu boburciu   4594 Feb  7 01:42 external_vars_CZ00CHASSIS2.yml
-rw-rw-rw- 1 boburciu boburciu   4874 Feb  7 01:42 external_vars_CZ3350WDY8.yml
-rw-rw-rw- 1 boburciu boburciu   4896 Feb  7 01:42 external_vars_CZ20180MMF.yml
-rw-rw-rw- 1 boburciu boburciu   4896 Feb  7 01:42 external_vars_CZ20180MMD.yml
-rw-rw-rw- 1 boburciu boburciu   4866 Feb  7 01:42 external_vars_CZ3350WDY2.yml
-rw-rw-rw- 1 boburciu boburciu   4866 Feb  7 01:42 external_vars_CZ28250494.yml
-rw-rw-rw- 1 boburciu boburciu   4866 Feb  7 01:42 external_vars_CZ28250493.yml
-rw-rw-rw- 1 boburciu boburciu   4872 Feb  7 01:42 external_vars_CZ28250491.yml
-rw-rw-rw- 1 boburciu boburciu   4872 Feb  7 01:42 external_vars_CZ28250492.yml
-rw-rw-rw- 1 boburciu boburciu   4861 Feb  7 01:42 external_vars_CZ270203QT.yml
-rw-rw-rw- 1 boburciu boburciu   4860 Feb  7 01:42 external_vars_CZ270203QM.yml
-rw-rw-rw- 1 boburciu boburciu   4852 Feb  7 01:42 external_vars_CZ270203QX.yml
-rw-rw-rw- 1 boburciu boburciu   4861 Feb  7 01:42 external_vars_CZ270203QQ.yml
-rw-rw-rw- 1 boburciu boburciu   4594 Feb  7 01:42 external_vars_CZ00CHASSIS1.yml
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$
```
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$ ` for i in `ls -lt ~/parse_excel_servers/ | grep external_vars_ | awk '{print $9}'`; do echo ""; echo ""; echo "***** running playbook for variables in $i *****"; echo ""; echo ""; echo ""; ansible-playbook -i ./hosts create_device_wMgmtIntIP_inRack_inTenant_inRack_inSite.yml -e "external_vars='../parse_excel_servers/$i' -v"; done `  <br/>

### To add only part of IaC list:
 boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$ ` ls -lX /home/boburciu/parse_excel_servers/external_vars*  | awk '{print $9}'  | cat -n | tail -36 `
 ```
    51  /home/boburciu/parse_excel_servers/external_vars_DL360_Gen9_CZJ73516QN.yml
    52  /home/boburciu/parse_excel_servers/external_vars_DL360_Gen9_CZJ73516QP.yml
    53  /home/boburciu/parse_excel_servers/external_vars_DL360_gen10_CZJ03404LC.yml
    54  /home/boburciu/parse_excel_servers/external_vars_DL360_gen10_CZJ03501PS.yml
    55  /home/boburciu/parse_excel_servers/external_vars_DL360_gen10_CZJ03501PT.yml
    56  /home/boburciu/parse_excel_servers/external_vars_DL360_gen10_CZJ03501PV.yml
    57  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen10_CZ28410LW5.yml
    58  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen10_CZ28410LW6.yml
    59  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen10_CZ28410LW7.yml
    60  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen9_CZJ701089K.yml
    61  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen9_CZJ701089M.yml
    62  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen9_CZJ70503GL.yml
    63  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen9_CZJ70503GM.yml
    64  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen9_CZJ70503GN.yml
    65  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen9_CZJ73516PH.yml
    66  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen9_CZJ73516PJ.yml
    67  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen9_CZJ73516PK.yml
    68  /home/boburciu/parse_excel_servers/external_vars_DL380_Gen9_CZJ73516PL.yml
    69  /home/boburciu/parse_excel_servers/external_vars_DL380_gen10_CZ20340JGZ.yml
    70  /home/boburciu/parse_excel_servers/external_vars_Dell_R640_CQM6Y53.yml
    71  /home/boburciu/parse_excel_servers/external_vars_Dell_R740_BQM6Y53.yml
    72  /home/boburciu/parse_excel_servers/external_vars_EX1_SWJ-OOB-R1.yml
    73  /home/boburciu/parse_excel_servers/external_vars_Fortigate1.yml
    74  /home/boburciu/parse_excel_servers/external_vars_Fortigate2.yml
    75  /home/boburciu/parse_excel_servers/external_vars_HP_c7000_Chassis1.yml
    76  /home/boburciu/parse_excel_servers/external_vars_HP_c7000_Chassis2.yml
    77  /home/boburciu/parse_excel_servers/external_vars_MX1-RE0.yml
    78  /home/boburciu/parse_excel_servers/external_vars_MX2-RE0.yml
    79  /home/boburciu/parse_excel_servers/external_vars_NE40E.yml
    80  /home/boburciu/parse_excel_servers/external_vars_QFX1.yml
    81  /home/boburciu/parse_excel_servers/external_vars_QFX2.yml
    82  /home/boburciu/parse_excel_servers/external_vars_SRX_1.yml
    83  /home/boburciu/parse_excel_servers/external_vars_SRX_2.yml
    84  /home/boburciu/parse_excel_servers/external_vars_SWH-OoB-R1.yml
    85  /home/boburciu/parse_excel_servers/external_vars_SWH-TOR-R2-1.yml
    86  /home/boburciu/parse_excel_servers/external_vars_SWH-TOR-R2-2.yml
```    
boburciu@WX-5CG020BDT2: /netbox-ansible-automation$  ` for x in ` ls -lX /home/boburciu/parse_excel_servers/external_vars*  | awk '{print $9}'  | cat | tail -36  `; do echo ""; echo ""; echo "@@@@@ running Device creation playbooks for extra-vars in $x @@@@@"; echo ""; echo ""; echo ""; ansible-playbook -i ./hosts -v add_device_w_mgmt.yml -e "external_vars=$x"; done `


boburciu@WX-5CG020BDT2: /netbox-ansible-automation$ ` ansible-playbook -i ./hosts -v create_device_wMgmtIntIP_inRack_inTenant_inRack_inSite.yml -e "external_vars=/home/boburciu/parse_excel_servers/external_vars_SRX_2.yml" `

## 3. How to integrate NAPALM with Containerized NetBox, to allow for real-time collecting of facts in NetBox, from its network devices objects, based on [netbox-docker guide](https://github.com/netbox-community/netbox-docker/wiki/NAPALM-Configuration):
[root@NetboX netbox-docker]# ` vi /root/projects/netbox-docker/env/netbox.env `
[root@NetboX netbox-docker]# ` cat /root/projects/netbox-docker/env/netbox.env | grep NAPALM `
```  
NAPALM_USERNAME=orangeoln
NAPALM_PASSWORD=l0c@l@dm1n
NAPALM_TIMEOUT=10
[root@NetboX netbox-docker]#
```  
[root@NetboX netbox-docker]# ` pip3 install napalm `
[root@NetboX netbox-docker]# ` pip3 install napalm-ce `
[root@NetboX netbox-docker]# ` docker-compose restart `
```  
Restarting netbox-docker_nginx_1         ... done
Restarting netbox-docker_netbox_1        ... done
Restarting netbox-docker_netbox-worker_1 ... done
Restarting netbox-docker_redis-cache_1   ... done
Restarting netbox-docker_postgres_1      ... done
Restarting netbox-docker_redis_1         ... done
[root@NetboX netbox-docker]#
``` 

### How to check if a NAPALM driver is installed in NetBox
[root@NetboX netbox-docker]# ` docker-compose run --rm --entrypoint /bin/bash netbox `
``` 
Creating netbox-docker_netbox_run ... done
``` 
bash-5.0$ ` ./manage.py nbshell `
``` 
🧬 loaded config '/etc/netbox/config/configuration.py'
🧬 loaded config '/etc/netbox/config/configuration.py'
🧬 loaded config '/etc/netbox/config/extra.py'
### NetBox interactive shell (d9fceee54b53)
### Python 3.9.1 | Django 3.1.3 | NetBox 2.10.3
### lsmodels() will show available models. Use help(<model>) for more info.
>>> 
>>>
>>> import napalm
>>> driver=napalm.get_network_driver("ce")
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/local/lib/python3.9/site-packages/napalm/base/__init__.py", line 97, in get_network_driver
    raise ModuleImportError(
napalm.base.exceptions.ModuleImportError: Cannot import "ce". Is the library installed?
>>> exit()
bash-5.0$ exit
exit
[root@NetboX netbox-docker]#
``` 

### How to rebuild image from the _netboxcommunity/netbox:latest_ in Docker Hub, while adding napalm-driver in Dockerfile
[root@NetboX netbox-docker]# ` vi Dockerfile `
[root@NetboX netbox-docker]# ` diff Dockerfile Dockerfile.bkp `
```
26d25
<       napalm-ce \
79c78
< RUN chmod -R g+w static media
---
> RUN mkdir static && chmod -R g+w static media
[root@NetboX netbox-docker]#

```
[root@NetboX netbox-docker]# ` mkdir .netbox `
[root@NetboX netbox-docker]# ` touch .netbox/requirements.txt `
[root@NetboX netbox-docker]# ` cat .netbox/requirements.txt `
```
napalm==3.2.0
napalm-ce==0.2.0
ruamel.yaml==0.16.13
django-auth-ldap==2.3.0
django-storages[azure,boto3,dropbox,google,libcloud,sftp]==1.11.1
[root@NetboX netbox-docker]#
```
[root@NetboX netbox-docker]# ` docker image build . --tag netbox:napalm --build-arg FROM=netboxcommunity/netbox:latest --build-arg NETBOX_PATH=".netbox" `
```
Sending build context to Docker daemon  158.7kB
Step 1/30 : ARG FROM
:

Successfully built 3ab20b99381c
Successfully tagged netbox:napalm
[root@NetboX netbox-docker]# [root@NetboX netbox-docker]# docker image ls
REPOSITORY               TAG           IMAGE ID       CREATED          SIZE
netbox                   napalm        3ab20b99381c   45 seconds ago   336MB
postgres                 12-alpine     7ec50832fed0   8 weeks ago      159MB
redis                    6-alpine      933c79ea2511   2 months ago     31.6MB
netboxcommunity/netbox   latest        8e452c542927   2 months ago     229MB
nginx                    1.19-alpine   629df02b47c8   3 months ago     22.3MB
[root@NetboX netbox-docker]#
```
[root@NetboX netbox-docker]# ` cp docker-compose.yml docker-compose.yml.bkp `
[root@NetboX netbox-docker]# ` vi docker-compose.yml `
[root@NetboX netbox-docker]# ` diff docker-compose.yml docker-compose.yml.bkp `
```
4c4
<     image: netbox:napalm
---
>     image: netboxcommunity/netbox:${VERSION-latest}
[root@NetboX netbox-docker]#
```
[root@NetboX netbox-docker]# ` docker-compose ps `
```
Name   Command   State   Ports
------------------------------
[root@NetboX netbox-docker]#
```
[root@NetboX netbox-docker]# ` docker-compose up `
```
Creating network "netbox-docker_default" with the default driver
Creating netbox-docker_redis-cache_1   ... done
Creating netbox-docker_postgres_1    ... done
Creating netbox-docker_redis_1       ... done
Creating netbox-docker_netbox-worker_1 ... done
Creating netbox-docker_netbox_1        ... done
Creating netbox-docker_nginx_1         ... done
Attaching to netbox-docker_postgres_1, netbox-docker_redis_1, netbox-docker_redis-cache_1, netbox-docker_netbox-worker_1, netbox-docker_netbox_1, netbox-docker_nginx_1

```
[root@NetboX netbox-docker]# ` docker-compose ps `
```
            Name                           Command               State                           Ports
------------------------------------------------------------------------------------------------------------------------------
netbox-docker_netbox-worker_1   python3 /opt/netbox/netbox ...   Up
netbox-docker_netbox_1          /opt/netbox/docker-entrypo ...   Up
netbox-docker_nginx_1           /docker-entrypoint.sh ngin ...   Up      80/tcp,
                                                                         0.0.0.0:8001->8080/tcp,0.0.0.0:49154->8080/tcp
netbox-docker_postgres_1        docker-entrypoint.sh postgres    Up      5432/tcp
netbox-docker_redis-cache_1     docker-entrypoint.sh sh -c ...   Up      6379/tcp
netbox-docker_redis_1           docker-entrypoint.sh sh -c ...   Up      6379/tcp
[root@NetboX netbox-docker]# 
```
[root@NetboX netbox-docker]# ` docker ps `
```
CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS         PORTS                                                     NAMES
055cd02cd6a0   nginx:1.19-alpine    "/docker-entrypoint.…"   3 minutes ago   Up 3 minutes   80/tcp, 0.0.0.0:8001->8080/tcp, 0.0.0.0:49154->8080/tcp   netbox-docker_nginx_1
e541d6a00f8e   netbox:napalm        "/opt/netbox/docker-…"   3 minutes ago   Up 3 minutes                                                             netbox-docker_netbox_1
441f071d94dd   netbox:napalm        "python3 /opt/netbox…"   3 minutes ago   Up 3 minutes                                                             netbox-docker_netbox-worker_1
4c3c5d0de41d   redis:6-alpine       "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes   6379/tcp                                                  netbox-docker_redis_1
8bea76d9a0dd   postgres:12-alpine   "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes   5432/tcp                                                  netbox-docker_postgres_1
5fff97d26517   redis:6-alpine       "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes   6379/tcp                                                  netbox-docker_redis-cache_1
[root@NetboX netbox-docker]#
```