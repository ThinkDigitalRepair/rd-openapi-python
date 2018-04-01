from unittest import TestCase
from repairdesk_api import RepairDesk
import jsonpickle

class TestRepairDesk(TestCase):
    def setUp(self):
        self.customers = []
        with open ('liliana.json', 'r') as file:
            self.customers = jsonpickle.decode(file.read())
    def test_merge(self):
        RepairDesk.merge(self.customers)
        pass
