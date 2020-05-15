#! /usr/bin/env python

import requests
from getpass import getpass
import json

# Step 1: Authenticate into APIC and set up session for api calls

s = requests.sessions()

print("Let's set up the lab now.")
print('Enter the IP address of the APIC:')
apic = input()
user = getpass('Enter your APIC username:')
password = getpass('Enter your APIC password now:')

url = "https://%s/api/aaaLogin.json" % (apic)

payload = "{\r\n\t\"aaaUser\":{\r\n\t\t\"attributes\":{\r\n\t\t\t\"name\": \"%s\",\r\n\t\t\t\"pwd\":\"%s\"\r\n\t\t}\r\n\t}\r\n}" % (user, password)
headers = {
    'Content-Type': 'application/json'
}

response = s.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))