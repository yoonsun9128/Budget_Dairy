from django.db import models
from django.urls import reverse
from users.models import User


class Account(models.Model):
    Payment_Method = (
        ("카드","카드"),
        ("현금","현금"),
        ("이체","이체"),
        ("입금","입금")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="금액")
    memo = models.CharField(max_length=50)
    method = models.CharField(max_length=50, choices=Payment_Method)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.method

    def get_absolute_url(self):
        return reverse('accounts:AccountDetailView', kwargs={'account_id':self.id})
