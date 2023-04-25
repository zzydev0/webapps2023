from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    # common attributes
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    created_time = models.DateTimeField(auto_now_add=True)
    # attributes for normal user
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    currency = models.CharField(max_length=16, default='GBP')
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=1000.00)
    notifications = models.CharField(max_length=256, default='')
    transactions = models.CharField(max_length=256, default='')

    class Meta:
        db_table = 'users'
        verbose_name = 'User Management'
        verbose_name_plural = verbose_name

    def compile_transactions(self):
        transactions = str(self.transactions)
        if transactions != '':
            compiled_list = list()
            transactions_list = transactions.split(',')[0:-1]
            for i in range(len(transactions_list)):
                no = i + 1
                transactions = transactions_list[i]
                items = transactions.split('_')
                from_user = items[0]
                from_currency = items[1]
                to_user = items[2]
                to_currency = items[3]
                amount = items[4]
                unit = items[5]
                operation_type = items[6]
                status = items[7]
                time = items[8]
                compiled_list.append(
                    (no, from_user, from_currency, to_user, to_currency, amount, unit, operation_type, status, time)
                )
            return compiled_list

    def get_unique_transactions(self, transactions_list):
        str(self.transactions)
        result = list()
        for i in range(len(transactions_list)):
            no = i + 1
            transactions = transactions_list[i]
            items = transactions.split('_')
            from_user = items[0]
            from_currency = items[1]
            to_user = items[2]
            to_currency = items[3]
            amount = items[4]
            unit = items[5]
            operation_type = items[6]
            status = items[7]
            time = items[8]
            result.append(
                (no, from_user, from_currency, to_user, to_currency, amount, unit, operation_type, status, time)
            )
        return result

    def compile_notifications(self):
        notifications = str(self.notifications)
        if notifications != '':
            compiled_list = list()
            notifications_list = notifications.split(',')[0:-1]
            for i in range(len(notifications_list)):
                no = i + 1
                notification = notifications_list[i]
                items = notification.split('_')
                from_user = items[0]
                amount = items[1]
                unit = items[2]
                time = items[3]
                compiled_list.append((no, from_user, amount, unit, time))
            return compiled_list

    def build_notifications(self, compiled_list):
        notifications = self.notifications
        res = ''
        for items in compiled_list:
            n = len(items)
            for i in range(1, n - 1):
                res += items[i]
                res += '_'
            res += items[n - 1]
            res += ','
        return res

    def get_nn(self):
        notifications = str(self.notifications)
        if notifications != '':
            notifications = str(notifications).split(',')
            return len(notifications) - 1
        else:
            return 0

    def get_part_of_day(self):
        time = self.created_time
        h = int(datetime.now().hour)
        return (
            "Morning"
            if 5 <= h <= 11
            else "Afternoon"
            if 12 <= h <= 17
            else "Evening"
            if 18 <= h <= 22
            else "Night"
        )
