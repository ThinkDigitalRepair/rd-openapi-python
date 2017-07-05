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