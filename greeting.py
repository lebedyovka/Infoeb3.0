import json

print('Имя .json файла: ')
fname = input()

with open(fname, 'r', encoding='utf-8') as f:
    data = json.load(f)

messages = data['messages']

print("Привет! Это твой помощник, сбор статистики ", end='')

if data['type'] == 'private_channel':
    print(f"приватного канала {data['name']}")

if data['type'] == 'public_channel':
    print(f"публичного канала {data['name']}")

if data['type'] == 'personal_chat':
    print(f'личной переписки с аккаунтом "{data['name']}"')

if data['type'] == 'private_supergroup':
    print(f'закрытой группы "{data['name']}"')

if data['type'] == 'public_supergroup':
    print(f'публичной группы "{data['name']}"')

if data['type'] == 'bot_chat':
    print(f'чата с ботом "{data['name']}"')