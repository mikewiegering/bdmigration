#! /user/bin/env python

import requests
from getpass import getpass
import csv

# Set up the variables

with open("ACI PostMan Variable Values.csv",  encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:        
        print(row)

print("Let's configure the subnets on the Old BD")
print("First Let's log in")
print('What is the ip address of the APIC?')
apic = input()
user = getpass('What is you username?')
password = getpass('What is your password?')
print('whats the name of the tenant?')
tenant = input()
print('what is the name of the app profile?')
app_profile = input()
print('what is the name of the old BD?')
old_bd = input()
print('what is the name of the network?')
subnet_network = input()
print('what is the name of the network IP?')
subnet_ip = input()
print('what is the name of the netmask?')
subnet_mask = input()
print('what is the name of the epg?')
epg = input()


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

# Create Subnets under Old BD

url = "https://%s/api/node/mo/uni/tn-%s/BD-%s/subnet-[%s.%s/%s].json" % (apic, tenant, old_bd, subnet_network, subnet_ip, subnet_mask)

payload = "{\"fvSubnet\":{\"attributes\":{\"dn\":\"uni/tn-%s/BD-%s/subnet-[%s.%s/%s]\",\"ip\":\"%s.%s/%s\",\"scope\":\"public\",\"rn\":\"subnet-[%s.%s/%s]\",\"status\":\"created\"},\"children\":[]}}\r\n" % (tenant, old_bd, subnet_network, subnet_ip, subnet_mask, subnet_network, subnet_ip, subnet_mask, subnet_network, subnet_ip, subnet_mask)
headers = {
    'Content-Type': 'application/json'
}

response = s.request("POST", url, headers=headers, data = payload, verify = False)

print(response.text.encode('utf8'))

# create EPG's for demo

url = "https://%s/api/node/mo/uni/tn-%s/ap-%s/epg-%s.json" % (apic, tenant, app_profile, epg)

payload = "{\"fvAEPg\":{\"attributes\":{\"dn\":\"uni/tn-%s/ap-%s/epg-%s\",\"name\":\"%s\",\"rn\":\"%s\",\"status\":\"created\"},\"children\":[{\"fvRsBd\":{\"attributes\":{\"tnFvBDName\":\"%s\",\"status\":\"created,modified\"},\"children\":[]}}]}}\r\n" % (tenant, app_profile, epg, epg, epg, old_bd)
headers = {
    'Content-Type': 'application/json'
}

response = s.request("POST", url, headers=headers, data = payload, verify = False)

print(response.text.encode('utf8'))

