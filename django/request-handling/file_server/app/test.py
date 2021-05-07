from datetime import datetime

value = '2020-01-01'

date = datetime.strptime(value, '%Y-%m-%d')
print(type(date))

print(type(date.strftime('%Y-%m-%d')))