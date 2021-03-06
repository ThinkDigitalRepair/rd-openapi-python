import os
from datetime import datetime

import vobject
from dateutil.tz import tzlocal

error_json = {'name': 'Too Many Requests', 'message': 'Rate limit exceeded.', 'code': 0, 'status': 429}


def strptime(date_time_string):
    """

    :param date_time_string:
    :return: Return a string representing the time in datetime format
    """
    x = datetime.strptime(str(date_time_string), "%m-%d-%Y %H:%M:%S").timestamp()
    return x


def to_human_readable(date_time):
    """

    :return: a string containing the date and time in a human-readable format.
    """

    return datetime.fromtimestamp(date_time).astimezone(tzlocal()).ctime()


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

    def __init__(self, customer=None):

        if not isinstance(customer, dict) and hasattr(customer, 'json'):
            customer = customer.json
        else:
            self.json = customer
        if self.json and 'data' in self.json:
            for key in customer['data']:
                # self.__dict__[key] = customer['data'][key]
                setattr(self, key, customer['data'][key])
                print(key)
        else:
            for key in customer:
                # self.__dict__[key] = customer[key]
                setattr(self, key, customer[key])

        if "fullName" in self.__dict__:
            name = self.__getattribute__('fullName').split()
            self.__dict__['first_name'], self.__dict__['last_name'] = name[0], name[1] if len(name) > 1 else ''

            # """ fullName, cid, phone, mobile, address1, address2, postcode, city, state, country, email,
            #  orgonization, refered_by, driving_licence, contact_person, tax_number, network"""

    def __contains__(self, value):
        return True if value in self.__dict__ else False

    def get_email(self):
        return self.__dict__['email']

    def get_first_name(self):
        return self.__dict__['first_name']

    def get_last_name(self):
        if 'last_name' in self.__dict__:
            return self.__dict__['last_name']
        else:
            return "No Last Name"

    def get_mobile(self):
        return self.__dict__['mobile']

    def get_phone(self):
        return self.__dict__['phone']

    def to_vcf(self):
        """
        Exports a VCF of the customer and writes it to a file
        :return: the vcf object
        """
        j = vobject.vCard()
        j.add('n')
        if 'first_name' in self.__dict__:
            first_name, last_name = self.__getattribute__('first_name'), self.__getattribute__('last_name')
        else:
            name = self.__getattribute__('fullName').split()
            first_name, last_name = name[0], name[1] if len(name) > 1 else ''

        j.n.value = vobject.vcard.Name(family=last_name, given=first_name)
        j.add('fn')  # required field
        j.fn.value = "{0} {1}".format(first_name, last_name)  # Set name

        def add_value(value_name, value, value_type=''):

            """

            :param value_name: vObject attribute
            :param value: value of the attribute
            :param value_type: type parameter
            """

            obj = j.add(value_name)  # adds a new element to j,
            obj.value = value
            obj.type_param = value_type
            return obj

        a = add_value('tel', self.__getattribute__('mobile').replace(' ', '').replace('-', ''),
                      'Mobile')  # removing spaces
        b = add_value('tel', self.__getattribute__('phone').replace(" ", ""), 'Contact Number')  # removing spaces
        c = add_value('email', self.__getattribute__('email'), 'Home')

        j.serialize()

        filename = './contacts/{0}{1}.vcf'.format(first_name, last_name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as vcf:
            vcf.write(j.serialize())
            vcf.close()

        return j
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = ""

        for key in self.__dict__:
            if key == 'json':
                continue
            if isinstance(self.__getattribute__(key), type("")):
                value = self.__getattribute__(key)
            else:
                for key2 in self.__getattribute__(key):
                    if isinstance(key2, str):
                        value = key2 + ": " + self.__getattribute__(key)[key2]

            string += key + ": " + value + " "
        return string
    
    def __getitem__(self, item):
        return self.__getattribute__(item)



class Devices:
    device = []

    def __init__(self):
        global device

    def append(self, device_to_append):
        """

        :type device_to_append: int
        """
        device.append(device_to_append)

    def get(self, dnum):
        """

        :type dnum: int
        """
        return device[dnum]

    def remove(self, dnum):
        """

        :type dnum: int
        """
        device.remove(dnum)


class Invoice(object):
    invoice_id = ""
    iter = 0

    def __init__(self, invoice):
        self.json = invoice
        self.human_readable_date = to_human_readable(invoice['summary']['created_date'])

        for key in invoice:
            self.__dict__[key] = invoice[key]
            self.invoice_id = invoice['summary']['order_id']

    def __getitem__(self, item):
        return self.__dict__[item]


class RepairProdItems:
    def __init__(self, name, device_id):
        repair_prod_item = {"name": name, "id": device_id}
        print("New repair_prod_item initialized: " + repair_prod_item['name'] + ": " +
              repair_prod_item['id'])


class Summary(object):
    ID = 0
    order_id = ""
    total = 0
    how_did_u_find_us = ""
    created_date = 0
    repair_collected = 0

    def __init__(self, identification, order_id, total, hdufu, created_date, repair_collected):
        self.ID = identification
        self.order_id = order_id
        self.total = total
        self.how_did_u_find_us = hdufu
        self.created_date = created_date
        self.repair_collected = repair_collected


class Ticket(object):
    t_id = ""
    statuses = ["Pending",
                "In Progress",
                "Repaired",
                "Completed",
                "Unlocked",
                "Repaired & Collected",
                "Waiting on Customer",
                "Warranty Repair",
                "Customer Reply",
                "Cancelled",
                "Disposed",
                "Waiting for Parts"]

    def __getitem__(self, item):
        return self.__dict__[item]

    def __init__(self, ticket_object):
        self.json = ticket_object

        if 'summary' in ticket_object:
            for key in ticket_object:
                self.__dict__[key] = ticket_object[key]

            self.t_id = ticket_object['summary']['order_id']

        elif 'data' in ticket_object:
            for key in ticket_object['data']:
                self.__dict__[key] = ticket_object['data'][key]
            self.t_id = ticket_object['data']['summary']['order_id']

    def __str__(self):
        return str(self.__dict__)

    def created_date_to_human_readable(self):
        return datetime.fromtimestamp(self.__dict__['summary']['created_date']).strftime('%m-%d-%Y %H:%M:%S')

    def __iter__(self):
        return self.__iter__()
