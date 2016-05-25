#20:21:27,065
#20:21:26,677

#12:20:27

import pytz, datetime

sample_start_time = "20:21:27,065"
#sample_start_time = sample_start_time.split(',')[0]

# local = pytz.timezone ("America/Chicago")
# naive = datetime.datetime.strptime (sample_start_time, "%H:%M:%S,%f")
# local_dt = local.localize(naive, is_dst=True)
# utc_dt = local_dt.astimezone (pytz.utc)
# utc =  utc_dt.strftime("%H:%M:%S")
# print utc
lt = datetime.datetime.now()
ut = datetime.datetime.utcnow()

# print t
# print 'hour  :', t.hour
# print 'minute:', t.minute
# print 'second:', t.second
# print 'microsecond:', t.microsecond
# print 'tzinfo:', t.tzinfo
print ("local_time",lt)
print ("utc_time",ut)

delta  = ut.hour - lt.hour

print sample_start_time

date_object = datetime.datetime.strptime(sample_start_time, "%H:%M:%S,%f")

print "old_date",date_object
date_object = date_object - datetime.timedelta(hours=delta)
#nt = ut - nt_delta
#print ("updated time", ut-nt)
print date_object.hour,date_object.minute,date_object.second, date_object.microsecond