import unittest

import intent.enums.pay_type_enum
from helpers import text_from_clients_helper


class TestTextFromClients(unittest.TestCase):

    def setUp(self):
        pass

    def test_missspelled_pay_type_from_user_gross_0(self):
        # score for gross is 1
        ans = text_from_clients_helper.fix_user_pay_type_input("gross")
        print(ans)
        self.assertEqual(intent.enums.pay_type_enum.PayType.GROSS, ans)

    def test_missspelled_pay_type_from_user_gross_1(self):
        # score for groos is 0.8
        ans = text_from_clients_helper.fix_user_pay_type_input("groos")
        print(ans)
        self.assertEqual(intent.enums.pay_type_enum.PayType.GROSS, ans)

    def test_missspelled_pay_type_from_user_gross_2(self):
        # score for groos is 0.8
        ans = text_from_clients_helper.fix_user_pay_type_input("gros")
        print(ans)
        self.assertEqual(intent.enums.pay_type_enum.PayType.GROSS, ans)

    def test_missspelled_pay_type_from_user_gross_3(self):
        # score for gorss is 0.8
        ans = text_from_clients_helper.fix_user_pay_type_input("gorss")
        print(ans)
        self.assertEqual(intent.enums.pay_type_enum.PayType.GROSS, ans)

    def test_missspelled_pay_type_from_user_gross_4(self):
        # score for gosssrrrss is 0.53
        ans = text_from_clients_helper.fix_user_pay_type_input("gosssrrrss")
        print(ans)
        self.assertEqual(intent.enums.pay_type_enum.PayType.GROSS, ans)

    def test_missspelled_pay_type_from_user_gross_5(self):
        # score for abc is < 0.53  (0)
        ans = text_from_clients_helper.fix_user_pay_type_input("abc")
        print(ans)
        self.assertEqual(intent.enums.pay_type_enum.PayType.NONE, ans)

    def test_missspelled_pay_type_from_user_net_1(self):
        # score for nt is  0.8
        ans = text_from_clients_helper.fix_user_pay_type_input("nt")
        print(ans)
        self.assertEqual(intent.enums.pay_type_enum.PayType.NET, ans)

    def test_missspelled_pay_type_from_user_net_2(self):
        # score for nte is  0.6666
        ans = text_from_clients_helper.fix_user_pay_type_input("nte")
        print(ans)
        self.assertEqual(intent.enums.pay_type_enum.PayType.NET, ans)

    def test_missspelled_pay_type_from_user_net_3(self):
        # score for ent is  0.6666
        ans = text_from_clients_helper.fix_user_pay_type_input("ent")
        print(ans)
        self.assertEqual(intent.enums.pay_type_enum.PayType.NET, ans)



if __name__ == '__main__':
    unittest.main()
