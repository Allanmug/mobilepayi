from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils.AirtelMoney import AirtelMoney
from django.conf import settings
import uuid

def home(request):
    return render(request, 'payments/home.html')

def collect_money(request):
    if request.method == 'POST':
        reference = request.POST['reference']
        customer_phone_number = request.POST['phone_number']
        amount = request.POST['amount']
        transaction_id = str(uuid.uuid4())

        airtel = AirtelMoney()
        token_response = airtel.getAuthToken()
        if token_response['success']:
            access_token = token_response['data']['access_token']
            collection_response = airtel.collectMoney(
                accessToken=access_token,
                reference=reference,
                customerPhoneNumber=customer_phone_number,
                amount=amount,
                transactionId=transaction_id
            )
            if collection_response['success']:
                return JsonResponse({'success': True, 'message': 'Payment initiated successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Payment initiation failed'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to obtain access token'})

    return render(request, 'payments/collect_money.html')

def transfer_money(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        amount = request.POST['amount']
        transaction_id = str(uuid.uuid4())

        airtel = AirtelMoney()
        token_response = airtel.getAuthToken()
        if token_response['success']:
            access_token = token_response['data']['access_token']
            transfer_response = airtel.transferMoney(
                accessToken=access_token,
                phoneNumber=phone_number,
                amount=amount,
                transactionId=transaction_id
            )
            if transfer_response['success']:
                return JsonResponse({'success': True, 'message': 'Transfer initiated successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Transfer initiation failed'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to obtain access token'})

    return render(request, 'payments/transfer_money.html')
