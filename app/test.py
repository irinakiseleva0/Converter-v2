'''from zeep import Client

print('Hello')
client = Client('http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?wsdl')
date = client.service.GetLatestDateTime()
result = client.service.GetCursOnDate(date)

rate_exchange = {}

names = []
value_list = result['_value_1']['_value_1']
for i in range(len(value_list)):

    b = value_list[i]['ValuteCursOnDate']
    rate_exchange[b["Vname"].strip()] = b["VunitRate"]
print(rate_exchange.keys())