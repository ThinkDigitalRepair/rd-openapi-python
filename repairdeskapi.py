"""python wrapper for RepairDesk OpenAPI"""
import json
import requests
import objects

# script-wide variables
base_url = "https://api.repairdesk.co/api/web/v1/"
api_key, api_key_string = "", ""
customers = []


# sample_url https://api.repairdesk.co/api/web/v1/customers?api_key=YOUR_KEY

def set_api_key(key):
    # type: (str) -> bool
    """

    :type key: str
    :rtype: bool
    """
    global api_key, api_key_string
    api_key = key
    api_key_string = "?api_key=" + api_key
    return True


def get_api_key(self):
    return self.api_key


def get_customers():
    # type: () -> list[]
    """Returns a list of only the customers in the JSON string.
    :rtype: list
    """
    url = base_url + "customers" + api_key_string
    customer_list = requests.get(url)
    # print(list(customers.json().values())[1])
    for c in list(customer_list.json().values())[1]:
        customers.append(objects.Customer(c))
    return customers
