from django.shortcuts import render
from .models import Balance
# Create your views here.
from django.db.models import F
from django import http
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.db import connection


def home(request):
    return render(request, 'banking/home.html')



def about(request):
    return render(request, 'banking/about.html')

def contacts(request):
    return render(request, 'banking/contacts.html')


def insertdata(request):
    if request.method == "GET":
        return render(request, 'banking/insertdata.html')
    elif request.method == "POST":
        name = request.POST['name1']
        email = request.POST['email1']
        balance = request.POST['balance1']
        bankid = request.POST['bankid1']
        with connection.cursor() as cursor:
            cursor.execute('select bankid from banking_balance')
            all_id = []
            for i in cursor.fetchall():
                all_id.append(i[0])
            if not bankid in all_id:
                cursor.execute('insert into banking_balance values(%s,%s,%s,%s)', (
                    name, email, balance, bankid))
            else:
                return HttpResponse('id should be unique')

        return HttpResponseRedirect('insertdata')

def transactions(request):
     with connection.cursor() as cursor:
        cursor.execute('select * from transactions')
        trans_tuple = cursor.fetchall()
        return render(request, 'banking/transactions.html', {'transaction': trans_tuple})

def transfer(request):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute('select name from banking_balance')
            cus_name = []
            for i in cursor.fetchall():
                cus_name.append(i[0])
            return render(request, 'banking/transfer.html', {'customer_name': cus_name})
    elif request.method == "POST":
        sender = request.POST['Sender1']
        receiver = request.POST['Receiver1']
        amount = int(request.POST['amount1'])
        with connection.cursor() as cursor:
            cursor.execute(
                "select balance from banking_balance where name = '%s'" % (sender))
            sender_balance = int(cursor.fetchall()[0][0])

        if int(sender_balance) >= int(amount):
            sender_new_balance = int(sender_balance) - int(amount)
            with connection.cursor() as cursor:
                update_sender_balance = "update banking_balance set BALANCE = %d where NAME = '%s'" % (
                    sender_new_balance, sender)
                cursor.execute(update_sender_balance)
                cursor.execute(
                    "select balance from banking_balance where name = '%s'" % (receiver))
                receiver_balance = cursor.fetchall()[0][0]
            receiver_new_balance = int(receiver_balance) + int(amount)
            with connection.cursor() as cursor:
                update_receiver_balance = "update banking_balance set Balance = %d where NAME = '%s'" % (
                    receiver_new_balance, receiver)
                cursor.execute(update_receiver_balance)
            with connection.cursor() as cursor:
                cursor.execute(
                    'insert into transactions (Sender,Receiver,Amount) values(%s,%s,%s)', (sender, receiver, amount))
            return HttpResponseRedirect('transfer')
        else:
            return HttpResponseRedirect('transactions')


def customers(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from banking_balance')
        detail_tuple = cursor.fetchall()
        return render(request, 'banking/customers.html', {'Balance': detail_tuple})

        
"""   if request.method == "GET":
        all_d=Balance.objects.all()
        return render(request, 'banking/transfer.html', {'customer_name': all_d})
    elif request.method == "POST":
        sender = request.POST['Sender1']
        receiver = request.POST['Rece1']
        amount = int(request.POST['amount1'])
        sender_balance=Balance.objects.raw('SELECT balance FROM banking_balance WHERE name = %s', [sender])
        if int(sender_balance) >= int(amount):
            sender_new_balance = int(sender_balance) - int(amount)
            receiverpre_balance=Balance.objects.raw('SELECT balance FROM banking_balance WHERE name = %s', [receiver])
            receiver_new_balance = int(receiverpre_balance) + int(amount)"""