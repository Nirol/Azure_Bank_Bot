import unittest

import intent_helper
import text_from_clients_helper
from db_intent_enum import DBIntent
from general_salary_details import GeneralSalaryDetails



class TestSalaryDataHandler(unittest.TestCase):

    def setUp(self):

        self.general_salary_details = GeneralSalaryDetails()

    def test_is_total_salary_1(self):
        self.general_salary_details.salary_type="TOTAL"
        result = intent_helper.is_total_salary(self.general_salary_details.salary_type)
        self.assertEqual(False, result)

    def test_is_total_salary_2(self):
        self.general_salary_details.salary_type=DBIntent.TOTAL
        result = intent_helper.is_total_salary(self.general_salary_details.salary_type)
        self.assertEqual(True, result)

    def test_fix_user_salary_type_input(self):
        user_input_salary_type = "avrg"
        intent_result = text_from_clients_helper.fix_user_salary_type_input(
            user_input_salary_type)
        print(intent_result)
        self.assertEqual(DBIntent.AVG, intent_result)




if __name__ == '__main__':
    unittest.main()
