from pylab import *
import tcx

date = '20180408_ski'

data_garmin = tcx.TCXParser('/home/sorokin/Downloads/{}_garmin.tcx'.format(date))
plot(data_garmin.time_values, data_garmin.hr_values, label='Garmin')

data_scosche = tcx.TCXParser('/home/sorokin/Downloads/{}_scosche.tcx'.format(date))
plot(data_scosche.time_values, data_scosche.hr_values, label='Scosche')

# print(data_garmin.pace)
#
# plot(data_garmin.time_values, data_garmin.pace, label='Pace')

xlabel('Time')
ylabel('Heart rate')
title('Heart rate')
grid(True)

legend()
#show()

savefig('/home/sorokin/Downloads/{}_hr.svg'.format(date))
