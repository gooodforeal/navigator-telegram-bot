from telebot import types


main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
"Клавиатура главного меню бота"
main_markup.row('Построить маршрут')
main_markup.row('История')
