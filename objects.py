import vobject, os


# Todo: Create reverse function
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

    """cid
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
    network"""

    def __init__(self, customer):
        if 'data' in customer:
            for key in customer['data']:
                self.__dict__[key] = customer['data'][key]
        else:
            for key in customer:
                self.__dict__[key] = customer[key]
                #
                #
                # """ fullName, cid, phone, mobile, address1, address2, postcode, city, state, country, email, orgonization,
                #          refered_by, driving_licence, contact_person, tax_number, network"""

    def to_vcf(self):
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

        j.prettyPrint()
        j.serialize()

        filename = './contacts/{0}{1}.vcf'.format(first_name, last_name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as vcf:
            vcf.write(j.serialize())
            vcf.close()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = ""

        for key in self.__dict__:
            if isinstance(self.__getattribute__(key), type("")):
                value = self.__getattribute__(key)
            else:
                for key2 in self.__getattribute__(key):
                    if isinstance(key2, type("")):
                        value = key2 + ": " + self.__getattribute__(key)[key2]

            string += key + ": " + value + "\n"
        return string


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
    def __init__(self, invoice):
        for key in invoice:
            self.__dict__[key] = invoice[key]
            print("key: {0}\nvalue: {1}".format(key, self.__dict__[key]))


class RepairProdItems():
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
    ticket_list = []
    devices = []
    ticket_data = {}

    def __init__(self, ticket_object):
        """ test """

        global ticket_list
        global ticket_data
        global devices

        ticket_data = {
            "success": True,
            "statusCode": 200,
            "message": "OK",
            "data": {
                "ticketData": [
                    {
                        "summary": {
                            "id": "406453",
                            "order_id": "T-1373",
                            "total": "$60.00",
                            "how_did_u_find_us": "",
                            "created_date": 1499133810,
                            "repair_collected": -62169955200,
                            "customer": {
                                "fullName": "Gloria  Del Olma",
                                "id": "774276",
                                "mobile": "+1 760-880-9618",
                                "address1": "",
                                "fullname": "Gloria ",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "iPhone Manual SIM Unlock (2017)",
                                        "id": "1960066"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463745",
                                "price": "60.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$60.00",
                                "device": {
                                    "id": "",
                                    "name": ""
                                },
                                "assigned_to": {
                                    "id": "0",
                                    "fullname": ""
                                },
                                "imei": "123456789123456",
                                "due_on": -62169955200
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "397661",
                            "order_id": "T-1341",
                            "total": "$60.00",
                            "how_did_u_find_us": "",
                            "created_date": 1498604679,
                            "repair_collected": -62169955200,
                            "customer": {
                                "fullName": "Steven Bucio",
                                "id": "766591",
                                "mobile": "+1 760-699-4438",
                                "address1": "",
                                "fullname": "Steven",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "iPhone Manual SIM Unlock (2017)",
                                        "id": "1960066"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "453359",
                                "price": "60.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$60.00",
                                "device": {
                                    "id": "",
                                    "name": ""
                                },
                                "assigned_to": {
                                    "id": "0",
                                    "fullname": ""
                                },
                                "imei": "355373085937615",
                                "due_on": -62169955200
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "395838",
                            "order_id": "T-1334",
                            "total": "$60.00",
                            "how_did_u_find_us": "",
                            "created_date": 1498504721,
                            "repair_collected": -62169955200,
                            "customer": {
                                "fullName": "Carlos Caballero",
                                "id": "764954",
                                "mobile": "",
                                "address1": "",
                                "fullname": "Carlos",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": "+1 760-396-6548"
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "T-Mobile iPhone Unlock (Clean)",
                                        "id": "1474146"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "451187",
                                "price": "60.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$60.00",
                                "device": {
                                    "id": "",
                                    "name": ""
                                },
                                "assigned_to": {
                                    "id": "0",
                                    "fullname": ""
                                },
                                "imei": "358369067425097",
                                "due_on": -62169955200
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "392572",
                            "order_id": "T-1325",
                            "total": "$60.00",
                            "how_did_u_find_us": "",
                            "created_date": 1498258447,
                            "repair_collected": -62169955200,
                            "customer": {
                                "fullName": "Valerie Ramirez",
                                "id": "161340",
                                "mobile": "+1 442-200-4534",
                                "address1": "",
                                "fullname": "Valerie",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "iPhone Manual SIM Unlock (2017)",
                                        "id": "1960066"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "447497",
                                "price": "60.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$60.00",
                                "device": {
                                    "id": "",
                                    "name": ""
                                },
                                "assigned_to": {
                                    "id": "0",
                                    "fullname": ""
                                },
                                "imei": "356951067653562",
                                "due_on": -62169955200
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "411589",
                            "order_id": "T-1385",
                            "total": "$77.90",
                            "how_did_u_find_us": "",
                            "created_date": 1499388313,
                            "repair_collected": 1499324400,
                            "customer": {
                                "fullName": "Maria Hernandez",
                                "id": "780096",
                                "mobile": "+1 760-393-6422",
                                "address1": "",
                                "fullname": "Maria",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD) Black",
                                        "id": "892467"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "469695",
                                "price": "75.00",
                                "gst": "2.90",
                                "line_discount": "0.00",
                                "total": "$77.90",
                                "device": {
                                    "id": "137485",
                                    "name": "iPhone 5S"
                                },
                                "assigned_to": {
                                    "id": "1769",
                                    "fullname": "Edgar Hernandez"
                                },
                                "imei": "358805057292872",
                                "due_on": 1499391420
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "411309",
                            "order_id": "T-1380",
                            "total": "$41.55",
                            "how_did_u_find_us": "",
                            "created_date": 1499376141,
                            "repair_collected": 1499324400,
                            "customer": {
                                "fullName": "Walk In",
                                "id": "0",
                                "mobile": "",
                                "address1": "",
                                "fullname": "Walk",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Louder speaker Replacement",
                                        "id": "892446"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "469343",
                                "price": "40.00",
                                "gst": "1.55",
                                "line_discount": "0.00",
                                "total": "$41.55",
                                "device": {
                                    "id": "137483",
                                    "name": "iPhone 4S"
                                },
                                "assigned_to": {
                                    "id": "1798",
                                    "fullname": "King Amaya"
                                },
                                "imei": "",
                                "due_on": 1499379660
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "411169",
                            "order_id": "T-1379",
                            "total": "$60.00",
                            "how_did_u_find_us": "",
                            "created_date": 1499366993,
                            "repair_collected": -62169955200,
                            "customer": {
                                "fullName": "Brenda Benitas",
                                "id": "413240",
                                "mobile": "+1 760-777-3329",
                                "address1": "",
                                "fullname": "Brenda",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Data Forensics",
                                        "id": "1382142"
                                    }
                                ],
                                "status": {
                                    "name": "In Progress"
                                },
                                "id": "469166",
                                "price": "60.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$60.00",
                                "device": {
                                    "id": "153216",
                                    "name": "All"
                                },
                                "assigned_to": {
                                    "id": "1755",
                                    "fullname": "Jonathan White"
                                },
                                "imei": "",
                                "due_on": 1499370540
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "409760",
                            "order_id": "T-1378",
                            "total": "$94.43",
                            "how_did_u_find_us": "",
                            "created_date": 1499302153,
                            "repair_collected": 1499238000,
                            "customer": {
                                "fullName": "Avrian Palomino",
                                "id": "777199",
                                "mobile": "+1 760-894-9799",
                                "address1": "",
                                "fullname": "Avrian",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD) White",
                                        "id": "892483"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "467545",
                                "price": "89.00",
                                "gst": "5.43",
                                "line_discount": "0.00",
                                "total": "$94.43",
                                "device": {
                                    "id": "137486",
                                    "name": "iPhone 6"
                                },
                                "assigned_to": {
                                    "id": "1769",
                                    "fullname": "Edgar Hernandez"
                                },
                                "imei": "356981063786249",
                                "due_on": 1499305680
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "409669",
                            "order_id": "T-1377",
                            "total": "$136.80",
                            "how_did_u_find_us": "",
                            "created_date": 1499297726,
                            "repair_collected": 1499238000,
                            "customer": {
                                "fullName": "Alex Alonso",
                                "id": "777133",
                                "mobile": "+1 760-464-1763",
                                "address1": "",
                                "fullname": "Alex",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD)",
                                        "id": "2013924"
                                    },
                                    {
                                        "name": " Frame Labor",
                                        "id": "931007"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "467442",
                                "price": "136.80",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$136.80",
                                "device": {
                                    "id": "139870",
                                    "name": "iPhone 6s"
                                },
                                "assigned_to": {
                                    "id": "1769",
                                    "fullname": "Edgar Hernandez"
                                },
                                "imei": "",
                                "due_on": 1499301240
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "409290",
                            "order_id": "T-1376",
                            "total": "$60.00",
                            "how_did_u_find_us": "",
                            "created_date": 1499276989,
                            "repair_collected": 1499238000,
                            "customer": {
                                "fullName": "Justiniano Rivera",
                                "id": "776826",
                                "mobile": "+1 760-578-8995",
                                "address1": "",
                                "fullname": "Justiniano",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Charging Port Replacement",
                                        "id": "1459281"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "466944",
                                "price": "60.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$60.00",
                                "device": {
                                    "id": "212069",
                                    "name": "Samsung Tab Note 10.1 SM-P600"
                                },
                                "assigned_to": {
                                    "id": "1769",
                                    "fullname": "Edgar Hernandez"
                                },
                                "imei": "",
                                "due_on": 1499280480
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "406425",
                            "order_id": "T-1372",
                            "total": "$100.00",
                            "how_did_u_find_us": "",
                            "created_date": 1499132159,
                            "repair_collected": -62169955200,
                            "customer": {
                                "fullName": "Alvarro Leon",
                                "id": "774195",
                                "mobile": "+1 760-238-1303",
                                "address1": "",
                                "fullname": "Alvarro",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Battery",
                                        "id": "2007462"
                                    }
                                ],
                                "status": {
                                    "name": "In Progress"
                                },
                                "id": "463713",
                                "price": "100.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$100.00",
                                "device": {
                                    "id": "137476",
                                    "name": "iPad Air"
                                },
                                "assigned_to": {
                                    "id": "1798",
                                    "fullname": "King Amaya"
                                },
                                "imei": "",
                                "due_on": 1499131380
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "406319",
                            "order_id": "T-1371",
                            "total": "$75.27",
                            "how_did_u_find_us": "",
                            "created_date": 1499126309,
                            "repair_collected": 1499065200,
                            "customer": {
                                "fullName": "Delores Iniguez",
                                "id": "774169",
                                "mobile": "+1 760-676-6830",
                                "address1": "",
                                "fullname": "Delores",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Charging Port Replacement",
                                        "id": "1459288"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463580",
                                "price": "61.50",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$61.50",
                                "device": {
                                    "id": "212070",
                                    "name": "Galaxy Tab A 8 Inch SM-T350"
                                },
                                "assigned_to": {
                                    "id": "1755",
                                    "fullname": "Jonathan White"
                                },
                                "imei": "",
                                "due_on": 1499129760
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "406290",
                            "order_id": "T-1370",
                            "total": "$291.90",
                            "how_did_u_find_us": "",
                            "created_date": 1499124618,
                            "repair_collected": 1499065200,
                            "customer": {
                                "fullName": "Jacob Jemenez",
                                "id": "774150",
                                "mobile": "+1 760-625-4199",
                                "address1": "",
                                "fullname": "Jacob",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen Replacement",
                                        "id": "1732094"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463545",
                                "price": "275.00",
                                "gst": "16.90",
                                "line_discount": "0.00",
                                "total": "$291.90",
                                "device": {
                                    "id": "176001",
                                    "name": "Galaxy Note 5"
                                },
                                "assigned_to": {
                                    "id": "1798",
                                    "fullname": "King Amaya"
                                },
                                "imei": "",
                                "due_on": 1499128080
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "406244",
                            "order_id": "T-1369",
                            "total": "$180.02",
                            "how_did_u_find_us": "",
                            "created_date": 1499121701,
                            "repair_collected": -62169955200,
                            "customer": {
                                "fullName": "Jerry Nava",
                                "id": "444887",
                                "mobile": "+1 760-485-9881",
                                "address1": "",
                                "fullname": "Jerry",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": "+1 760-899-2993"
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD) Black",
                                        "id": "892482"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463489",
                                "price": "89.00",
                                "gst": "5.43",
                                "line_discount": "0.00",
                                "total": "$94.43",
                                "device": {
                                    "id": "137486",
                                    "name": "iPhone 6"
                                },
                                "assigned_to": {
                                    "id": "1798",
                                    "fullname": "King Amaya"
                                },
                                "imei": "",
                                "due_on": 1499125140
                            },
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD) White",
                                        "id": "892453"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463490",
                                "price": "70.00",
                                "gst": "4.81",
                                "line_discount": "0.00",
                                "total": "$74.81",
                                "device": {
                                    "id": "137484",
                                    "name": "iPhone 5"
                                },
                                "assigned_to": {
                                    "id": "1798",
                                    "fullname": "King Amaya"
                                },
                                "imei": "",
                                "due_on": ""
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "406235",
                            "order_id": "T-1368",
                            "total": "$130.00",
                            "how_did_u_find_us": "",
                            "created_date": 1499120798,
                            "repair_collected": 1499238000,
                            "customer": {
                                "fullName": "Jesenia Santos",
                                "id": "774096",
                                "mobile": "+1 760-989-2577",
                                "address1": "",
                                "fullname": "Jesenia",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Backlight IC Repair",
                                        "id": "1402165"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463475",
                                "price": "130.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$130.00",
                                "device": {
                                    "id": "137486",
                                    "name": "iPhone 6"
                                },
                                "assigned_to": {
                                    "id": "1755",
                                    "fullname": "Jonathan White"
                                },
                                "imei": "359234064286299",
                                "due_on": 1499124300
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "406220",
                            "order_id": "T-1367",
                            "total": "$30.00",
                            "how_did_u_find_us": "",
                            "created_date": 1499119451,
                            "repair_collected": -62169955200,
                            "customer": {
                                "fullName": "Angelica Sanchez",
                                "id": "774082",
                                "mobile": "+1 714-615-1550",
                                "address1": "",
                                "fullname": "Angelica",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Factory Reset",
                                        "id": "1071142"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463453",
                                "price": "20.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$20.00",
                                "device": {
                                    "id": "153216",
                                    "name": "All"
                                },
                                "assigned_to": {
                                    "id": "1755",
                                    "fullname": "Jonathan White"
                                },
                                "imei": "",
                                "due_on": 1499122800
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "406191",
                            "order_id": "T-1366",
                            "total": "$141.80",
                            "how_did_u_find_us": "",
                            "created_date": 1499117133,
                            "repair_collected": 1499151600,
                            "customer": {
                                "fullName": "Shawna Vandeneurg",
                                "id": "774055",
                                "mobile": "+1 760-799-8231",
                                "address1": "",
                                "fullname": "Shawna",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD) White",
                                        "id": "962068"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463415",
                                "price": "135.00",
                                "gst": "6.80",
                                "line_discount": "0.00",
                                "total": "$141.80",
                                "device": {
                                    "id": "141411",
                                    "name": "Iphone 6s Plus"
                                },
                                "assigned_to": {
                                    "id": "1798",
                                    "fullname": "King Amaya"
                                },
                                "imei": "",
                                "due_on": 1499120700
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "406150",
                            "order_id": "T-1365",
                            "total": "$20.00",
                            "how_did_u_find_us": "",
                            "created_date": 1499114446,
                            "repair_collected": 1499065200,
                            "customer": {
                                "fullName": "Stephanie Chavez",
                                "id": "774022",
                                "mobile": "+1 760-989-9120",
                                "address1": "",
                                "fullname": "Stephanie",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Factory Reset",
                                        "id": "1071142"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463359",
                                "price": "20.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$20.00",
                                "device": {
                                    "id": "153216",
                                    "name": "All"
                                },
                                "assigned_to": {
                                    "id": "1755",
                                    "fullname": "Jonathan White"
                                },
                                "imei": "355695074552850",
                                "due_on": 1499118000
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "405983",
                            "order_id": "T-1361",
                            "total": "$94.43",
                            "how_did_u_find_us": "",
                            "created_date": 1499105796,
                            "repair_collected": 1499065200,
                            "customer": {
                                "fullName": "Gabriel Arambula",
                                "id": "773876",
                                "mobile": "+1 760-625-9254",
                                "address1": "",
                                "fullname": "Gabriel",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD) Black",
                                        "id": "892482"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "463146",
                                "price": "89.00",
                                "gst": "5.43",
                                "line_discount": "0.00",
                                "total": "$94.43",
                                "device": {
                                    "id": "137486",
                                    "name": "iPhone 6"
                                },
                                "assigned_to": {
                                    "id": "1798",
                                    "fullname": "King Amaya"
                                },
                                "imei": "354411060232478",
                                "due_on": 1499109300
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "403756",
                            "order_id": "T-1360",
                            "total": "$145.99",
                            "how_did_u_find_us": "",
                            "created_date": 1498940031,
                            "repair_collected": 1498892400,
                            "customer": {
                                "fullName": "Brad Leclerc",
                                "id": "771964",
                                "mobile": "+1 760-996-1547",
                                "address1": "",
                                "fullname": "Brad",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD) Black",
                                        "id": "942047"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "460671",
                                "price": "140.60",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$140.60",
                                "device": {
                                    "id": "141411",
                                    "name": "Iphone 6s Plus"
                                },
                                "assigned_to": {
                                    "id": "1769",
                                    "fullname": "Edgar Hernandez"
                                },
                                "imei": "353288070054543",
                                "due_on": 1498943580
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "403747",
                            "order_id": "T-1359",
                            "total": "$41.60",
                            "how_did_u_find_us": "",
                            "created_date": 1498939269,
                            "repair_collected": 1499065200,
                            "customer": {
                                "fullName": "Hugo Leyea",
                                "id": "170866",
                                "mobile": "+1 760-485-9952",
                                "address1": "",
                                "fullname": "Hugo",
                                "address2": "",
                                "orgonization": "",
                                "email": "hugo.leyea@aol.com",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "iPhone 6 Battery",
                                        "id": "892738"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "460659",
                                "price": "41.60",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$41.60",
                                "device": {
                                    "id": "137486",
                                    "name": "iPhone 6"
                                },
                                "assigned_to": {
                                    "id": "1769",
                                    "fullname": "Edgar Hernandez"
                                },
                                "imei": "354449068109421",
                                "due_on": 1498942800
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "402772",
                            "order_id": "T-1358",
                            "total": "$72.33",
                            "how_did_u_find_us": "",
                            "created_date": 1498873858,
                            "repair_collected": 1498806000,
                            "customer": {
                                "fullName": "Rafael Davalos",
                                "id": "131062",
                                "mobile": "+1 442-324-6063",
                                "address1": "",
                                "fullname": "Rafael",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD) Replacement",
                                        "id": "892522"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "459531",
                                "price": "70.00",
                                "gst": "2.33",
                                "line_discount": "0.00",
                                "total": "$72.33",
                                "device": {
                                    "id": "137492",
                                    "name": "iPhone 5C"
                                },
                                "assigned_to": {
                                    "id": "1798",
                                    "fullname": "King Amaya"
                                },
                                "imei": "",
                                "due_on": 1498877400
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "402738",
                            "order_id": "T-1357",
                            "total": "$95.42",
                            "how_did_u_find_us": "",
                            "created_date": 1498872170,
                            "repair_collected": 1498806000,
                            "customer": {
                                "fullName": "Jasmine Padilla",
                                "id": "770994",
                                "mobile": "+1 760-972-8997",
                                "address1": "",
                                "fullname": "Jasmine",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": "+1 760-899-9657"
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Screen (Digitizer+LCD) White",
                                        "id": "892483"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "459489",
                                "price": "89.99",
                                "gst": "5.43",
                                "line_discount": "0.00",
                                "total": "$95.42",
                                "device": {
                                    "id": "137486",
                                    "name": "iPhone 6"
                                },
                                "assigned_to": {
                                    "id": "1798",
                                    "fullname": "King Amaya"
                                },
                                "imei": "",
                                "due_on": 1498875180
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "402719",
                            "order_id": "T-1356",
                            "total": "$70.00",
                            "how_did_u_find_us": "",
                            "created_date": 1498871167,
                            "repair_collected": -62169955200,
                            "customer": {
                                "fullName": "Juan Romero",
                                "id": "770986",
                                "mobile": "+1 760-625-5442",
                                "address1": "",
                                "fullname": "Juan",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": ""
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "Factory Reset Protection Removal",
                                        "id": "1026182"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "459467",
                                "price": "60.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$60.00",
                                "device": {
                                    "id": "153216",
                                    "name": "All"
                                },
                                "assigned_to": {
                                    "id": "1755",
                                    "fullname": "Jonathan White"
                                },
                                "imei": "",
                                "due_on": 1498874700
                            }
                        ]
                    },
                    {
                        "summary": {
                            "id": "402651",
                            "order_id": "T-1354",
                            "total": "$100.00",
                            "how_did_u_find_us": "",
                            "created_date": 1498868067,
                            "repair_collected": 1499065200,
                            "customer": {
                                "fullName": "Luis Alvarez",
                                "id": "118960",
                                "mobile": "+1 760-620-4299",
                                "address1": "",
                                "fullname": "Luis",
                                "address2": "",
                                "orgonization": "",
                                "email": "",
                                "phone": "+1 760-534-2162"
                            }
                        },
                        "devices": [
                            {
                                "repairProdItems": [
                                    {
                                        "name": "IMEI Repair",
                                        "id": "1071151"
                                    }
                                ],
                                "status": {
                                    "name": "Repaired & Collected"
                                },
                                "id": "459381",
                                "price": "100.00",
                                "gst": "0.00",
                                "line_discount": "0.00",
                                "total": "$100.00",
                                "device": {
                                    "id": "153216",
                                    "name": "All"
                                },
                                "assigned_to": {
                                    "id": "1755",
                                    "fullname": "Jonathan White"
                                },
                                "imei": "",
                                "due_on": 1498871580
                            }
                        ]
                    }
                ],
                "TotalRecords": "58",
                "fromDate": 1498288920
            }
        }
        i = 0
        for a, b in zip(ticket_object, ticket_data):
            # print (a + "| " + b)
            pass
