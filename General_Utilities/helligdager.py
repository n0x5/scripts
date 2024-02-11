import datetime


format = '%A %B %d %Y'


year = 2030

Nyttårsdag = datetime.date(year, 1, 1)
Arbeidernes = datetime.date(year, 5, 1)
Nasjonaldag = datetime.date(year, 5, 17)
Førstejuledag = datetime.date(year, 12, 25)
Andrejuledag = datetime.date(year, 12, 26)


a = year % 19
b = year // 100
c = year % 100
d = b // 4
e = b % 4
f = (b + 8) // 25
g = (b - f + 1) // 3
h = (19 * a + b - d - g + 15) % 30
i = c // 4
k = c % 4
l = (32 + 2 * e + 2 * i - h - k) % 7
m = (a + 11 * h + 22 * l) // 451
easter = datetime.date(year, (h + l - 7 * m + 114)//31, (h + l - 7 * m + 114) % 31 + 1)

november = datetime.date(year, 11, 1)
while november.weekday() != 6:
    november += datetime.timedelta(days=1)

allehelgensdag = november + datetime.timedelta(days=1)
Palmesøndag = easter - datetime.timedelta(days=7)
Skjærtorsdag = easter - datetime.timedelta(days=3)
Langfredag = easter - datetime.timedelta(days=2)
Førstepåskedag = easter
Andrepåskedag = easter + datetime.timedelta(days=1)
Himmelfartsdag = easter + datetime.timedelta(days=39)
Førstepinsedag = easter + datetime.timedelta(days=49)
Andrepinsedag = easter + datetime.timedelta(days=50)
fastelavnssøndag = easter - datetime.timedelta(days=49)

print('Bevegelige hellidager:')
print('Palmesøndag: '+ Palmesøndag.strftime(format))
print('Skjærtorsdag: '+ Skjærtorsdag.strftime(format))
print('Langfredag: ' + Langfredag.strftime(format))
print('Første påskedag: ' + Førstepåskedag.strftime(format))
print('Andre påskedag: ' + Andrepåskedag.strftime(format))
print('Himmelfartsdag: ' + Himmelfartsdag.strftime(format))
print('Første pinsedag: ' + Førstepinsedag.strftime(format))
print('Andre pinsedag: ' + Andrepinsedag.strftime(format))
print('Fastelavnssøndag: ' + fastelavnssøndag.strftime(format))
print('Allehelgensdag: ' + allehelgensdag.strftime(format))

print('')
print('Ubevegelige hellidager:')
print('Nyttårsdag: ' + Nyttårsdag.strftime(format))
print('Arbeidernes dag: ' + Arbeidernes.strftime(format))
print('Nasjonaldag: ' + Nasjonaldag.strftime(format))
print('Første juledag: ' + Førstejuledag.strftime(format))
print('Andre juledag: ' + Andrejuledag.strftime(format))
