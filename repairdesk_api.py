"""python wrapper for RepairDesk OpenAPI"""
import json, os, requests
from objects import *
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

tickets = []
save_offline = True  # Indicates whether to save to local file
read_offline = False


# sample_url https://api.repairdesk.co/api/web/v1/customers?api_key=YOUR_KEY

def __delete(url_string_snippet, record_number):
    assert type(record_number) is int or type(record_number) is str
    result = requests.delete(base_url + url_string_snippet + "/" + str(record_number), params={'api_key': api_key})
    print(result.url)
    return result


def delete_parts(*argv):
    result = []

    for part in argv:
        result.append(__delete("parts", part))

    return result


def get_api_key(self):
    return self.api_key


def __get(url_string_snippet, args=()):
    # in case of errors, I removed return statements to have just one at the end of the function
    """

    :rtype: json
    :param args: dict containing keys and values for the URL
    :type url_string_snippet: string
    """
    filename = "./" + url_string_snippet + ".json"
    payload = {'api_key': api_key}
    payload.update(args)

    if read_offline:  # Pull from online
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                result = json.load(file)
                # return result
        else:
            raise FileNotFoundError("{0} not found! Try pulling from online first.".format(filename))
    else:  # Pull from online
        result = requests.get(base_url + url_string_snippet, params=payload)
        url = result.url
        print(url)

        # Write data to disk
        if save_offline and "No Result Found" not in result.text:
            result = requests.get(base_url + url_string_snippet, params=payload).json()

            # Create file path
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w+") as out:  # Save data to file
                # out.write(datetime.now().__str__() + "\n")
                out.write(json.dumps(result))
                out.close()
        else:  # If there is no data to return
            print("No results found with this criteria.")
            result = False

    return result

def get_csv():
    # TODO: Convert wget string to requests string for CSV file. PHPSESSID is necessary for grabbing of files
    # TODO: Find out if there is a way to crawl/ index website endpoints and files with a sessionID
    # wget - O
    # result.csv - -no - cookies - -header = 'Cookie:PHPSESSID=ofpt96b2abpoluutl2sb7hp9e2' 'https://app.repairdesk.co/index.php?r=invoice/export2CSV&keyword=&prod_type=&status=&to=&from=&pagesize=50'"
    return


def get_customer(customer_id):
    customer_json = __get("customers/{0}".format(customer_id))
    return Customer(customer_json)


def get_customers(filter="", value=""):
    """Returns a list of only the customers in the JSON string.
    :rtype: list
    """
    # add customers to list
    result = __get("customers")
    customers = []

    for customer in result['data']:
        if filter:
            if filter in customer:
                if value in customer[filter]:
                    customers.append(Customer(customer))
            else:
                raise ValueError("Failed at Level 2")
        elif not filter:
            customers.append(Customer(customer))
        else:
            raise Exception("Something is wrong here!")
    return customers


def get_devices():
    return


def get_employees():
    return __get("employees")


def get_inventory():
    """Returns a list of items in inventory"""
    try:
        return __get("inventory")['data']
    except KeyError:
        print("There was an error with the data returned.")
        return


def get_invoice(id):
    """
    :return: returns invoice details.
    """
    result = __get("invoices/{0}".format(id))
    if result:
        result = Invoice(result['data'])
        return result
    else:
        print("No Results")

def get_invoices(days_ago=7, filter="", value=""):
    """

    :param days_ago: If you want to __get
    yesterday, 7 days, 30 days pass parameter named “filter” 1 for yesterday 7 or 30 etc. If you want to __get
    all invoices send 0 in this parameter.
    :return: returns invoices for past 7 days by default if no parameter is passed for the search.

    """

    result = __get("invoices", {'filter': days_ago})['data']['invoiceData']
    invoices = []

    for invoice in result:
        if filter:
            if filter in invoice:
                if value in invoice[filter]:
                    invoices.append(Invoice(invoice))
            else:
                raise ValueError("Failed at Level 2")
        elif not filter:
            invoices.append(Invoice(invoice))
        else:
            raise Exception("Something is wrong here!")
    return invoices


def get_parts():
    return __get("parts")['data']


def get_tickets(page_size=25, page=0, status=""):
    """Returns a list of the tickets.
        status types are "In Progress\""""
    try:
        return __get("tickets")['data']['ticketData']
    except KeyError:
        print("There was an error with the data returned.")
        return


def __post(url_string_snippet, args=()):
    payload = {'api_key': api_key}
    payload.update(args)

    return requests.post(base_url + url_string_snippet, params=payload)


def post_customer(customer):
    return __post(json.dumps(customer))


def __put(url_string_snippet, data):
    payload = {'api_key': api_key}

    print("data = {0}".format(data))

    result = requests.put(base_url + url_string_snippet, params=payload, json=data)
    print(result.url)
    return result


def put_customer(customer):
    return __put("customers/{0}".format(customer.__dict__['cid']), customer.__dict__)


def put_invoice(invoice):
    return __put("invoices/{0}".format(invoice.__dict__['summary']['id']), invoice.__dict__)


def search(keyword):
    # search function is broken on openAPI
    return


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
