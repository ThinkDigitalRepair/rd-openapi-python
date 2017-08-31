"""python wrapper for RepairDesk OpenAPI"""
import json
import requests
import objects
import logging as log
from pathlib import Path
from datetime import datetime

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
save_offline = False  # Indicates whether to save to local file or pull from online.
read_offline = False


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


def get_customer(customer_id):
    customer_json = get("customers/{0}".format(customer_id))
    return customer_json


def get_customers():
    """Returns a list of only the customers in the JSON string.
    :rtype: list
    """
    # add customers to list
    return get("customers")


def search(keyword):
    # search function is broken on openAPI
    pass


def post_customers(c_list):
    requests.put()
    pass


def get_tickets(page_size=25, page=0, status=""):
    """Returns a list of the tickets.
        status types are "In Progress\""""
    return get("tickets")['data']['ticketData']


def get_invoices(days_ago=7):
    """

    :param days_ago: If you want to get
    yesterday, 7 days, 30 days pass parameter named “filter” 1 for yesterday 7 or 30 etc. If you want to get
    all invoices send 0 in this parameter.
    :return: returns invoices for past 7 days by default if no parameter is passed for the search.

    """
    return get("invoice", {'filter': days_ago})['data']['invoiceData']


def get_invoice(id):
    """

    :return: returns invoice details.

    """
    return get("invoices/{0}".format(id))['data']


def get(url_string_snippet, args=()):
    """

    :rtype: json
    :param args: dict containing keys and values for the URL
    :type url_string_snippet: string
    """
    filename = url_string_snippet.replace('/', '') + ".json"
    payload = {'api_key': api_key}
    payload.update(args)

    if not read_offline:  # Pull from online
        result = requests.get(base_url + url_string_snippet, params=payload)
        url = result.url
        print(url)
    else:  # Pull from offline
        with open(filename, 'r') as file:
            result = json.load(file)['data']
        return result

    if not read_offline and "No Result Found" not in result.text:  # If there is data to return
        # TODO: Change this line to account for offline file
        result = requests.get(base_url + url_string_snippet, params=payload).json()

        with open(filename, "w+") as out:  # Save data to file
            # out.write(datetime.now().__str__() + "\n")
            out.write(json.dumps(result))
            out.close()

        return result
    else:  # If there is no data to return
        print("No results found with this criteria.")
        return 0


def get_csv():
    # TODO: Convert wget string to requests string for CSV file. PHPSESSID is necessary for grabbing of files
    # TODO: Find out if there is a way to crawl/ index website endpoints and files with a sessionID
    # wget - O
    # result.csv - -no - cookies - -header = 'Cookie:PHPSESSID=ofpt96b2abpoluutl2sb7hp9e2' 'https://app.repairdesk.co/index.php?r=invoice/export2CSV&keyword=&prod_type=&status=&to=&from=&pagesize=50'"
    pass
