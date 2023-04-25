from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, OperationalError
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from sign import models
from util.convert import convert


# Create your views here.


@login_required(login_url='/sign/login/')
def index(request):
    curr_user = models.User.objects.get(username=request.user)
    users = models.User.objects.all()
    return render(request, 'transact/index.html', locals())


@login_required(login_url='/sign/login/')
def search(request):
    curr_user = models.User.objects.get(username=request.user)
    target_email = request.GET.get('email')
    result = models.User.objects.filter(email=target_email)
    if result:
        self_check = curr_user.email != target_email
        if self_check:
            target_user = models.User.objects.get(email=target_email)
        else:
            return render(request, 'transact/search.html', locals())
    else:
        return render(request, 'transact/search.html', locals())
    return render(request, 'transact/search.html', locals())


@login_required(login_url='/sign/login/')
@xframe_options_sameorigin
def pay(request):
    curr_user = models.User.objects.get(username=request.user)
    target_user = models.User.objects.get(username=request.GET.get('target_user'))
    amount = request.GET.get('amount')
    curr_currency = curr_user.currency
    target_currency = target_user.currency
    unit = request.GET.get('unit')
    business_type = request.GET.get('business_type')
    balance = curr_user.balance
    if business_type == 'pay':
        from_amount = convert('http://3.88.160.124:8000', unit, curr_currency, amount)
        pay_condition = (from_amount <= balance)
        if pay_condition:
            try:
                with transaction.atomic():
                    curr_user.balance -= from_amount
                    to_amount = convert('http://3.88.160.124:8000', unit, target_currency, amount)
                    target_user.balance += to_amount
                    success_tag = True
                    curr_user.transactions += f'{curr_user.username}_{curr_user.currency}_{target_user.username}_{target_currency}_{amount}_{unit}_{business_type}_success_{datetime.now().strftime("%H:%M:%S %m/%d/%Y")},'
            except OperationalError:
                messages.info(request, f"Transfer operation is not possible now.")
        else:
            try:
                with transaction.atomic():
                    fail_tag = True
                    curr_user.transactions += f'{curr_user.username}_{curr_user.currency}_{target_user.username}_{target_currency}_{amount}_{unit}_{business_type}_fail_{datetime.now().strftime("%H:%M:%S %m/%d/%Y")},'
            except OperationalError:
                messages.info(request, f"Transfer operation is not possible now.")

    elif business_type == 'collect':
        try:
            with transaction.atomic():
                notification = f'{curr_user.username}_{amount}_{unit}_{datetime.now().strftime("%H:%M:%S %m/%d/%Y")},'
                curr_user.transactions += f'{curr_user.username}_{curr_user.currency}_{target_user.username}_{target_currency}_{amount}_{unit}_{business_type}_pending_{datetime.now().strftime("%H:%M:%S %m/%d/%Y")},'
                target_user.notifications += notification
                success_tag = True
        except OperationalError:
            messages.info(request, f"Transfer operation is not possible now.")
    curr_user.save()
    target_user.save()
    return render(request, 'transact/index.html', locals())


@login_required(login_url='/sign/login/')
def record(request):
    curr_user = models.User.objects.get(username=request.user)
    users = models.User.objects.all()
    transactions_list = list()
    for user in users:
        for transactions in user.transactions.split(',')[0:-1]:
            transactions_list.append(transactions)
    transactions_list = list(set(transactions_list))
    transactions_list = curr_user.get_unique_transactions(transactions_list)
    return render(request, 'transact/history.html', locals())


@login_required(login_url='/sign/login/')
def notify(request):
    curr_user = models.User.objects.get(username=request.user)
    notifications_list = curr_user.compile_notifications()
    return render(request, 'transact/notify.html', locals())


@login_required(login_url='/sign/login/')
@xframe_options_sameorigin
def handle_notification(request):
    curr_user = models.User.objects.get(username=request.user)
    option = request.GET.get('option')
    choice = option.split('_')[0]
    no = int(option.split('_')[1])
    target_username = option.split('_')[2]
    target_user = models.User.objects.get(username=target_username)
    notifications_list = curr_user.compile_notifications()
    target_notification = notifications_list[no - 1]
    curr_currency = curr_user.currency
    target_currency = target_user.currency
    amount = target_notification[2]
    unit = target_notification[3]
    fail_tag = False
    message = ''
    if choice == 'accept':
        to_amount = convert('http://3.88.160.124:8000', curr_currency, unit, amount)
        pay_condition = (to_amount <= curr_user.balance)
        if pay_condition:
            try:
                with transaction.atomic():
                    curr_user.balance -= to_amount
                    curr_user.transactions += f'{curr_user.username}_{curr_user.currency}_{target_user.username}_{target_currency}_{amount}_{unit}_collect_accept_{datetime.now().strftime("%H:%M:%S %m/%d/%Y")},'
                    target_user.transactions += f'{curr_user.username}_{curr_user.currency}_{target_user.username}_{target_currency}_{amount}_{unit}_collect_accept_{datetime.now().strftime("%H:%M:%S %m/%d/%Y")},'
            except OperationalError:
                messages.info(request, f"Transfer operation is not possible now.")
        else:
            try:
                with transaction.atomic():
                    fail_tag = True
                    message = 'Your balance is not enough!'
                    curr_user.transactions += f'{curr_user.username}_{curr_user.currency}_{target_user.username}_{target_currency}_{amount}_{unit}_collect_fail_{datetime.now().strftime("%H:%M:%S %m/%d/%Y")},'
            except OperationalError:
                messages.info(request, f"Transfer operation is not possible now.")

    elif option == 'decline':
        try:
            with transaction.atomic():
                curr_user.transactions += f'{curr_user.username}_{curr_user.currency}_{target_user.username}_{target_currency}_{amount}_{unit}_collect_decline_{datetime.now().strftime("%H:%M:%S %m/%d/%Y")},'
                target_user.transactions += f'{curr_user.username}_{curr_user.currency}_{target_user.username}_{target_currency}_{amount}_{unit}_collect_decline_{datetime.now().strftime("%H:%M:%S %m/%d/%Y")},'
        except OperationalError:
            messages.info(request, f"Transfer operation is not possible now.")
    if not fail_tag:
        notifications_list.remove(target_notification)
        curr_user.notifications = curr_user.build_notifications(notifications_list)
    curr_user.save()
    target_user.save()
    return render(request, 'transact/notify.html', locals())


@login_required(login_url='/sign/login/')
@xframe_options_sameorigin
def upgrade(request):
    curr_user = models.User.objects.get(username=request.user)
    users = models.User.objects.filter(is_superuser=False)
    target_user_username = request.GET.get('option')
    if target_user_username:
        target_user = models.User.objects.get(username=target_user_username)
        target_user.is_superuser = True
        target_user.save()
    return render(request, 'transact/upgrade.html', locals())
