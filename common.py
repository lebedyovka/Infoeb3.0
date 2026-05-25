from datetime import datetime, timedelta
from banned import BANNED
from banned_english import BANNED_ENG
from words import how_many_words
import sys, string, re

MONTHS = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня', \
    '07': 'июля', '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}

SIXSEVEN = ['67', 'sixseeven', 'СИКС СЕВЕН', 'сикс севен', 'сикс сеевен', 'СИКСЕВЕН', 'сиксевен',\
     'six seven', 'sixseven', 'шестьдесят семь', 'шисят семь', 'SIXSEVEN', '60+7', '60 + 7', 'шесть семь', '6-7']


def border():
    print('================')

def fucking_russian(y):
    if y % 100 in [11, 12, 13, 14]:
        return 'лет'
    match y:
        case _ if y % 10 == 1:
            return 'год'
        case _ if y % 10 in [2, 3, 4]:
            return 'года'
        case _:
            return 'лет'

def fucking_russian2(m):
    match m:
        case _ if m % 10 == 1 and m % 100 != 11:
            return 'месяц'
        case _ if m % 10 in [2, 3, 4] and m % 100 not in [12, 13, 14]:
            return 'месяца'
        case _:
            return 'месяцев'

def fucking_russian3(d):
    if 11 <= d % 100 <= 14:
        return 'дней'
        
    match d % 10:
        case 1:
            return 'день'
        case 2 | 3 | 4:
            return 'дня'
        case _:
            return 'дней'


def parse_date(date):
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    ret = f'{day} {MONTHS[month]} {year}'
    return ret

def date_interval(date_str):
    year = int(date_str[0:4])
    month = int(date_str[5:7])
    day = int(date_str[8:10])
    
    start = datetime(year, month, day)
    end = datetime.now()
    
    y = end.year - start.year
    m = end.month - start.month
    d = end.day - start.day
    
    if d < 0:
        m -= 1
        d += 30 
        
    if m < 0:
        y -= 1
        m += 12
        
    parts = []
    
    if y > 0:
        parts.append(f"{y} {fucking_russian(y)}")
    if m > 0:
        parts.append(f"{m} {fucking_russian2(m)}")
    if d > 0:
        parts.append(f"{d} {fucking_russian3(d)}")

    return " ".join(parts) if parts else "меньше одного дня"

def speakers(users):
    if len(users) > 3:
        print("Топ воздуханов: ")
    users = dict(sorted(users.items(), key=lambda item: item[1], reverse = True))
    i = 1
    for user, count in users.items():
        if i < 6 and i <= len(users):
            print(f'{i} Юзер {user} отправил {count} сообщений')
        else: 
            break
        i += 1

def clear():
    sys.stdout.write("\033[A\033[K")
    sys.stdout.flush()


def is_russian(word):
    return all('а' <= char <= 'я' or char == 'ё' for char in word)
    
def is_english(word):
    return all('a' <= char <= 'z' for char in word)

def parse_messages(messages):
    users = {}
    frequency = {}
    sixseven = 0
    num = 0
    total_words = 0
    total = {}
    mgs = 0
    years = {}

    for i in messages:
        if i['text'] == "":
            num += 1
        else:
            break

    p = string.punctuation + "»«—"
    for i in messages:

        d = i['date'][0:4]
        if d not in years:
            years[d] = 0
        years[d] += 1

        u = i.get('from')
        if u:
            if u not in users:
                users[u] = 0
            users[u] += 1

        m = i['text']
        if m and isinstance(m, str):
            mgs += 1
            for s in SIXSEVEN:
                if s in m:
                    sixseven += 1

            m = re.sub(r'[^а-яА-Яa-zA-Z\s]', '', m)
            words = m.lower().split()

            for w in words:
                clean_word = w.strip(p)
                
                if not clean_word:
                    continue

                
                if is_russian(clean_word):
                        if clean_word in BANNED:
                            continue
                        frequency[clean_word] = frequency.get(clean_word, 0) + 1

                elif is_english(clean_word):
                    if clean_word in BANNED_ENG:
                        continue
                    frequency[clean_word] = frequency.get(clean_word, 0) + 1

        m2 = i['text']
        if m2 and isinstance(m2, str):

            m = re.sub(r'[^а-яА-Яa-zA-Z0-9\s]', '', m2)
            words = m2.lower().split()
            for w in words:
                clean_word = w.strip(p)
                total_words += 1
                if clean_word:
                    if clean_word not in total:
                        total[clean_word] = 0
                    total[clean_word] += 1

    frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse = True))
    return users, frequency, sixseven, num, total_words, total, how_many_words(total_words), mgs, years
    

def only_text(messages):
    with open('all_messages_text.txt', 'w', encoding='utf-8') as f:
        for i in messages:
            # 1. Достаем дату
            date = i.get('date', 'Unknown Date')
            if 'T' in date:
                date = date.replace('T', ' ')[:16]
            user = i.get('from', 'Система')

            m = i.get('text')
            if isinstance(m, list):
                m = "".join([part if isinstance(part, str) else part.get('text', '') for part in m])
            
            if m:
                m_clean = m.replace('\n', ' ') 
                f.write(f"[{date}] {user}: {m_clean}\n")

