"""python wrapper for RepairDesk OpenAPI"""
import json
import logging as log

import requests
from openpyxl import load_workbook

from objects import *

log.basicConfig(filename='log.log',
                format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%m-%d-%Y:%H:%M:%S',
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
        deletion_confirmation = __delete("parts", part)
        result.append(deletion_confirmation)

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
                if print_url:
                    print(filename)
        else:
            raise FileNotFoundError("{0} not found! Try pulling from online first.".format(filename))
    else:  # Pull from online
        result = requests.get(base_url + url_string_snippet, params=payload)
        url = result.url
        if print_url:
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


def get_customers(filter_by="", value=""):
    """Returns a list of only the customers in the JSON string.
    :rtype: list
    """
    # add customers to list
    result = __get("customers")
    customers = []

    for customer in result['data']:
        if filter_by:
            if filter_by in customer:
                if value.replace(' ', '') in customer[filter_by].replace(' ', ''):
                    customers.append(Customer(customer))
            else:
                print("{0} is not a valid key".format(filter_by))
                print("Valid keys are {0}".format(customer.keys()))
                break
        elif not filter_by:
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


def get_invoices(days_ago=0, keyword=""):
    """

    :param keyword: A search term to filter search results by. Use in conjuction with keyword.
    :param value: Keyword value. For example, keyword=value (..., name, "John Doe")
    :param days_ago: If you want to __get
    yesterday, 7 days, 30 days pass parameter named “filter” 1 for yesterday 7 or 30 etc. If you want to __get
    all invoices send 0 in this parameter.
    :return: returns invoices for past 7 days by default if no parameter is passed for the search.

    """

    result = __get("invoices", filter=days_ago, keyword=keyword)
    if result:
        result = result['data']['invoiceData']
    else:
        result = []
    return result


def get_parts():
    return __get("parts")['data']


def get_problems() -> object:
    return __get("problems")


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


def get_taxed_items_from_xlsx(filename: str):
    tax_class = {'MTS': 0.114}
    invoice_xlsx = load_workbook(filename)
    worksheet = invoice_xlsx.active
    invoice_number_row = worksheet['A']
    item_name_row = worksheet['D']
    taxed_items = []
    price_row = worksheet['G']
    item_prices = []
    tax_row = worksheet['H']
    tax_charged = []

    for c in range(2, len(tax_row)):
        if tax_row[c].value == 0 or price_row[c].value == 0 or tax_row[c].value is None or price_row[c].value is None:
            continue
        elif tax_row[c].value / price_row[c].value == tax_class['MTS']:
            taxed_items.append("From invoice: {0} - {1}".format(invoice_number_row[c].value, item_name_row[c].value))
            item_prices.append(price_row[c].value)
            tax_charged.append(tax_row[c].value)
    return {'tax_items': taxed_items, 'tax_charged': tax_charged, 'item_price_sum': round(sum(item_prices)),
            'total': round(sum(tax_charged), 2)}



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


def __post(url_string_snippet: str, **kwargs) -> object:
    """

    :rtype: object
    """
    payload = {'api_key': api_key}

    result = requests.post(base_url + url_string_snippet, kwargs, params=payload)
    print("requests.post(\"{0}\", data={1})".format(result.url, kwargs))
    return result


def merge_customers(customer1, customer2):
    customer1
    customer2
    # decide which record to keep
    # copy data from record to discard to record to keep

    pass
    return


def post_customer(customer):
    return __post("customers", json={"first_name": "Test", "last_name": "Customer2", "email": "noone2@example.com"})
    # return requests.post("http://httpbin.org/post", data={"first name": "Test", "last_name": "Customer2", "email": "noone2@example.com"})


def post_payment(invoice_id: str, amount: int, payment_date: str, method: str, notes: str) -> object:
    """
    Adds payment to invoice
        Request Sample:
        {"amount":"30.00","payment_date":"1472122800","method":"Cash","notes":"Test
        Notes"}
    :return:
    """
    payment_date = int(strptime(payment_date))
    return __post("invoices/{0}/payments".format(invoice_id),
                  json={"amount": amount, "payment_date": payment_date, "method": method,
                        "notes": notes})


def post_ticket(ticket):
    return __post("tickets", json=ticket.__dict__)


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
    return __put("ticket", json.dumps(ticket))


def search(keyword):
    # search function is broken on openAPI
    return


def set_api_key(key):
    """

    :type key: str
    :rtype: None
    """
    global api_key, api_key_string
    api_key = key
    api_key_string = "?api_key=" + api_key


def strptime(date_time_string):
    """

    :param date_time_string: "%m-%d-%Y %H:%M:%S"
    :return: timestamp
    """
    if len(date_time_string.replace(" ", "")) == 17:
        return datetime.strptime(date_time_string, "%m-%d-%Y %H:%M:%S").timestamp()
    elif len(date_time_string.strip()) == 10:
        return datetime.strptime(date_time_string, "%m-%d-%Y").timestamp()
    else:
        raise ValueError(
            "Improper date_time_string format: {0}; len={1}".format(date_time_string, len(date_time_string)))


def total(list_to_sum, list_value):
    total = 0
    for item in list_to_sum:
        total += item[list_value]
    return total
