import logging


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

    def __init__(self, customer):
        """ fullName, cid, phone, mobile, address1, address2, postcode, city, state, country, email, orgonization,
                 refered_by, driving_licence, contact_person, tax_number, network"""
        self.phone = customer['phone']
        self.fullname = customer['fullName']
        self.cid = customer['cid']
        self.phone = customer['phone']
        self.mobile = customer['mobile']
        self.address1 = customer['address1']
        self.address2 = customer['address2']
        self.postal_code = customer['postcode']
        self.city = customer['city']
        self.state = customer['state']
        self.country = customer['country']
        self.email = customer['email']
        self.organization = customer['orgonization']
        self.referred_by = customer['refered_by']
        self.driving_license = customer['driving_licence']
        self.contact_person = customer['contact_person']
        self.tax_number = customer['tax_number']
        self.network = customer['network']


# Todo: Create reverse function

class Tickets(object):
    ticket_list = []
    devices = []
    ticket_data=""

    def __init__(self):
        """ test """

        global ticket_list
        global ticket_data
        global devices
        pass


class Summary():
    ID = 0
    order_id = ""
    total = 0
    how_did_u_find_us = ""
    created_date = 0
    repair_collected = 0

    def __init__(self):
        global ID
        global order_id
        global total
        global how_did_u_find_us
        global created_date
        global repair_collected


class Devices():
    device = []

    def __init__():
        global device

    def append(self, device_to_append):
        device.append(device_to_append)

    def get(dnum):
        return device[dnum]

    def remove(dnum):
        device.remove(dnum)


class RepairProdItems():
    def __init__(self, name, device_id):
        repair_prod_item = {"name": name, "id": device_id}
        print ("New repair_prod_item initialized: " + repair_prod_item['name'] + ": " +
               repair_prod_item['id'])
