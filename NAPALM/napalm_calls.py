import napalm
driver=napalm.get_network_driver("dellos10")
device=driver(hostname="192.168.70.4", username="admin", password="admin")
device.open()
cmd = "show running-configuration | grep vlan | grep interface"
vlancfg = device.cli([cmd])[cmd]
untagged_vlan_id=None
tagged_vlan_list=[]

device_interfaces = device.get_interfaces()
device_interfaces.keys()
device_interfaces['ethernet1/1/8:1']

cmd = "show running-configuration interface ethernet1/1/1:1"
ifcfg = device.cli([cmd])[cmd]

-------------------
import napalm
driver=napalm.get_network_driver("ce")
device=driver(hostname="192.168.201.24", username="orangeoln", password="l0c@l@dm1n")
device.open()
cmd = "display current-configuration interface 10GE1/0/1"
ifcfg = device.cli([cmd])[cmd]
untagged_vlan_id=None
tagged_vlan_list=[]


if "undo port default vlan" in ifcfg:
    ifcfg = ifcfg.replace("undo port default vlan", "dummy text")

if "port default vlan" in ifcfg:
    untagged_vlan_id = ifcfg.split(" port default vlan ")[1].split("\n", 2)[0]
    dot1q_mode = "Access"  

if "undo port trunk allow-pass vlan" in ifcfg:
    ifcfg=ifcfg.replace("undo port trunk allow-pass vlan", "dummy text")    

if "port trunk allow-pass vlan" in ifcfg:
    ifcfg_tagged_vlan_list = ifcfg.split(" port trunk allow-pass vlan ")[1].split("\n", 2)[0]
    dot1q_mode = "Tagged"
    if "to" in ifcfg_tagged_vlan_list:
        # add to the list of passed VLANs the ones prior to VLAN range (x y in "port trunk allow-pass vlan x y z to zz tt uu")
        tagged_vlan_list.extend(ifcfg_tagged_vlan_list.split(" to ")[0].rsplit(" ")[0:-1])
        # for the range, append the elements of it
        tagged_vlan_list.extend( list( range( int(ifcfg_tagged_vlan_list.split(" to ")[0].rsplit(" ")[-1]),
              int(ifcfg_tagged_vlan_list.split(" to ")[1].rsplit(" ")[0]) + 1) ) )
        # add to the list of passed VLANs the ones following the VLAN range (tt uu)
        tagged_vlan_list.extend(ifcfg_tagged_vlan_list.split(" to ")[1].rsplit(" ")[1:])
    else:
        tagged_vlan_list = (ifcfg.split(" port trunk allow-pass vlan ")[1].split("\n", 2)[0] ).split(" ")

# create the VLANs in NetBox
# if tagged_vlan_list.append(untagged_vlan_id):
#     for vlan in tagged_vlan_list.append(untagged_vlan_id):
#         print(f"******* Now we'll create NetBox VLAN object for VID={vlan}")

if tagged_vlan_list:
    if untagged_vlan_id:
        for vlan in tagged_vlan_list.append(untagged_vlan_id):
            print(f"******* Now we'll create NetBox VLAN object for VID={vlan}")
    else:
        for vlan in tagged_vlan_list:
            print(f"******* Now we'll create NetBox VLAN object for VID={vlan}")
else:
    if untagged_vlan_id:
        print(f"******* Now we'll create NetBox VLAN object for VID={untagged_vlan_id}")    

if "to" in vlancfg_vlan_list:
    # add to the list of passed VLANs the ones prior to VLAN range (x y in "port trunk allow-pass vlan x y z to zz tt uu")
    device_vlan_list.extend(vlancfg_vlan_list.split(" to ")[0].rsplit(" ")[0:-1])
    # for the range, append the elements of it
    device_vlan_list.extend( list( range( int(vlancfg_vlan_list.split(" to ")[0].rsplit(" ")[-1]),
          int(vlancfg_vlan_list.split(" to ")[1].rsplit(" ")[0]) + 1 ) ) )
    # add to the list of passed VLANs the ones following the VLAN range (tt uu)
    device_vlan_list.extend(vlancfg_vlan_list.split(" to ")[1].rsplit(" ")[1:])
else:
    device_vlan_list = vlancfg_vlan_list.split(" ")        