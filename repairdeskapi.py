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
    """Returns a list of only the customers in the JSON string"""
    url = base_url + "customers" + api_key_string
    customers = requests.get(url)
    return list(customers.json().values())[3]

class Customer(object):
    """A customer in the RD System:
    Attributes are :
                    fullName
cid
phone
mobile
address1
address2
postcode
city
state
country
email
organization
refered_by
driving_licence
contact_person
tax_number
network
    """
#todo: Create attributes for each value
    def __init__(self, name):
        self.name = name

    def say_name(self):
        print(self.name)
