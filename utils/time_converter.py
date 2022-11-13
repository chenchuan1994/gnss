from datetime import datetime, timedelta

DAY_SECS = 86400  # 24 * 60 * 60
WEEK_DAYS = 7     # A week contains 7 days
LEAP_SECONDS = {
    (1981, 6, 30, 23, 59, 60): 1,
    (1982, 6, 30, 23, 59, 60): 1,
    (1983, 6, 30, 23, 59, 60): 1,
    (1985, 6, 30, 23, 59, 60): 1,
    (1987, 12, 31, 23, 59, 60): 1,
    (1989, 12, 31, 23, 59, 60): 1,
    (1990, 12, 31, 23, 59, 60): 1,
    (1992, 6, 30, 23, 59, 60): 1,
    (1993, 6, 30, 23, 59, 60): 1,
    (1994, 6, 30, 23, 59, 60): 1,
    (1995, 12, 31, 23, 59, 60): 1,
    (1997, 6, 30, 23, 59, 60): 1,
    (1998, 12, 31, 23, 59, 60): 1,
    (2005, 12, 31, 23, 59, 60): 1,
    (2008, 12, 31, 23, 59, 60): 1,
    (2012, 6, 30, 23, 59, 60): 1,
    (2015, 6, 30, 23, 59, 60): 1,
    (2016, 12, 31, 23, 59, 60): 1,
}

leap_year = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 闰年
common_year = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 平年


def gpst2seconds(gps_week, gps_seconds):
    return gps_week * WEEK_DAYS * DAY_SECS + gps_seconds


def isLeapYear(year) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def gpst2utc(gps_week, gps_seconds) -> datetime:
    """
     Convert gps time(gps_week, gps_seconds) to utc time (year,month,day,hour,minute,second)
     @param:
      gps_week:
      gps_seconds:

     @return:
      datetime(year, month, day, hour, minute, seond, ms)
    """

    if gps_week < 0 or gps_seconds < 0:
        raise ValueError(
            "Input invalid gps week and gps seconds, {}".format(gps_week, gps_seconds))
        return -1

    gpts_seconds = gpst2seconds(gps_week, gps_seconds)

    utc_seconds = gpts_seconds
    days = int(utc_seconds / DAY_SECS)
    seconds = utc_seconds - days * DAY_SECS

    months = None

    # calc year, month, day
    y = 1980
    d = 0
    m = 0
    while days >= 0:
        if isLeapYear(y):
            months = leap_year
        else:
            months = common_year

        if y == 1980:
            months[0] = 26
        else:
            months[0] = 31

        for i in range(0, 12):
            days -= months[i]
            if days <= 0:
                d = days + months[i] + 1
                m = i + 1
                break

        if days > 0 and i == 11:
            y += 1

    if y == 1980 and m == 1:
        d += 5

    # calc hour, mintue, seconds
    h = int(seconds / 3600)
    mm = int((seconds - h * 3600) / 60)
    s = int(seconds - h * 3600 - mm * 60)
    ms = (seconds - h*3600 - mm*60-s)*1000

    gps_t = datetime(y, m, d, h, mm, s, ms)

    for key in list(LEAP_SECONDS.keys()):
        if (gps_t.year, gps_t.month, gps_t.day,
                gps_t.hour, gps_t.minute, gps_t.second+gps_t.microsecond/1000) >= key:
            gps_t -= timedelta(seconds=LEAP_SECONDS[key])
        else:
            break

    return gps_t


def utc2gpst(year, month, day, hour, minute, second, microsecond=0):
    return


def gpst2unix():
    return


if __name__ == "__main__":
    gps_week = 80
    gps_second = 345600
    print(gpst2utc(2232, 437323))  # datetime.datetime(1980, 1, 23, 0, 0)
