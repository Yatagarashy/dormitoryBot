from datetime import datetime, timedelta, date

date = str(date.today() + timedelta(days=5))

print(date)

print(type(date))


# for i in range(28):
#     print(date.today() + timedelta(days=i+1))