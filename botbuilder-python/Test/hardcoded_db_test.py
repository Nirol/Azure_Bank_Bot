import unittest

from db_hardcoded_imp import DBHardcoded


class TestDBHardCode(unittest.TestCase):


    def setUp(self):
        self.hardcoded_db = DBHardcoded()

    def test_get_bonus(self):
        bonus = self.hardcoded_db.get_bonus()
        self.assertEqual(bonus, 570)

    def test_find_salary_data_1(self):
        last_salary = self.hardcoded_db.find_salary_data("LAST","net")
        self.assertEqual(last_salary, 17000)

    def test_find_salary_data_2(self):
        last_salary = self.hardcoded_db.find_salary_data("AVG","net")
        self.assertEqual(last_salary, 16780.11)

    def test_find_salary_data_3(self):
        last_salary = self.hardcoded_db.find_salary_data("YTD","gross")
        self.assertEqual(last_salary, 97612)


if __name__ == '__main__':
    unittest.main()