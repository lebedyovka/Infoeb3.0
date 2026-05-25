from greeting import messages
from common import parse_date, date_interval, speakers, clear, border, parse_messages, only_text

print('\nМенюшка. Введи номер команды или stop, чтобы завершить программу')
print('1 Первое сообщение')
print('2 Сколько всего сообщений')
print('3 Сколько прошло времени с первого сообщения')
print('4 Активные говоруны')
print('5 Самые обсуждаемые темы')
print('6 Сиксеевен')
print('7 Сколько раз встречается ... (введи слово далее)')
print('8 Сколько всего слов в чате')
print('9 Сколько сообщений за год')
#print('404 Дебаг')

users, frequency, sixseven, num, total_words, total, book, mgs, years = parse_messages(messages)

# если это внатуре кому-то интересно читать на гитхабе, напиши на @bedvka, получишь подарок :)

print('\nВведите команду: ', end='')
command = input()
clear()

while command != 'stop':
    border()
    match command:
        case "stop":
            exit(0)

        case "1":
            date = parse_date(messages[num]['date'])
            print(f'Самое первое сообщение пришло от юзера "{messages[num]['from']}" {date}.')
            print(f'    Вот оно: {messages[num]['text']}')

        case "2":
            print(f'Ого! Целых {len(messages)} сообщений')

        case "3":
            print(f'Чат существует {date_interval(messages[0]['date'])}')

        case "4":
            speakers(users)
        
        case '5':
            i = 0
            for word, count in frequency.items():
                print(f'{i + 1} {word} - {count} повторений')
                i += 1
                if i == 20:
                    break
                #print(f"'{word}',", end=' ')
                #i += 1
                #if i == 100:
                #    break

        case "6":
            print(f'Количество 67 в чате: {sixseven}')

        case "7":
            print(f'Введите слово: ', end='')
            word = input().lower()
            if word in total:
                print(f'Количество вхождений {word}: {total[word]}')
            else:
                print(f'Слова {word} нет в чате')
        
        case "8":
            print(f'В чате {total_words} слов ({total_words // mgs} на сообщение).\nЭто примерно столько, сколько {book}')

        case "9":
            for year, cnt in years.items():
                print(f'В {year} году отправлено {cnt} сообщений')

        case "404":
            only_text(messages)

    print('Введите команду: ', end='')
    command = input()
    clear()
