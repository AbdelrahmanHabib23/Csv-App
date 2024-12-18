from django.test import TestCase  
from .models import Account  

class AccountModelTests(TestCase):  
    def test_create_account(self):  
        account = Account.objects.create(name="Test Account", balance=100.00)  
        self.assertEqual(account.name, "Test Account")  
        self.assertEqual(account.balance, 100.00)  

class TransferFundsTest(TestCase):  
    def setUp(self):  
        self.account1 = Account.objects.create(name="Account 1", balance=200.00)  
        self.account2 = Account.objects.create(name="Account 2", balance=100.00)  

    def test_transfer_funds(self):  
        self.account1.balance -= 50  
        self.account2.balance += 50  
        self.account1.save()  
        self.account2.save()  
        
        self.assertEqual(self.account1.balance, 150.00)  
        self.assertEqual(self.account2.balance, 150.00)