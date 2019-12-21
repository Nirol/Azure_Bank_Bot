from enum import Enum


class Intent(Enum):
    AVG_SALARY = "Bank_PayCheck_CheckAvgSalary"
    YTD_SALARY = "Bank_PayCheck_CheckSalaryYTD"
    LAST_SALARY = "Bank_PayCheck_CheckLastSalary"
    BONUS = "Bank_PayCheck_CheckLastBonus"
    GENERAL_SALARY = "Bank_PayCheck_Salary"
    NONE_INTENT = "NoneIntent"
