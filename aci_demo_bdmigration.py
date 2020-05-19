#! /user/bin/env python

import requests
from getpass import getpass
import csv

# Set up the variables

print("Let's migrate our VLAN's to new BD's now")
print("First Let's log in")
print('What is the ip address of the APIC?')
apic = input()
user = getpass('What is you username?')
password = getpass('What is your password?')

# pull in the CSV file and loop through the scripts

with open("ACI PostMan Variable Values.csv",  encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    line_count = 0
    for row in reader:
        if line_count == 0:
            print(f'The variables for this script are {",".join(row)}')
            line_count += 1

        # let's set the variable values using the csv file dictionary    
        print(f'the name of the tenant is {row["tenant"]}')
        tenant = row["tenant"]
        print(f'the name of the app profile is {row["app_profile"]}')
        app_profile = row["app_profile"]
        print(f'the name of the old BD is {row["old_bd"]}')
        old_bd = row["old_bd"]
        print(f'the name of the new BD is {row["new_bd"]}')
        new_bd = row["new_bd"]
        print(f'the name of the network is {row["subnet_network"]}')
        subnet_network = row["subnet_network"]
        print(f'the name of the network IP is {row["subnet_ip"]}')
        subnet_ip = row["subnet_ip"]
        print(f'the name of the netmask is {row["subnet_mask"]}')
        subnet_mask = row["subnet_mask"]
        print(f'the name of the epg is {row["epg"]}')
        epg = row["epg"]
        print(f'the name of the vrf is {row["vrf"]}')
        vrf = row["vrf"]
        line_count += 1

        # set session persistance for all the API calls

        s = requests.session()    

        # first call to authenticate into the apic

        url = "https://%s/api/aaaLogin.json" % (apic)

        payload = "{\r\n\t\"aaaUser\":{\r\n\t\t\"attributes\":{\r\n\t\t\t\"name\": \"%s\",\r\n\t\t\t\"pwd\":\"%s\"\r\n\t\t}\r\n\t}\r\n}" % (user, password)
        headers = {
            'Content-Type': 'application/json'
        }

        response = s.request("POST", url, headers=headers, data = payload, verify = False)

        print(response.text.encode('utf8'))

        # Create the "new" Bridge Domain

        
        url = "https://%s/api/node/mo/uni/tn-%s/BD-%s.json" % (apic, tenant, new_bd)

        payload = "{\n    \"fvBD\": {\n        \"attributes\": {\n            \"dn\": \"uni/tn-%s/BD-%s\",\n            \"name\": \"%s\",\n            \"rn\": \"BD-%s\",\n            \"status\": \"created\"\n        },\n        \"children\": [\n            {\n                \"fvRsCtx\": {\n                    \"attributes\": {\n                        \"tnFvCtxName\": \"%s\",\n                        \"status\": \"created,modified\"\n                    },\n                    \"children\": []\n                }\n            },\n            {\n                \"fvRsIgmpsn\": {\n                    \"attributes\": {\n                        \"tnIgmpSnoopPolName\": \"default\",\n                        \"status\": \"created,modified\"\n                    },\n                    \"children\": []\n                }\n            }\n        ]\n    }\n}" % (tenant, new_bd, new_bd, new_bd, vrf)
        headers = {
            'Content-Type': 'application/json'
        }

        response = s.request("POST", url, headers=headers, data = payload, verify = False)

        print(response.text.encode('utf8'))

        # create a new subnet on the new Bridge Domain

        url = "https://%s/api/node/mo/uni/tn-%s/BD-%s/subnet-[%s.%s/%s].json" % (apic, tenant, new_bd, subnet_network, subnet_ip, subnet_mask)

        payload = "{\"fvSubnet\":{\"attributes\":{\"dn\":\"uni/tn-%s/BD-%s/subnet-[%s.%s/%s]\",\"ip\":\"%s.%s/%s\",\"scope\":\"public\",\"rn\":\"subnet-[%s.%s/%s]\",\"status\":\"created\"},\"children\":[]}}\r\n" % (tenant, new_bd, subnet_network, subnet_ip, subnet_mask, subnet_network, subnet_ip, subnet_mask, subnet_network, subnet_ip, subnet_mask)
        headers = {
            'Content-Type': 'application/json'
        }

        response = s.request("POST", url, headers=headers, data = payload, verify = False)

        print(response.text.encode('utf8'))

        # Migrate the EPG to register to the new Bridge Domain

        url = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s/rsbd.json" % (apic, tenant, app_profile, epg)

        payload = "{\"fvRsBd\":{\"attributes\":{\"tnFvBDName\":\"%s\"},\"children\":[]}}" % (new_bd)
        headers = {
            'Content-Type': 'application/json'
        }

        response = s.request("POST", url, headers=headers, data = payload, verify = False)

        print(response.text.encode('utf8'))

        # Delete the old subnet from the "Old" Bridge Domain

        url = "https://%s/api/node/mo/uni/tn-%s/BD-%s.json" % (apic, tenant, old_bd)

        payload = "{\"fvBD\":{\"attributes\":{\"dn\":\"uni/tn-%s/BD-%s\",\"status\":\"modified\"},\"children\":[{\"fvSubnet\":{\"attributes\":{\"dn\":\"uni/tn-%s/BD-%s/subnet-[%s.%s/%s]\",\"status\":\"deleted\"},\"children\":[]}}]}}\r\n" % (tenant, old_bd, tenant, old_bd, subnet_network, subnet_ip, subnet_mask)
        headers = {
            'Content-Type': 'application/json'
        }

        response = s.request("POST", url, headers=headers, data = payload, verify = False)

        print(response.text.encode('utf8'))