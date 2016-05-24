#20:21:27,065
#20:21:26,677

#12:20:27

import pytz, datetime

sample_start_time = "20:21:27,065"
local = pytz.timezone ("America/Chicago")
naive = datetime.datetime.strptime (sample_start_time, "%H:%M:%S,%f")
local_dt = local.localize(naive, is_dst=True)
utc_dt = local_dt.astimezone (pytz.utc)
utc =  utc_dt.strftime("%H:%M:%S")
print utc