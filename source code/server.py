from socket import *;
import json
import pickle
import http.client

def postman_get_request(query):
    conn = http.client.HTTPSConnection("www.alphavantage.co")
    payload = ''
    headers = {}
    conn.request("GET", query, payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data.decode("utf-8"))
    #data.decode("utf-8")
    return data

def construct_stock_query(company,function):
    query = "/query?function=" + function + "&symbol=" + company + "&apikey=HPECJTEH87ZBVC1N"
    return query

def construct_fx_exchange_query(func,base,target):
    query = "/query?function=" + func + "&from_currency=" + base + "&to_currency=" + target + "&apikey=HPECJTEH87ZBVC1N"
    return query

def construct_fx_price_query(func,base,target):
    query = "/query?function=" + func + "&from_symbol=" + base + "&to_symbol=" + target + "&apikey=HPECJTEH87ZBVC1N"
    return query

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind(('localhost', 3518))
    serversocket.listen(5)

    while(1):
        (clientsocket, address) = serversocket.accept()
        inputs = clientsocket.recv(2048)
        inputs = pickle.loads(inputs)
        
        byte_stream = ""

        if inputs[0] == "1": #stock markets
            if inputs[1] == "1": #company overview
                query = construct_stock_query(company=inputs[3], function=inputs[2])
                data = postman_get_request(query=query)
                overview_data = json.loads(data)
                industry = overview_data['Industry']
                name = overview_data['Name']
                country = overview_data['Country']
                description = overview_data['Description']
                currency = overview_data['Currency']
                overview_info = [industry,name,country,description,currency]
                byte_stream = pickle.dumps(overview_info)
            
            elif inputs[1] == "2": #company daily prices
                query = construct_stock_query(company=inputs[3], function=inputs[2])
                data = postman_get_request(query=query)
                data = json.loads(data)
                dataForAllDays = data['Time Series (Daily)']
                date = inputs[4]
                dataForSingleDate = dataForAllDays[date]
                stock_prices = [dataForSingleDate['1. open'], dataForSingleDate['2. high'], dataForSingleDate['3. low'],dataForSingleDate['4. close'], dataForSingleDate['5. volume'] ]
                byte_stream = pickle.dumps(stock_prices)
        
        elif inputs[0] == "2": #FX
            if inputs[1] == "1": #exchange rate info
                query = construct_fx_exchange_query(inputs[2], inputs[3], inputs[4])
                data = postman_get_request(query=query)
                data = json.loads(data)
                data = data['Realtime Currency Exchange Rate']
                base_curr_name = data['2. From_Currency Name']
                target_curr_name = data['4. To_Currency Name']
                rate = data['5. Exchange Rate']
                exchange_data = [base_curr_name,target_curr_name,rate]
                byte_stream = pickle.dumps(exchange_data)
            
            elif inputs[1] == "2": #daily price info
                query = construct_fx_price_query(inputs[2], inputs[3], inputs[4])
                data = postman_get_request(query=query)
                data = json.loads(data)
                data = data['Time Series FX (Daily)']
                date = inputs[5]
                fx_prices = data[date]
                price_overview = [fx_prices['1. open'], fx_prices['2. high'], fx_prices['3. low'], fx_prices['4. close'] ]
                byte_stream = pickle.dumps(price_overview)
        
        clientsocket.send(byte_stream)        
        clientsocket.close()

print("Server running on http://localhost:3518")
createServer()