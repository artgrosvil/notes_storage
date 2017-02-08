from telebot import types

def keyboard_main():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Добавить заметку')
    markup.row('Список заметок')
    return markup

def keyboard_change_notes(count):
    markup = types.ReplyKeyboardMarkup()
    count = count - 1
    count_tmp = []
    i = 0
    while i <= count:
        i = i + 1
        count_tmp.append(str(i))
    count_tmp = tuple(count_tmp)
    markup.row(*count_tmp)
    markup.row('Назад')
    return markup

def keyboard_edit_note():
    markup = types.ReplyKeyboardMarkup()
    markup.row('Редактировать', 'Удалить')
    markup.row('Назад')
    return markup

def keyboard_main_remove():
    markup = types.ReplyKeyboardRemove(selective=False)
    return markup