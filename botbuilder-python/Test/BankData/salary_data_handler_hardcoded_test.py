import unittest

from db_hardcoded_imp import DBHardcoded
from db_intent_enum import DBIntent

from pay_type_enum import PayType
from salary_data_handler import SalaryDataHandler



class TestSalaryDataHandlerHardcoded(unittest.TestCase):

    def setUp(self):
        self.DB = DBHardcoded()
        self.DB_handler = SalaryDataHandler(self.DB)

    def test_get_salary_info_LAST_NET(self):
        salary_text = self.DB_handler.find_salary_data(DBIntent.LAST.value, PayType.NET.value)
        self.assertEqual(salary_text, 17000)


    def test_get_salary_info_LAST_GROSS(self):
        salary_text = self.DB_handler.find_salary_data(DBIntent.LAST.value,
                                                       PayType.GROSS.value)
        self.assertEqual(salary_text, 24000)

    def test_get_salary_info_pay_type_AVG_Net(self):
        salary_text = self.DB_handler.find_salary_data(DBIntent.AVG.value,
                                                       PayType.NET.value)
        self.assertEqual(salary_text, 16780.11)




if __name__ == '__main__':
    unittest.main()
