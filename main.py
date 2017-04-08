import keyboard
import db
import telebot
from datetime import datetime

bot = telebot.TeleBot('325797002:AAFAm_xl9zv8ZX4ji6s0zrSAdDOFQmhEDSk')

def map_list_notes(list_notes):
    string_notes = ''
    dict_id_notes = {}
    for i, el in enumerate(list_notes):
        string_notes = string_notes + str(i + 1) + ') ' + str(el[1]) + ' \nДата: ' + str(el[3]) + '\n\n'
        dict_id_notes.update({i+1:el[0]})
    notes = [string_notes, dict_id_notes]
    return notes

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    markup = keyboard.keyboard_main()
    bot.send_message(message.chat.id, 'Привет, этот бот поможет тебе хранить твои заметки!', reply_markup=markup)

@bot.message_handler(regexp='Добавить заметку')
def handle_add_note(message):
    markup = keyboard.keyboard_main_remove()
    step = bot.send_message(message.chat.id, 'Введите заметку:', reply_markup=markup)
    bot.register_next_step_handler(step, add_note)

def add_note(message):
    markup = keyboard.keyboard_main()
    db.insert_note(message.chat.id, message.text, datetime.now())
    bot.send_message(message.chat.id, 'Заметка добавлена!', reply_markup=markup)

@bot.message_handler(regexp='Список заметок')
def handle_get_notes(message):
    list_notes = db.get_notes(message.chat.id)
    notes = map_list_notes(list_notes)
    count = db.count_notes(message.chat.id)
    if count == 0:
        markup = keyboard.keyboard_main()
        bot.send_message(message.chat.id, 'У вас нет заметок.', reply_markup=markup)
    else:
        markup = keyboard.keyboard_change_notes(count)
        bot.send_message(message.chat.id, 'Ваш список заметок:', reply_markup=markup)
        step = bot.send_message(message.chat.id, notes[0], reply_markup=markup)
        bot.send_message(message.chat.id, 'Выбирите заметку для изменения:')
        bot.register_next_step_handler(step, lambda m: change_note(m, notes))

def change_note(message, notes):
    if message.text == 'Назад':
        markup = keyboard.keyboard_main()
        bot.send_message(message.chat.id, 'Назад', reply_markup=markup)
    else:
        markup = keyboard.keyboard_edit_note()
        id_note = int(message.text)
        step = bot.send_message(message.chat.id, 'Действия с заметкой:', reply_markup=markup)
        bot.register_next_step_handler(step, lambda m: move_note(m, id_note, notes))

def move_note(message, id_note, notes):
    if message.text == 'Назад':
        markup = keyboard.keyboard_main()
        bot.send_message(message.chat.id, 'Назад', reply_markup=markup)
    elif message.text == 'Редактировать':
        markup = keyboard.keyboard_main_remove()
        step = bot.send_message(message.chat.id, 'Введите заметку:', reply_markup=markup)
        bot.register_next_step_handler(step, lambda m: edit_note(m, id_note, notes))
    elif message.text == 'Удалить':
        markup = keyboard.keyboard_main()
        dict_id_notes = notes[1]
        db.delete_note(dict_id_notes.get(id_note))
        bot.send_message(message.chat.id, 'Заметка удалена', reply_markup=markup)

def edit_note(message, id_note, notes):
    markup = keyboard.keyboard_main()
    dict_id_notes = notes[1]
    db.update_note(dict_id_notes.get(id_note), message.text)
    bot.send_message(message.chat.id, 'Заметка отредактирована.', reply_markup=markup)

if __name__ == '__main__':
    bot.polling(none_stop=True)