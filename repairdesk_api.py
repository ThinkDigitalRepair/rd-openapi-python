"""python wrapper for RepairDesk OpenAPI"""
import json
import logging as log
import time

import jsonpickle
import requests
from Levenshtein import ratio
from jsondiff import diff as jsondiff
from jsonmerge import merge as jsonmerge
from openpyxl import load_workbook

from error import *
from objects import *

base_url = "https://api.repairdesk.co/api/web/v1/"


# noinspection PyStatementEffect
class RepairDesk:
    def __init__(self, api_key, read_offline=False):
        log.basicConfig(filename='log.log',
                        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%m-%d-%Y:%H:%M:%S',
                        level=log.DEBUG)

        # script-wide variables

        self.api_key = api_key
        self.api_key_string = ""

        self.tickets = []
        self.save_offline = True  # Indicates whether to save to local file
        self.offline_mode = read_offline

        self.last_refresh = datetime.now()

        self.session = requests.Session()
        # sample_url https://api.repairdesk.co/api/web/v1/customers?api_key=YOUR_KEY

    def __delete(self, url_string_snippet, record_number):
        assert type(record_number) is int or type(record_number) is str
        result = requests.delete(base_url + url_string_snippet + "/" + str(record_number),
                                 params={'api_key': self.api_key})
        print(result.url)
        return result

    @staticmethod
    def diff(obj1, obj2=None):
        """"Compare objects and return the differences."""
        print("function: diff()\n========================================================")
        if obj1 and obj2:
            difference = jsondiff(obj1.json, obj2.json)
        elif isinstance(obj1, list) and obj1 and not obj2:
            difference = jsondiff(obj1[0].json, obj1[1].json)
        else:
            raise ValueError("{0} and {1} are not valid objects".format(obj1, obj2))

        # cid should always be different. We don't want to merge this, so we're removing it. .
        difference['data'].pop('cid')

        print("function: End diff()\n========================================================")
        return difference

    def delete_parts(self, *argv):
        return [self.__delete("parts", part) for part in argv]

    def __get(self, url_string_snippet, print_url=False, **kwargs):
        """
    
        :rtype: json
        :param kwargs: dict containing keys and values for the URL
        :type url_string_snippet: string
        """
        if 'keyword' in kwargs:
            filename = "./" + url_string_snippet + "/" + kwargs['keyword'] + ".json"
        else:
            filename = "./" + url_string_snippet + ".json"
        payload = {'api_key': self.api_key}
        payload.update(kwargs)

        if self.offline_mode:  # Pull from offline
            try:
                with open(filename, 'r') as file:
                    result = jsonpickle.decode(file.read())
                    if print_url:
                        print(filename)
            except FileNotFoundError:  # File doesn't exist
                raise FileNotFoundError("{0} not found! Try pulling from online first.".format(filename))

        else:  # Pull from online
            result = requests.get(base_url + url_string_snippet, params=payload)
            url = result.url
            if print_url:
                print(url)

            # Write data to disk
            if self.save_offline and "No Result Found" not in result.text:
                result = requests.get(base_url + url_string_snippet, params=payload).json()

                # Create file path
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "w+") as out:  # Save data to file
                    # out.write(datetime.now().__str__() + "\n")
                    out.write(jsonpickle.encode(result))
                    out.close()
            else:  # If there is no data to return
                print("No results found with this criteria.")
                result = {}

        return result

    def get_xlsx(self, keyword: str = "", prod_type: str = "", status: str = "", to_date: str = "30 Sep, 2017",
                 from_date: str = "01 Jul, 2017", pagesize: int = 50) -> object:
        if logged_in:
            payload = {'r': 'invoice/export2CSV', 'keyword': keyword, 'prod_type': '', 'status': '', 'to': to_date,
                       'from': from_date, 'pagesize': pagesize}
            xlsx = self.session.get(url="https://app.repairdesk.co/index.php", params=payload)
            if self.save_offline:
                with open('invoice.xlsx', 'wb') as f:
                    f.write(xlsx.content)
                    f.close()
            return xlsx.content
        else:
            return False

    def get_customer(self, customer_id=0, phone_number=0):
        """
        Find and return customer object based on ID or phone number
        :param customer_id:
        :param phone_number:
        :return:
        """
        # TODO: edit to account for all possibilities
        if phone_number != 0 and customer_id == 0:
            try:
                results = self.__get("customers", keyword=str(phone_number))['data']
                if len(results) > 1:
                    return [Customer(result) for result in results]

                return Customer(results[0])
            except (IndexError, KeyError):  # If customer is not found in your records, this will return an IndexError
                # WARNING: May cause issues in the future by not returning a customer object
                return None

        else:
            customer_json = self.__get("customers/{0}".format(customer_id))
        return Customer(customer_json)

    @property
    def customers(self, filter_by="", value=""):
        """Returns a list of only the customers in the JSON string.
        :rtype: list
        """
        # add customers to list
        customers_as_dict = self.__get("customers")['data']
        customers_list = []
        for customer in customers_as_dict:
            if filter_by:
                if filter_by in customer:
                    if value.replace(' ', '') in customer[filter_by].replace(' ', ''):
                        customers_list.append(Customer(customer))
                else:
                    print("{0} is not a valid key".format(filter_by))
                    print("Valid keys are {0}".format(customer.keys()))
                    raise ValueError(filter_by)

            elif not filter_by:

                customers_list.append(Customer(customer))
                pass
            else:
                raise Exception("Something is wrong here!")
        return customers_list

    def get_devices(self):
        return

    def get_employees(self):
        return self.__get("employees")

    def get_inventory(self):
        """Returns a list of items in inventory"""
        try:
            return self.__get("inventory")['data']
        except KeyError:
            print("There was an error with the data returned.")
            return []

    def get_invoice(self, invoice_id):
        # Todo add ability to search by Invoice ID
        """
        :return: returns invoice details.
        """
        result = self.__get("invoices/{0}".format(invoice_id))
        if result:
            result = Invoice(result['data'])
            return result
        else:
            print("No Results")

    def get_invoices(self, days_ago=0, keyword=""):
        """

        :param keyword: A search term to filter search results by. Use in conjuction with keyword.
        :param days_ago: If you want to self.__get
        yesterday, 7 days, 30 days pass parameter named “filter” 1 for yesterday 7 or 30 etc. If you want to self.__get
        all invoices send 0 in this parameter.
        :return: returns invoices for past 7 days by default if no parameter is passed for the search.

        """

        result = self.__get("invoices", filter=days_ago, keyword=keyword)
        if result not in [None, {}] and result['success'] and 'invoiceData' in result['data']:
            invoices = [Invoice(invoice) for invoice in result['data']['invoiceData']]
            return invoices
        else:
            return [None]

    def get_matches(self, name: str):
        # TODO: make function apply for first and last names individually
        matches = []
        assert self.customers != []
        for customer in self.customers:
            name_ratio = ratio(name, customer.__getattribute__('fullName'))
            getattribute__ = customer.__getattribute__('fullName')
            if getattribute__ == "Dianna Sierra":
                print(customer.__getattribute__('fullName'))
                print(name_ratio)
            if name_ratio > 0.4:
                matches.append(customer)
        return matches

    def get_parts(self):
        return self.__get("parts")['data']

    def get_problems(self) -> object:
        return self.__get("problems")

    def get_taxed_items(self, tax_class_name, days_ago=7):
        assert isinstance(tax_class_name, str)
        detailed_invoice_list = []
        invoices = self.get_invoices(days_ago=days_ago)
        add_sleep = True if len(invoices) > 50 else False
        for invoice in invoices:
            get_invoice = self.get_invoice(invoice.__getattribute__("summary")['id'])
            if add_sleep:
                print("sleeping")
                time.sleep(60 / 50)

        items_with_specified_tax = []
        total = 0
        for invoice in detailed_invoice_list:
            for item in invoice['items']:
                if tax_class_name in item['tax_class']['tax_class']:
                    items_with_specified_tax.append(item)
                    total += float(item['gst'])
        return {"items": items_with_specified_tax, "total": round(total, 2)}

    def get_taxed_items_from_xlsx(self, exclude: list = [], filename: str = ""):
        """

        :exclude: list: a list of strings to exclude from result
        """
        # TODO: Enter options for filter
        tax_class = {'MTS': 0.114}
        # invoice_xlsx is of type <openpyxl.workbook.workbook.Workbook>
        invoice_xlsx = load_workbook(filename) if filename else self.get_xlsx()
        assert invoice_xlsx
        worksheet = invoice_xlsx.active
        invoice_number_row = worksheet['A']
        item_name_row = worksheet['D']
        taxed_items = []
        price_row = worksheet['G']
        item_prices = []
        tax_row = worksheet['H']
        tax_charged = []

        for c in range(2, len(tax_row)):
            if tax_row[c].value == 0 or price_row[c].value == 0 or tax_row[c].value is None or \
                    price_row[c].value is None:
                continue
            elif tax_row[c].value / price_row[c].value == tax_class['MTS'] and item_name_row[c].value not in exclude:
                taxed_items.append(
                    "From invoice: {0} - {1}".format(invoice_number_row[c].value, item_name_row[c].value))
                item_prices.append(price_row[c].value)
                tax_charged.append(tax_row[c].value)

        return {'taxed_items': taxed_items, 'tax_charged': tax_charged, 'total_gross': round(sum(item_prices)),
                'total_tax_collected': round(sum(tax_charged), 2)}

    def get_ticket(self, ticket_id):
        ticket_json = self.__get("tickets/{0}".format(ticket_id))
        return Ticket(ticket_json)

    def get_tickets(self, page_size=25, page=0, **kwargs):
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
                kwargs['from_date'] = self.strptime(kwargs['from_date'])

            if "to_date" in kwargs:
                print("to_date: {0}".format(kwargs['to_date']))
                kwargs['to_date'] = self.strptime(kwargs['to_date'])

            result = self.__get("tickets", **kwargs)['data']['ticketData']
            ticket_list = [Ticket(item) for item in result]

            return ticket_list

        except KeyError:
            print("There was an error with the data returned.")
            return []

    def __post(self, url_string_snippet: str, data: dict = None, **kwargs) -> object:
        """
        :rtype: object
        """
        payload = {'api_key': self.api_key}

        result = requests.post(base_url + url_string_snippet, params=payload, data=data)
        print("requests.post(\"{0}\", data={1})".format(result.url, kwargs))
        return result

    def login(self, username: str, password: str) -> bool:

        if not self.offline_mode:
            login_url = "https://app.repairdesk.co/index.php"
            username_field = "LoginForm[username]"
            password_field = "LoginForm[password]"
            auth = ('user', 'pass')
            payload = {username_field: username, password_field: password}

            login = self.session.post(auth=auth, url=login_url, data=payload)

            global logged_in

            if "Incorrect Email or password" in login.text:
                log.log(level=30, msg="User not logged in successfully")
                logged_in = False
                raise NotLoggedInError(expression="Expression", message="User not logged in successfully")
            else:
                logged_in = True
                return logged_in

    @staticmethod
    def merge(obj1=None, obj2=None):
        print("function: merge()\n========================================================")
        if not obj1 and not obj2:
            obj1 = {"cid": "1", "first_name": "Test", "last_name": "Customer", "phone": "", "mobile": "+1 555-555-5555",
                    "address1": "", "address2": "", "postcode": "", "city": "", "state": "", "country": "United States",
                    "email": "noone@example.com", "orgonization": "", "refered_by": "", "driving_licence": "",
                    "contact_person": "", "tax_number": "", "network": "Verizon",
                    "customer_group": {"id": "1", "name": "Individual"}}
            obj2 = {"cid": "2", "first_name": "Test", "last_name": "Customer", "phone": "760-534-8118",
                    "mobile": "+1 555-555-5234",
                    "address1": "", "address2": "", "postcode": "", "city": "", "state": "", "country": "United States",
                    "email": "noone1@example.com", "orgonization": "", "refered_by": "", "driving_licence": "",
                    "contact_person": "", "tax_number": "", "network": "Verizon",
                    "customer_group": {"id": "12", "name": "Individual"}}

        result = jsonmerge(obj1, obj2)

        print("function: End merge()\n========================================================")
        return result

    @staticmethod
    def merge_customers(customer1, customer2):
        customer1
        customer2
        # decide which record to keep
        # copy data from record to discard to record to keep

        pass
        return

    def post_customer(self, customer):
        data = {}

        for key, value in customer.__dict__.items():
            data[key] = value

        return self.__post("customers", data=data)

    def post_invoice(self, invoice):
        data = {}

        for key, value in invoice.__dict__.items():
            data[key] = value

        return self.__post("invoices", data=data)

    def post_payment(self, invoice_id: str, amount: int, payment_date: str, method: str, notes: str) -> object:
        """
        Adds payment to invoice
            Request Sample:
            {"amount":"30.00","payment_date":"1472122800","method":"Cash","notes":"Test
            Notes"}
        :return:
        """
        payment_date = int(self.strptime(payment_date))
        return self.__post("invoices/{0}/payments".format(invoice_id),
                           json={"amount": amount, "payment_date": payment_date, "method": method,
                                 "notes": notes})

    def post_ticket(self, ticket):
        data = {}

        for key, value in ticket.__dict__.items():
            data[key] = value

        return self.__post("tickets", data=data)

    def __put(self, url_string_snippet, data):
        payload = {'api_key': self.api_key}

        print("data = {0}".format(data))

        result = requests.put(base_url + url_string_snippet, params=payload, json=data)
        print(result.url)
        return result

    def put_customer(self, customer):
        return self.__put("customers/{0}".format(customer.__dict__['cid']), customer.__dict__)

    def put_invoice(self, invoice):
        return self.__put("invoices/{0}".format(invoice.__dict__['summary']['id']), invoice.__dict__)

    def put_ticket(self, ticket):
        return self.__put("ticket", json.dumps(ticket))

    def search(self, keyword):
        # search function is broken on openAPI
        return

    # noinspection PyIncorrectDocstring
    @staticmethod
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

    @staticmethod
    def total(list_to_sum, list_value):
        total = 0
        for item in list_to_sum:
            total += item[list_value]
