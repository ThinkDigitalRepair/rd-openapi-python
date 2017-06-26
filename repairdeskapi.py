"""python wrapper for RepairDesk OpenAPI"""
import json
import requests

#scriptwide variables
base_url="https://api.repairdesk.co/api/web/v1/"

#sample_url https://api.repairdesk.co/api/web/v1/customers?api_key=YOUR_KEY

def set_api_key(key):
    global api_key
    global api_key_string
    api_key = key
    api_key_string = "?api_key=" + api_key
    return True

def get_api_key():
    return api_key

def get_customers():
    url = base_url + "customers" + api_key_string
    customers = requests.get(url)
    return customers

class Customer(object):
    """A customer in the RD System"""

    def __init__(self, name):
        self.name = name

    def say_name(self):
        print(self.name)
