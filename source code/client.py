import pickle
import socket
import json

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

mysock.connect(('localhost',3518))

print("----- WELCOME TO STOCK & FX MARKETS QUICK QUERY SYSTEM -----")
area = input("SELECT YOUR AREA (PRESS 1 FOR STOCKS, PRESS 2 FOR FX): ")
company = ""
selection = ""
date = ""
inputs_to_send = ""

if area == "1":
    company = input('Input company symbol that you are interested in the market(MSFT,IBM,AAPL etc.): ')
    selection = input("SELECT FROM MENU\n" +
                    "1.COMPANY OVERVİEW\n" + 
                    "2.DAILY PRICE INFO\n")
    
    if selection == "2":
        date = input('Input date(year-day-month):')
        func = "TIME_SERIES_DAILY"
        inputs_to_send = [area,selection,func,company,date]

    elif selection == "1":
        func = "OVERVIEW"
        inputs_to_send = [area,selection,func,company]

elif area == "2":
    selection = input("SELECT FROM MENU\n" +
                    "1.EXCHANGE RATE INFO\n" + 
                    "2.FOREX DAILY PRICES INFO\n")
    
    if selection == "1":
        func = "CURRENCY_EXCHANGE_RATE"
        base_currency = input("From Symbol:(USD, EUR, TRY etc.:) ")
        target_currency = input("To Symbol:(USD, EUR, TRY etc.:)" )
        inputs_to_send = [area,selection,func,base_currency,target_currency]
    
    elif selection == "2":
        func = "FX_DAILY"
        base_currency = input("From Symbol:(USD, EUR, TRY etc.:) ")
        target_currency = input("To Symbol:(USD, EUR, TRY etc.:)" )
        date = input("Input date:")
        inputs_to_send = [area,selection,func,base_currency,target_currency,date]

input_bytes = pickle.dumps(inputs_to_send)

mysock.send(input_bytes)

while True:
    data = mysock.recv(2048)
    if len(data) < 1:
        break
    
    data = pickle.loads(data)

    if area == "1":
        if selection == "1":
            print("Industry:" + data[0])
            print('----')
            print("Name:" + data[1])
            print('----')
            print("Country:" + data[2])
            print('----')
            print("Description:" + data[3])
            print('----')
            print("Currency:" + data[4])
            print("\n")

        if selection == "2":
            print("-----" + company + "-----")
            print('1. open: ' + data[0])
            print('2. high: ' + data[1])
            print('3. low: ' + data[2])
            print('4. close: ' + data[3])
            print('5. volume: ' + data[4])
    
    elif area == "2":
        if selection == "1":
            print(data[0] + " = " + data[2] + " " + data[1])
        
        if selection == "2":
            print('1. open: ' + data[0])
            print('2. high: ' + data[1])
            print('3. low: ' + data[2])
            print('4. close: ' + data[3])

mysock.close()