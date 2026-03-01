'''
   1. Ask your name, email, phone, payment method
    2. Ask users items to add to cart and price
    3 Display total of the prices
    4.     Order confirmed
    5. Repeat if user want to purchase again
'''

userDetails = {}
priceDetails = {}
total = 0
print('Enter zzz to exit ')


while (True):
    name = input("Enter user name")
    email = input("Enter email")
    phone = input("Enter phone number")
    payment = input("Enter your payment method")
    if(name == 'zzz' or email == 'zzz' or phone == 'zzz' or payment == 'zzz'):
        break
    
    userDetails ={
        'name' :name,
        'email':email,
        'phone':phone,
        'payment':payment
    }
        # userDetails['name'] = name
        # userDetails['email'] = email
        # userDetails['phone'] = phone
        # userDetails['payment'] = payment

    while(True):
        item = input('Item name')
        priceStr = (input('Price: '))


        if(item == 'zzz' or priceStr == 'zzz'):
            break

        priceDetails[item] = int(priceStr)
        total +=int(priceStr)

    wantToContinue = input("Want to continue : Y/N ")
    if(wantToContinue == 'N'):
        break

print(userDetails, "\n", priceDetails, "\n", total)


