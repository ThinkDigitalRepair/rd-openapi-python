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


def __get(url_string_snippet, **kwargs):

    """

    :rtype: json
    :param kwargs: dict containing keys and values for the URL
    :type url_string_snippet: string
    """
    print_url = True
    filename = "./" + url_string_snippet + ".json"
    payload = {'api_key': api_key}
    payload.update(kwargs)

    if read_offline:  # Pull from online
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                result = json.load(file)
                if print_url: print(filename)
        else:
            raise FileNotFoundError("{0} not found! Try pulling from online first.".format(filename))
    else:  # Pull from online
        result = requests.get(base_url + url_string_snippet, params=payload)
        url = result.url
        if print_url: print(url)

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
            result = {}

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
                if value.replace(' ', '') in customer[filter].replace(' ', ''):
                    customers.append(Customer(customer))
            else:
                print("{0} is not a valid key".format(filter))
                print("Valid keys are {0}".format(customer.keys()))
                break
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
        return []


def get_invoice(invoice_id):
    # Todo add ability to search by Invoice ID
    """
    :return: returns invoice details.
    """
    result = __get("invoices/{0}".format(invoice_id))
    if result:
        result = Invoice(result['data'])
        return result
    else:
        print("No Results")


def get_invoices(days_ago=0, keyword="", value=""):
    """

    :param days_ago: If you want to __get
    yesterday, 7 days, 30 days pass parameter named “filter” 1 for yesterday 7 or 30 etc. If you want to __get
    all invoices send 0 in this parameter.
    :return: returns invoices for past 7 days by default if no parameter is passed for the search.

    """

    result = __get("invoices", filter=days_ago)
    if result:
        result = result['data']['invoiceData']
    else:
        return []

    invoices = []

    for invoice in result:
        if keyword:
            if keyword in invoice:
                if value in invoice[keyword]:
                    invoices.append(Invoice(invoice))
            else:
                raise ValueError("Failed at Level 2")
        elif not keyword:
            invoices.append(Invoice(invoice))
        else:
            raise Exception("Something is wrong here!")
    return invoices


def get_parts():
    return __get("parts")['data']


def get_taxed_items(tax_class_name, days_ago=7):
    assert isinstance(tax_class_name, str)
    detailed_invoice_list = []
    for invoice in get_invoices(days_ago=days_ago):
        detailed_invoice_list.append(get_invoice(invoice.__getattribute__("summary")['id']))

    items_with_specified_tax = []
    total = 0
    for invoice in detailed_invoice_list:
        for item in invoice['items']:
            if tax_class_name in item['tax_class']['tax_class']:
                items_with_specified_tax.append(item)
                total += float(item['gst'])
    return {"items": items_with_specified_tax, "total": round(total, 2)}


def get_ticket(ticket_id):
    ticket_json = __get("tickets/{0}".format(ticket_id))
    return Ticket(ticket_json)


def get_tickets(page_size=25, page=0, **kwargs):
    """
    Returns a list of the tickets.
    a) : pagesize: number of ticket to be displayed per request
    b) : page: refers to pagination limits e.g. Page 1,2 3 etc. Default page is identified by 0
    c) : status: search by ticket status
    d) : assigned_to: Send ID of the ticket assignee
    e) : created_by: Send ID of the user who created the ticket
    f) : from_date,to_date: earliest date to latest date. Both values not required.
        If not set, this will return tickets for today as default.
        To get tickets for previous dates, send an extra parameter in URL titled "filter" with values:
        time must be entered as a string in the format: "%m-%d-%Y %H:%M:%S" OR "%m-%d-%Y"
    Yesterday: 1
    Last Week: 7
    Last Month: 30
    All: 0
    """
    try:
        if "from_date" in kwargs:
            print("from_date: {0}".format(kwargs['from_date']))
            kwargs['from_date'] = strptime(kwargs['from_date'])

        if "to_date" in kwargs:
            print("to_date: {0}".format(kwargs['to_date']))
            kwargs['to_date'] = strptime(kwargs['to_date'])

        result = __get("tickets", **kwargs)['data']['ticketData']
        ticket_list = []

        for item in result:
            ticket_list.append(Ticket(item))
        return ticket_list

    except KeyError:
        print("There was an error with the data returned.")
        return []


def __post(url_string_snippet, args=()):
    payload = {'api_key': api_key}
    payload.update(args)

    return requests.post(base_url + url_string_snippet, params=payload)


def merge_customers():
    c_list = get_customers()
    customer1 = c_list[0]
    customer2 = c_list[1]
    # decide which record to keep
    # copy data from record to discard to record to keep

    pass
    return


def post_customer(customer):
    return __post(json.dumps(customer))


def post_ticket(ticket):
    return __post(json.dumps(ticket))


def __put(url_string_snippet, data):
    """
    Update
    :type url_string_snippet: string
    """
    payload = {'api_key': api_key}

    print("data = {0}".format(data))

    result = requests.put(base_url + url_string_snippet, params=payload, json=data)
    print(result.url)
    return result


def put_customer(customer):
    return __put("customers/{0}".format(customer.__dict__['cid']), customer.__dict__)


def put_invoice(invoice):
    return __put("invoices/{0}".format(invoice.__dict__['summary']['id']), invoice.__dict__)


def put_ticket(ticket):
    return __put(json.dumps(ticket))


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


def strptime(date_time_string):
    if len(date_time_string.strip()) == 19:
        return datetime.strptime(date_time_string, "%m-%d-%Y %H:%M:%S").timestamp()
    elif len(date_time_string.strip()) == 10:
        return datetime.strptime(date_time_string, "%m-%d-%Y").timestamp()
    else:
        raise ValueError("Improper date_time_string format")


def total(list_to_sum, list_value):
    total = 0
    for item in list_to_sum:
        total += item[list_value]
    return total
