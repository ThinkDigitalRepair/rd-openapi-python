"""python wrapper for RepairDesk OpenAPI"""
import json
import requests
import objects
import logging as log
from pathlib import Path

ticketfile = "ticketfile.json"

log.basicConfig(filename='log.log',
                format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', \
                datefmt='%m-%d-%Y:%H:%M:%S', \
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
    # add customers to list
    return get("customers")['data']


def search(keyword):
    # search function is broken on openAPI
    pass


def post_customers(c_list):
    pass


def get_tickets(page_size=25, page=0, status=""):
    """Returns a list of the tickets.
        status types are "In Progress\""""
    return get("tickets")['data']['ticketData']


def get_invoices(_filter_=1):
    return get("invoice", {'filter': _filter_})['data']['invoiceData']


def get(url_string_snippet, args=()):
    payload = {'api_key': api_key}
    payload.update(args)
    result = requests.get(base_url + url_string_snippet, params=payload)
    print(result.ok)
    if "No Result Found" not in result.text:
        return requests.get(base_url + url_string_snippet, params=payload).json()
    else:
        print("No results found with this criteria.")
        return 0


def get_csv():
    # TODO: Convert wget string to requests string for CSV file. PHPSESSID is necessary for grabbing of files
    # TODO: Find out if there is a way to crawl/ index website endpoints and files with a sessionID
    # wget - O
    # result.csv - -no - cookies - -header = 'Cookie:PHPSESSID=ofpt96b2abpoluutl2sb7hp9e2' 'https://app.repairdesk.co/index.php?r=invoice/export2CSV&keyword=&prod_type=&status=&to=&from=&pagesize=50'"
    pass
