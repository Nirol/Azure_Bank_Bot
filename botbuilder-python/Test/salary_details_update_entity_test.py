import unittest


from salary_details import SalaryDetails


class TestUpdateEntity(unittest.TestCase):


    def setUp(self):
        self.salary_details = SalaryDetails()

    def test_update_entity_1(self):
        self.salary_details.update_entity("net","Net")
        self.assertEqual(self.salary_details.net, "Net")

    def test_update_entity_2(self):
        self.salary_details.update_entity("gross", "Gross")
        self.assertEqual(self.salary_details.gross, "Gross")

    def test_update_entity_3(self):
        self.salary_details.update_entity("pay_type", "both")
        self.assertEqual(self.salary_details.pay_type, "both")


if __name__ == '__main__':
    unittest.main()