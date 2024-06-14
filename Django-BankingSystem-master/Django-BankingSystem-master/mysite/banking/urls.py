from django.urls import path

from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('insertdata',views.insertdata,name='insertdata'),
    path('transactions',views.transactions,name='transactions'),
    path('customers',views.customers,name='customers'),
    path('transfer',views.transfer,name='transfer'),
    path('contacts',views.contacts,name='contacts'),
]