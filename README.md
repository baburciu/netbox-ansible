# netbox-ansible
## Ansible playbooks usage for Netbox automation, based on Galaxy collection https://docs.ansible.com/ansible/latest/collections/netbox/netbox/.

## 0. How to install Ansible Galaxy collection to correct path:

boburciu@WX-5CG020BDT2:~$ ` ansible-config list | grep COLLECTIONS_PATHS -C1 ` # verify default location for the collections, so that the new modules can be read by Ansible cfg
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
boburciu@WX-5CG020BDT2:~$ ` ansible-galaxy collection install netbox.netbox --collections-path ~/.ansible/collections ` # installing the collection of roles in proper location

## 1. How to add/remove NetBox WebUI Organization tab objects:
boburciu@WX-5CG020BDT2: ~$ ` cd ~/netbox-ansible-automation ` <br/>
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$  <br/>
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$ ` cat external_vars.yml `  <br/>
```
---
# external_vars.yml to be used in playbooks called in order by import_playbook

url_var: "http://192.168.200.23:8001/"
token_var: "97dab58500f94c141d63fb78b6406f9b53a119ac"

## ======== variables used for NetBox WebUI Organization tab objects ======== ##
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

##  ======== variables used for NetBox WebUI IPAM tab objects ======== ##
vrf_name: PUB_API
vrf_rd: 65000:92062
vrf_description: "Interconnect VRF between OIaaS FW and IP Fabric Leaf SWs"
vrf_tag: oiaas



boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$
```
boburciu@WX-5CG020BDT2:~/netbox-ansible-automation$ ` ansible-playbook -i ./hosts -v main_organization.yml -e 'site_description="Orange DC in Romania, Bucharest"' ` 

### Results in Netbox WebUI > Racks page:
![Netbox ](./images/rack_image.PNG)