from django.conf import settings
import requests
import json

class AirtelMoney:
    def baseUrl(self):
        if settings.DEBUG:
            return 'https://openapiuat.airtel.africa'
        else:
            return 'https://openapi.airtel.africa'

    def getAuthToken(self):
        url = f'{self.baseUrl()}/auth/oauth2/token'
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*'
        }
        data = {
            "client_id": settings.AIRTEL_CLIENT_ID,
            "client_secret": settings.AIRTEL_CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))  
            success = True if response.status_code == 200 else False
            return {"success": success, "data": response.json()}
        except Exception as ex:
            return {"success": False, "message": str(ex)}

    def collectMoney(self, accessToken, reference, customerPhoneNumber, amount, transactionId):
        url = f'{self.baseUrl()}/merchant/v1/payments/'
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'X-Country': 'UG',
            'X-Currency': 'UGX',
            'Authorization': f'Bearer {accessToken}'
        }
        data = {
            "reference": reference,
            "subscriber": {
                "country": "UG",
                "currency": "UGX",
                "msisdn": int(customerPhoneNumber)
            },
            "transaction": {
                "amount": int(amount),
                "country": "UG",
                "currency": "UGX",
                "id": transactionId
            }
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))  
            success = True if response.status_code == 200 else False
            return {"success": success, "data": response.json()}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def checkCollectionStatus(self, accessToken, id):
        url = f'{self.baseUrl()}/standard/v1/payments/{id}'
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'X-Country': 'UG',
            'X-Currency': 'UGX',
            'Authorization': f'Bearer {accessToken}'
        }
        
        try:
            response = requests.get(url, headers=headers)  
            statusCode = response.status_code
            success = True if statusCode == 200 else False
            return {
                "success": success, 
                "status": statusCode, 
                "data": response.json()
            }
        except Exception as e:
            return {
                "success":False,
                "status":500,
                "message":str(e)
            }

    def canReceiveMoney(self, accessToken, phoneNumber, amount, country='UGANDA', currency='UGX'):
        url = f'{self.baseUrl()}/openapi/moneytransfer/v2/validate'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {accessToken}'
        }
        data = {
            "amount": int(amount),
            "country": country,
            "currency": currency,
            "msisdn": phoneNumber
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))  
            responseBody = response.json()
            success = True if response.status_code == 200 else False
            return {
                "success": success, 
                "message": responseBody['message'], 
                "data": responseBody
            }
        except Exception as e:
            return {
                "success": False, 
                "message": str(e), 
                "data": {}
            }

    def transferMoney(self, accessToken, phoneNumber, amount, transactionId, country='UGANDA', currency='UGX'):
        url = f'{self.baseUrl()}/openapi/moneytransfer/v2/credit'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {accessToken}'
        }
        raw_pin = "1234" # airtel money pin of the payer
        encrypted_pin = self.encrypt(raw_pin) 
        
        data = {
            "amount": int(amount),
            "country": country,
            "currency": currency,
            "extTRID": transactionId,
            "msisdn": phoneNumber,
            "payerCountry": "UG",
            "payerFirstName": "Charles",
            "payerLastName": "Muhanzi",
            "pin": str(encrypted_pin)
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))  
            responseBody = response.json()
            if response.status_code == 200:
                if responseBody['status'] == "200":
                    success = True
                else:
                    success = False    
                message = responseBody['message']
            else:
                success = False
                message = responseBody['error']    
            return {
                "success": success, 
                "message": message, 
                "data": responseBody
            }
        except Exception as e:
            return {
                "success": False, 
                "message": str(e), 
                "data": {}
            }

    def checkTransferStatus(self, accessToken, transactionId, country='UGANDA'):
        base_url = self.baseUrl()    
        url = f'{base_url}/openapi/moneytransfer/v2/checkstatus'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {accessToken}'
        }
        data = {
            "country": country,
            "extTRID": transactionId
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))  
            statusCode = response.status_code
            responseBody = response.json()
            success = True if statusCode == 200 else False
            if success:
                message = responseBody['message']
            else:
                message = responseBody['error']    
            return {
                "success": success, 
                "status": statusCode,
                "message": message, 
                "data": response.json()
            }
        except Exception as e:
            return {
                "success":False,
                "status":500,
                "message":str(e)
            }

    def encrypt(self, pin=''):
        from base64 import b64decode, b64encode
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
        
        pubkey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkq3XbDI1s8Lu7SpUBP+bqOs/MC6PKWz6n/0UkqTiOZqKqaoZClI3BUDTrSIJsrN1Qx7ivBzsaAYfsB0CygSSWay4iyUcnMVEDrNVOJwtWvHxpyWJC5RfKBrweW9b8klFa/CfKRtkK730apy0Kxjg+7fF0tB4O3Ic9Gxuv4pFkbQIDAQAB"
        
        msg = pin
        keyDER = b64decode(pubkey)
        keyPub = RSA.importKey(keyDER)
        cipher = Cipher_PKCS1_v1_5.new(keyPub)
        cipher_text = cipher.encrypt(msg.encode())
        emsg = b64encode(cipher_text).decode('utf-8')
        print(f'Encrypted Pin:  {emsg}')
        return emsg
