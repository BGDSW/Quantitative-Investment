import requests


def Get_BeiJing_Time(get_day=False, get_second=False):
    url = 'https://www.beijing-time.org/t/time.asp'
    page = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41"})
    text = page.text.split(';')
    year = text[1].split('=')[-1]
    month = text[2].split('=')[-1]
    date = text[3].split('=')[-1]
    day = text[4].split('=')[-1]  # 星期几
    hour = text[5].split('=')[-1]
    minute = text[6].split('=')[-1]
    second = text[7].split('=')[-1]
    date = '{}{}{}{}{}'.format(year,
                               month.rjust(2, '0'),
                               date.rjust(2, '0'),
                               hour.rjust(2, '0'),
                               minute.rjust(2, '0'))
    if (get_day):
        return date, day
    if (get_second):
        return date + second.rjust(2, '0')
    else:
        return date

def Split_Time(time:str, Int=True, Year=False, Month=False, Date=False, Hour=False, Minute=False, Second=False):
        ans = []
        if(Year):
            if(Int):
                ans.append(int(time[:4]))
            else:
                ans.append(time[:4])
        if(Month):
            if (Int):
                ans.append(int(time[4:6]))
            else:
                ans.append(time[4:6])
        if(Date):
            if (Int):
                ans.append(int(time[6:8]))
            else:
                ans.append(time[6:8])
        if(Hour):
            if (Int):
                ans.append(int(time[8:10]))
            else:
                ans.append(time[8:10])
        if(Minute):
            if (Int):
                ans.append(int(time[10:12]))
            else:
                ans.append(time[10:12])
        if(len(time)==14):
            if (Second):
                if (Int):
                    ans.append(int(time[12:14]))
                else:
                    ans.append(time[12:14])
        if(len(ans)==1):
            return ans[0]
        return ans

class Time():
    def __init__(self, year=-1, month=-1, day=-1, hour=-1, minute=-1):
        # TODO: no processing leap year
        self.Year = year
        self.Month = month
        self.Day = day
        self.Hour = hour
        self.Minute = minute

    def toString(self):
        return '%04d%02d%02d%02d%02d' % (self.Year, self.Month, self.Day, self.Hour, self.Minute)

    def SetTime(self, year=-1, month=-1, day=-1, hour=-1, minute=-1):
        self.Year = year
        self.Month = month
        self.Day = day
        self.Hour = hour
        self.Minute = minute

    def refresh(self):
        # TODO: adjust months from only 31 days
        if (self.Minute >= 60):
            self.Hour += self.Minute // 60
            self.Minute = self.Minute % 60
        if (self.Hour >= 24):
            self.Day += self.Hour // 24
            self.Hour = self.Hour % 24
        if (self.Day >= 32):
            if (self.Day % 31 == 0):
                self.Month += self.Day // 31 - 1
                self.Day = 31
            else:
                self.Month += self.Day // 31
                self.Day = self.Day % 31
        if (self.Month >= 13):
            if (self.Month % 12 == 0):
                self.Year += self.Month // 12 - 1
                self.Month = 12
            else:
                self.Year += self.Month // 12
                self.Month = self.Day % 12

    def __add__(self, other):
        self.Minute += other
        self.refresh()
