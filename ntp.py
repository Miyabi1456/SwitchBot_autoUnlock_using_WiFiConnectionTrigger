from machine import RTC
import ntptime
import utime
rtc = RTC()

def set_ntptime():
    print("set NTP time")
    ntptime.settime()
    
def get_jst():
    utc_offset = 9 #日本はUTC+9
    year, month, day, weekday, hours, minutes, seconds, subseconds = rtc.datetime()
    jst = str(year)+'/'+str(month)+'/'+str(day)+' '+str((hours+utc_offset)%24)+':'+str(minutes)+':'+str(seconds)
    return jst, year, month, day, weekday, hours, minutes, seconds, subseconds
    
if __name__ == "__main__":
    set_ntptime()
    print(get_jst())
