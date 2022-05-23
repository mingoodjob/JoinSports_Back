import datetime as dt

current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(current_time)

old_time = dt.datetime(2018,9,11,0,0,0)

delta_time = current_time - old_time

print(delta_time)
