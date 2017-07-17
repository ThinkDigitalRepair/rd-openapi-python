"""python wrapper for RepairDesk OpenAPI"""
import json
import requests
import objects
import logging as log
from pathlib import Path

ticketfile = "ticketfile.json"

log.basicConfig(filename='log.log',
                format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', \
                datefmt='%d-%m-%Y:%H:%M:%S', \
                level=log.DEBUG)

# script-wide variables
base_url = "https://api.repairdesk.co/api/web/v1/"
api_key, api_key_string = "", ""
customers = []
tickets = []


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
    """Returns a list of only the customers in the JSON string.
    :rtype: list
    """
    url = base_url + "customers" + api_key_string
    customer_list = requests.get(url)
    log.info(customer_list)

    customer_list = customer_list.json()['data']
    # add customers to list
    for c in customer_list:
        customers.append(objects.Customer(c))

    return customers


def search(keyword):
    # search function is broken on openAPI
    pass


def post_customers(c_list):
    pass


def get_tickets(page_size=25, page=0, status=""):
    """Returns a list of the tickets.
    status types are "In Progress\""""

    if not Path(ticketfile).is_file():
        with open(ticketfile, "w+") as tf:
            tf.write("TEXT!")
            print(tf)

    url = base_url + "tickets" + api_key_string
    log.info("ticket_list type: %s", type(requests.get(url).json()))
    ticket_list = requests.get(url).json()
    """
        TotalRecords
        fromDate
        ticketData
        End of Program
    """
    log.info("ticket len: %s", len(ticket_list))
    for i in ticket_list:
        log.info("type of %s = %s", i, type(i))

    # Add ticket information to array
    return tickets
