import unittest
from db_hardcoded_imp import DBHardcoded
from db_intent_enum import DBIntent
from pay_type_enum import PayType
from salary_data_handler import SalaryDataHandler
from text_to_clients_helper import get_pay_type_salary_massage, get_both_pay_type_salary_massage,get_both_pay_type_total_salary_massage


class TestSalaryDataHandler(unittest.TestCase):

    def setUp(self):
        self.DB = DBHardcoded()
        self.DB_handler = SalaryDataHandler(self.DB)

    def test_get_salary_info_LAST_NET(self):
        salary_text = get_pay_type_salary_massage( self.DB_handler, DBIntent.LAST.value,  PayType.NET.value)
        self.assertEqual(salary_text, 'Your LAST net salary was=17000')

    def test_get_salary_info_LAST_GROSS(self):
        salary_text = get_pay_type_salary_massage( self.DB_handler, DBIntent.LAST.value,  PayType.GROSS.value)
        self.assertEqual(salary_text, 'Your LAST gross salary was=24000')

    def test_get_salary_info_pay_type_AVG_Net(self):
        salary_text = get_pay_type_salary_massage( self.DB_handler, DBIntent.AVG.value,  PayType.NET.value)
        self.assertEqual(salary_text, 'Your AVG net salary was=16780.11')

    def test_get_salary_info_pay_type_both(self):
        salary_text = get_both_pay_type_salary_massage( self.DB_handler, DBIntent.LAST.value)
        expected_string = 'Your LAST net salary was=17000' + "\n" + 'Your LAST gross salary was=24000'
        self.assertEqual(salary_text,expected_string )

    def test_get_both_pay_type_total_salary_message(self):
        res = get_both_pay_type_total_salary_massage(
            self.DB_handler)
        expected_string = "Overall net Salary data:\nYour AVG net salary was=16780.11\nYour YTD net salary was=76345\nYour LAST net salary was=17000\nOverall gross Salary data:\nYour AVG gross salary was=23671.23\nYour YTD gross salary was=97612\nYour LAST gross salary was=24000"
        self.assertEqual(expected_string, res)



if __name__ == '__main__':
    unittest.main()
