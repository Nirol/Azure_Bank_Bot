import unittest

from db_hardcoded_imp import DBHardcoded
from intent_helper import Intent
from salary_data_handler import SalaryDataHandler
from salary_details import SalaryDetails


class TestSalaryDataHandler(unittest.TestCase):

    def setUp(self):
        self.DB = DBHardcoded()
        self.DB_handler = SalaryDataHandler(self.DB)
        self.salary_details = SalaryDetails()

    def test_get_salary_info_net(self):
        self.salary_details.intent = Intent.LAST_SALARY.value
        self.salary_details.net = "Net"
        salary_text = self.DB_handler.get_salary_info(self.salary_details)
        self.assertEqual(salary_text, 'Your LAST net salary was=17000')

    def test_get_salary_info_gross(self):
        self.salary_details.intent = Intent.LAST_SALARY.value
        self.salary_details.net = "Gross"
        salary_text = self.DB_handler.get_salary_info(self.salary_details)
        self.assertEqual(salary_text, 'Your LAST gross salary was=24000')

    def test_get_salary_info_pay_type_net(self):
        self.salary_details.intent = Intent.LAST_SALARY.value
        self.salary_details.pay_type = "net"
        salary_text = self.DB_handler.get_salary_info(self.salary_details)
        self.assertEqual(salary_text, 'Your LAST net salary was=17000')

    def test_get_salary_info_pay_type_Net(self):
        self.salary_details.intent = Intent.LAST_SALARY.value
        self.salary_details.pay_type = "Net"
        salary_text = self.DB_handler.get_salary_info(self.salary_details)
        self.assertEqual(salary_text, 'Your LAST net salary was=17000')

    def test_get_salary_info_pay_type_both(self):
        self.salary_details.intent = Intent.LAST_SALARY.value
        self.salary_details.pay_type = "both"
        salary_text = self.DB_handler.get_salary_info(self.salary_details)
        expected_string = 'Your LAST net salary was=17000' + "\n" + 'Your LAST gross salary was=24000'
        self.assertEqual(salary_text,expected_string )


if __name__ == '__main__':
    unittest.main()
