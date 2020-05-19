#! /usr/bin/env python

import requests
from getpass import getpass
import csv


# Setup the base lab variables



print("Let's set up the Lab for the Demo now.")
print('What is the IP address of the APIC?')
apic = input()
user = getpass('what is your apic username?')
password = getpass('what is your apic password?')
tenant = 'bdtest'
vrf = 'test_vrf_1'
app_profile = 'access'
old_bd = 'old_bd'



# set session persistance for all api calls in this file
s = requests.session()

# first call is to authenticate into the apic

url = "https://%s/api/aaaLogin.json" % (apic)

payload = "{\n    \"aaaUser\": {\n        \"attributes\": {\n            \"name\": \"%s\",\n            \"pwd\": \"%s\"\n        }\n    }\n}" % (user, password)
    
headers = {
      'Content-Type': 'application/json'
    }

response = s.request("POST", url, headers=headers, data = payload, verify = False)
    
print(response.text.encode('utf8'))

# create a new tenant



url = "https://192.168.2.149/api/node/mo/uni/tn-%s.json" % (tenant)

payload = "{\n    \"fvTenant\": {\n        \"attributes\": {\n            \"dn\": \"uni/tn-%s\",\n            \"name\": \"%s\",\n            \"rn\": \"tn-%s\",\n            \"status\": \"created\"\n        },\n        \"children\": []\n    }\n}" % (tenant, tenant, tenant)
headers = {
    'Content-Type': 'application/json'
}

response = s.request("POST", url, headers=headers, data = payload, verify = False)

print(response.text.encode('utf8'))

# create an app profile

url = "https://%s/api/node/mo/uni/tn-%s/ap-%s.json" % (apic, tenant, app_profile)

payload = "{\n    \"fvAp\": {\n        \"attributes\": {\n            \"dn\": \"uni/tn-%s/ap-%s\",\n            \"name\": \"%s\",\n            \"rn\": \"ap-%s\",\n            \"status\": \"created\"\n        },\n        \"children\": []\n    }\n}" % (tenant, app_profile, app_profile, app_profile)
headers = {
    'Content-Type': 'application/json'
}

response = s.request("POST", url, headers=headers, data = payload, verify = False)

print(response.text.encode('utf8'))

# create a vrf

url = "https://%s/api/node/mo/uni/tn-%s/ctx-%s.json" % (apic, tenant, vrf)

payload = "{\n    \"fvCtx\": {\n        \"attributes\": {\n            \"dn\": \"uni/tn-%s/ctx-%s\",\n            \"name\": \%s\",\n            \"rn\": \"ctx-%s\",\n            \"status\": \"created\"\n        },\n        \"children\": []\n    }\n}" % (tenant, vrf, vrf, vrf)
headers = {
    'Content-Type': 'application/json'
}

response = s.request("POST", url, headers=headers, data = payload, verify = False)

print(response.text.encode('utf8'))

# create OLD BD

url = "https://%s/api/node/mo/uni/tn-%s/BD-%s.json" % (apic, tenant, old_bd)

payload = "{\n    \"fvBD\": {\n        \"attributes\": {\n            \"dn\": \"uni/tn-%s/BD-%s\",\n            \"name\": \"%s\",\n            \"rn\": \"BD-%s\",\n            \"status\": \"created\"\n        },\n        \"children\": [\n            {\n                \"fvRsCtx\": {\n                    \"attributes\": {\n                        \"tnFvCtxName\": \"%s\",\n                        \"status\": \"created,modified\"\n                    },\n                    \"children\": []\n                }\n            },\n            {\n                \"fvRsIgmpsn\": {\n                    \"attributes\": {\n                        \"tnIgmpSnoopPolName\": \"default\",\n                        \"status\": \"created,modified\"\n                    },\n                    \"children\": []\n                }\n            }\n        ]\n    }\n}" % (tenant, old_bd, old_bd, old_bd, vrf)
headers = {
    'Content-Type': 'application/json'
}

response = s.request("POST", url, headers=headers, data = payload, verify = False)

print(response.text.encode('utf8'))

