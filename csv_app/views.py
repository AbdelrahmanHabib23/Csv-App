import csv
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.db.models import F
from .models import Account
from .forms import CSVUploadForm, TransferFundsForm

# Configure logging
logger = logging.getLogger(__name__)

def import_accounts(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                reader = csv.reader(file.read().decode('utf-8').splitlines())
                next(reader)  # Skip the header row
                successful_imports = 0
                accounts_to_create = []  # To store accounts before bulk creation

                with transaction.atomic():  # Ensure atomicity for bulk creation
                    for row in reader:
                        try:
                            ID, NAME, BALANCE = row
                            if not BALANCE.replace('.', '', 1).isdigit():
                                raise ValueError(f"Invalid balance value: {BALANCE}")
                            accounts_to_create.append(Account(name=NAME, balance=float(BALANCE)))
                        except ValueError as e:
                            messages.error(request, f"Error with account {NAME}: {e}")
                            logger.error(f"Error with account {NAME}: {e}")

                    if accounts_to_create:
                        Account.objects.bulk_create(accounts_to_create)
                        successful_imports = len(accounts_to_create)

                messages.success(request, f'Successfully imported {successful_imports} account(s)!')
                return redirect('list_accounts')
            except Exception as e:
                messages.error(request, f"Error importing file: {e}")
                logger.error(f"Error importing file: {e}")
        else:
            messages.error(request, "The form is not valid.")

    else:
        form = CSVUploadForm()

    return render(request, 'pages/import_accounts.html', {'form': form})


def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'pages/list_accounts.html', {'accounts': accounts})


def account_info(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    return render(request, 'pages/account_info.html', {'account': account})


def transfer_funds(request):
    if request.method == 'POST':
        form = TransferFundsForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']

            # Validate amount and account balances
            if amount <= 0:
                messages.error(request, "The transfer amount must be positive.")
                return render(request, 'pages/transfer_funds.html', {'form': form})

            if from_account.balance < amount:
                messages.error(request, "Insufficient balance in the selected account.")
                return render(request, 'pages/transfer_funds.html', {'form': form})

            try:
                # Update balances atomically using F expressions
                with transaction.atomic():
                    from_account.balance = F('balance') - amount
                    to_account.balance = F('balance') + amount

                    from_account.save()
                    to_account.save()

                messages.success(request, f"Successfully transferred ${amount:.2f} from {from_account.name} to {to_account.name}.")
                return redirect('success_url')  # Redirect to success page
            except IntegrityError as e:
                messages.error(request, "An error occurred during the transfer. Please try again.")
                logger.error(f"Error during fund transfer: {e}")
        else:
            messages.error(request, "The transfer form is invalid.")

    else:
        form = TransferFundsForm()

    return render(request, 'pages/transfer_funds.html', {'form': form})


def success_view(request):
    return render(request, 'pages/success_url.html')  # Assuming this is where you'll create the HTML
