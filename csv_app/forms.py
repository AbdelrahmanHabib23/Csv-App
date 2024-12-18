from django import forms
from .models import Account

# Form to upload a CSV file
class CSVUploadForm(forms.Form):
    file = forms.FileField()

# Form to transfer funds between accounts
class TransferFundsForm(forms.Form):  
    from_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="From Account")  
    to_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="To Account")  
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")