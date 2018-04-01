import requests, json

def put_customer(customer):
    return put(url_string_snippet="customers/{0}".format(customer['cid']), data=customer)


def put(url_string_snippet, data):
    api_key = "mUz8SpB-hyAO-HMxe-NQC9-Gy5oqQ1IR"
    payload = {'api_key': api_key}
    base_url = "https://api.repairdesk.co/api/web/v1/"
    print(base_url + url_string_snippet + "{0}".format(payload))
    print("data = {0}".format(data))
    return requests.put(base_url + url_string_snippet, params=payload, json=data)


if __name__ == "__main__":
    customer = {"cid": "141675", "first_name": "Ozzy ", "last_name": "Rendon", "phone": "", "mobile": "+1 760-412-0642", "address1": "", "address2": "", "postcode": "", "city": "", "state": "", "country": "", "email": "", "orgonization": "", "refered_by": "", "driving_licence": "", "contact_person": "", "tax_number": "", "network": "T-Mobile (Think Digital)", "customer_group": {"id": "1", "name": "Individual"}}
    print(customer)
    #customer['first_name'] = "Test"
    #customer['last_name'] = "Test"
    print(customer)
    result = put_customer(customer)
    print(result.text)  # responds that customer was updated, but returns non-updated value.
