import time
import telebot
import os
from dotenv import load_dotenv
import messages.bonuses as bonuses
import messages.info as info
import messages.register as register

from telebot import types

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BotToken = os.getenv("TOKEN")
bot = telebot.TeleBot(BotToken)
opened = [0]
op = 0
manager_reply = False
reply_to_client = False
client_id_input = False
reply_client_chat_id = None
admin_ids = ['5513975267']
tabs_dict = {0: 'main',
             1: 'reg',
             2: 'info',
             3: 'bonus',
             21: 'conditions',
             22: 'how_reg',
             23: 'payments',
             24: 'slot',
             40: 'question'}
 
@bot.message_handler(commands=['start'])
def welcome(message):
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Зарегистрироваться ✅", callback_data='reg')
        item2 = types.InlineKeyboardButton("Информация и FAQ ❓", callback_data='info')
        item3 = types.InlineKeyboardButton("Действующие бонусы 🎁", callback_data='bonus')

        markup.add(item1).add(item2).add(item3)
        bot.send_message(message.chat.id, f"<b>Привет!👋 Я бот партнера сервиса Яндекс.Еда!</b>\n\nСейчас мы находимся в поиске <b>команды курьеров!</b>🏃‍\n\nПланируешь накопить на свою <b>мечту</b>, но не получается подобрать удобный <b>источник дохода?</b>💰\n\nТогда быстрее ознакамливайся с правилами и <b>регистрируйся</b> в нашей программе!🧑‍💻".format(message.from_user, bot.get_me()), parse_mode = 'html',  reply_markup=markup)
       

@bot.message_handler(content_types=['text'])
def lalala(message):
    global manager_reply, reply_to_client, reply_client_chat_id, client_id_input

    if message.chat.type == 'private':
        if (manager_reply == True and reply_to_client == False):
            for i in admin_ids:
                bot.send_message(i, f'<b>Новое обращение в поддержку партнерки:</b>\n\n@{message.chat.id}'.format(message.from_user, bot.get_me()), parse_mode = 'html')
                bot.forward_message(i, message.chat.id, message.message_id)
            
                markupAdmin = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Да",  callback_data='reply_to_client_username')
                markupAdmin.add(item1)
                bot.send_message(i, f'Ответить?'.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup=(markupAdmin))
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("На главную",  callback_data='main')
            markup.add(item1)
            bot.send_message(message.chat.id, '📤 Ваше обращение было направлено в службу поддержки.\n\nПожалуйста, ожидайте ответ'.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup=(markup))


        elif (client_id_input == True and manager_reply == False and reply_to_client == False):
            if(any(c.isalpha() for c in message.text[1:]) or any(c.isalpha() for c in message.text)):
                bot.send_message(message.chat.id, f'<b>❗️Ошибка❗️<\b>\n\n'.format(message.from_user, bot.get_me()), parse_mode = 'html')
                client_id_input = False
            else:
                if((message.text).find("@") == 0):
                    reply_client_chat_id = message.text[1:]
                else:
                    reply_client_chat_id = message.text
           
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("<< Назад", callback_data='delete')
                reply_to_client = True

                markup.add(item1)
                bot.send_message(message.chat.id, f'Ваш Ответ:'.format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup=markup)
            

        elif (client_id_input == True and reply_to_client == True and manager_reply == False):
           
            try:
                bot.send_message(reply_client_chat_id, f'<b>📬 Вам поступил ответ от менеджера:</b>\n\n{message.text}', parse_mode = 'html')
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("На главную",  callback_data='main')
                markup.add(item1)
                bot.send_message(reply_client_chat_id, f'⬇Нажмите, чтобы вернуться в меню⬇', parse_mode = 'html', reply_markup=markup)
            except:
                bot.send_message(message.chat.id, f'<b>❗️Ошибка❗️<\b>\n\n'.format(message.from_user, bot.get_me()), parse_mode = 'html')
            finally:
                bot.send_message(message.chat.id, f'Ответ отправлен!'.format(message.from_user, bot.get_me()), parse_mode = 'html')
                reply_to_client = False
                client_id_input = False
                

        else:
            bot.send_message(message.chat.id, 'Я не знаю, что ответить 😢')
            time.sleep(2)
            bot.delete_message(message.chat.id, message.id+1)

 
def check_back():
    global opened, tabs_dict
    
    if(opened[-1] == 1 or opened[-1] == 3 or opened[-1] == 2 or opened[-1] == 40):
        return tabs_dict[opened[-2]]
    elif(opened[-1] == 21 or opened[-1] == 22 or opened[-1] == 23 or opened[-1] == 24):
        return tabs_dict[2]

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global op, manager_reply, reply_to_client, client_id_input, opened
    manager_reply = False
    reply_to_client = False
    client_id_input = False
    try:
        if call.message:
            if call.data == 'main':
                if(opened[-1] > 0):
                        opened.pop(-1)
                #bot.send_message(call.message.chat.id, f'{opened}'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Зарегистрироваться ✅", callback_data='reg')
                item2 = types.InlineKeyboardButton("Информация и FAQ ❓", callback_data='info')
                item3 = types.InlineKeyboardButton("Действующие бонусы 🎁", callback_data='bonus')

                markup.add(item1).add(item2).add(item3)
                bot.edit_message_text(chat_id = call.message.chat.id, text = f"<b>Привет!👋 Я бот партнера сервиса Яндекс.Еда!</b>\n\nСейчас мы находимся в поиске <b>команды курьеров!</b>🏃‍\n\nПланируешь накопить на свою <b>мечту</b>, но не получается подобрать удобный <b>источник дохода?</b>💰\n\nТогда быстрее ознакамливайся с правилами и <b>регистрируйся</b> в нашей программе!🧑‍💻".format(call.message.from_user, bot.get_me()), message_id = call.message.message_id, parse_mode = 'html',  reply_markup=markup)
                    

            elif call.data == "reg":
                    if(opened[-1] > 1):
                        opened.pop(-1)
                    if(1 not in opened):
                        opened.append(1)
                    #bot.send_message(call.message.chat.id, f'{opened}'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = types.InlineKeyboardButton("Перейти к регистрации ✅", url=register.LINK)
                    item2 = types.InlineKeyboardButton("Информация и FAQ ❓", callback_data='info')
                    item3 = types.InlineKeyboardButton("<< Назад", callback_data=check_back())
                    markup.add(item1, item2, item3)
                    op = 1
                    #bot.edit_message_text("Для регистрации курьером, пожалуйста, ознакомьтесь с информацией и часто задаваемыми вопросами (Если вы этого еще не сделали) и перейдите к регистрации по кнопке внизу\n\n❗ВНИМАНИЕ❗ Пожалуйста, постарайтесь не перезагружать страницу во время регистрации во избежание технических проблем.\n\nЕсли что-то пошло не так - лучше начните регистрацию с самого начала\n\nБольшое спасибо!😊", call.message.chat.id, call.message.message_id, parse_mode = 'html', reply_markup=markup)
                    
                    bot.edit_message_text(chat_id = call.message.chat.id, text = f"<b>Зарегистрироваться ✅</b>\n\nДля регистрации курьером, пожалуйста:\n\n  1. Ознакомьтесь с <b>информацией и часто задаваемыми вопросами</b> (Если вы этого еще не сделали)\n\n  2. Перейдите к регистрации по <b>кнопке внизу⬇</b>\n\n<i>❗ВНИМАНИЕ❗ Пожалуйста, постарайтесь не перезагружать страницу во время регистрации во избежание технических проблем.\n\nЕсли что-то пошло не так - лучше начните регистрацию с <b>самого начала</b></i>\n\n  Большое спасибо!😊".format(call.message.from_user, bot.get_me()), message_id=call.message.message_id, parse_mode = 'html', reply_markup=(markup))
                    

            elif call.data == 'info':   
                    if(opened[-1] > 2):
                        opened.pop(-1)
                    if(2 not in opened):
                        opened.append(2)        
                    #bot.send_message(call.message.chat.id, f'{opened}'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = types.InlineKeyboardButton("Что предлагаем?", callback_data='conditions')
                    item2 = types.InlineKeyboardButton("Как проходит регистрация?", callback_data='how_reg')
                    item3 = types.InlineKeyboardButton("Выплаты", callback_data='payments')
                    item4 = types.InlineKeyboardButton("Что такое слот?", callback_data='slot')
                    item5 = types.InlineKeyboardButton("Задать вопрос", callback_data='question')
                    item6 = types.InlineKeyboardButton("<< Назад", callback_data=check_back())
 
                    markup.add(item1, item2, item3, item4, item5, item6)
                   
                    bot.edit_message_text(chat_id = call.message.chat.id, text = f'<b>Информация и FAQ ❓</b>\n\nПартнер сервиса Яндекс.Еда в поисках <b>команды курьеров!</b>\n\n➖ Хочешь сам выбирать <b>время и локации</b> для доставок?🕓\n\n➖ Хочешь иметь выплаты до 3400 рублей в день?💰\n\n➖ У тебя есть гаджет на базе Android 7 и выше?📱\n\n<b>Присоединяйся к партнеру сервиса Яндекс.Еда!</b>\n\n<i>Остались вопросы? Вы можете задать их нашему менеджеру, нажав на кнопку ЗАДАТЬ ВОПРОС под сообщением</i>'.format(call.message.from_user, bot.get_me()), message_id=call.message.message_id, parse_mode = 'html', reply_markup=markup)
                

            elif call.data == 'bonus':
                    if(opened[-1] > 3):
                        opened.pop(-1)
                    if(3 not in opened):
                        opened.append(3)  
                    #bot.send_message(call.message.chat.id, f'{opened}'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = types.InlineKeyboardButton("<< Назад", callback_data=check_back())
 
                    markup.add(item1)
                   
                    bot.edit_message_text(chat_id = call.message.chat.id, text = f"<b>Действующие бонусы 🎁</b>\n\n" + bonuses.NONE.format(call.message.from_user, bot.get_me()), message_id=call.message.message_id, parse_mode = 'html', reply_markup=markup)
                    
            
            elif call.data == 'conditions':
                #bot.delete_message(call.message.chat.id, call.message.id)
                if(opened[-1] > 21):
                        opened.pop(-1)
                if(21 not in opened):
                    opened.append(21)  
                #bot.send_message(call.message.chat.id, f'{opened}'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Задать вопрос", callback_data='question')
                item2 = types.InlineKeyboardButton("<< Назад", callback_data=check_back())
                
                markup.add(item1, item2)
            
                bot.edit_message_text(chat_id = call.message.chat.id, text = f'<b>Что предлагаем?</b>\n\n🔸Гибкое расписание, которое ты сам выбираешь из доступных слотов\n🔸Удобные локации в твоем городе\n🔸Яркую желтую одежду\n🔸Возможность совмещать с другой работой или учебой\n🔸Первая выплата поступает через две недели, далее для самозанятых, выплаты ежедневные\n\n  <b>Люди в желтом ждут тебя!</b>\n\n<i>Остались вопросы? Вы можете задать их нашему менеджеру, нажав на кнопку ЗАДАТЬ ВОПРОС под сообщением</i>'.format(call.message.from_user, bot.get_me()), message_id=call.message.message_id, parse_mode = 'html', reply_markup=markup)
                

            elif call.data == 'how_reg':
                #bot.delete_message(call.message.chat.id, call.message.id)
                if(opened[-1] > 22):
                        opened.pop(-1)
                if(22 not in opened):
                    opened.append(22) 
                #bot.send_message(call.message.chat.id, f'{opened}'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Задать вопрос", callback_data='question')
                item2 = types.InlineKeyboardButton("<< Назад", callback_data=check_back())
                
                markup.add(item1, item2)
            
                bot.edit_message_text(chat_id = call.message.chat.id, text = f'<b>Как проходит регистрация?</b>\n\n1. Вы <b>переходите по ссылке🔗</b> и попадаете на сайт с формой регистрации✏\n\n2. <b>Заполняете</b> стандартные данные, необходимые для регистрации📝\n\n3. Проходите небольшой <b>тест-обучение📚</b>\n\n4. Далее 2 варианта:\n    а) Вас <b>записывают в офис</b> вашего города для прохождение активации и выдачи инвентаря 🧑‍🏫\n    б) Вас <b>перенаправляют в памятку</b>, где подробно рассказывают как самостоятельно завершить регистрацию и пройти активацию📄\n\n<b>Эти 4 простых шага позволят вам стать курьером партнера сервиса Яндекс.Еда. Удачи!☺</b>\n\n<i>Остались вопросы? Вы можете задать их нашему менеджеру, нажав на кнопку ЗАДАТЬ ВОПРОС под сообщением</i>'.format(call.message.from_user, bot.get_me()),  message_id=call.message.message_id, parse_mode = 'html', reply_markup=markup)
                

            elif call.data == 'payments':
                if(opened[-1] > 23):
                        opened.pop(-1)
                if(23 not in opened):
                    opened.append(23) 
                #bot.send_message(call.message.chat.id, f'{opened}'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
                #bot.delete_message(call.message.chat.id, call.message.id)
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Задать вопрос", callback_data='question')
                item2 = types.InlineKeyboardButton("<< Назад", callback_data=check_back())
                
                markup.add(item1, item2)
               
                bot.edit_message_text(chat_id = call.message.chat.id, text = f'<b>Выплаты</b>\n\n🇷🇺Для городов РФ – до 3400 руб\n🇰🇿Для городов Казахстана – до 9600 тенге\n\n💵Выплаты производятся ежедневно или еженедельно, в зависимости от вашего гражданства, формы занятости и количества выполненных слотов\n\n<i>Остались вопросы? Вы можете задать их нашему менеджеру, нажав на кнопку ЗАДАТЬ ВОПРОС под сообщением</i>'.format(call.message.from_user, bot.get_me()), message_id=call.message.message_id, parse_mode = 'html', reply_markup=markup)
                

            elif call.data == 'slot':
                if(opened[-1] > 24):
                        opened.pop(-1)
                if(24 not in opened):
                    opened.append(24) 
                #bot.send_message(call.message.chat.id, f'{opened}'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
                #bot.delete_message(call.message.chat.id, call.message.id)
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Задать вопрос", callback_data='question')
                item2 = types.InlineKeyboardButton("<< Назад", callback_data=check_back())
                
                markup.add(item1, item2)
                
                bot.edit_message_text(chat_id = call.message.chat.id, text = f'<b>Что такое слот?</b>\n\n📆 Слот - это временной промежуток, в который вы выполняете доставку. Из слотов вы составляете свое расписание\n\n<i>Остались вопросы? Вы можете задать их нашему менеджеру, нажав на кнопку ЗАДАТЬ ВОПРОС под сообщением</i>'.format(call.message.from_user, bot.get_me()), message_id=call.message.message_id, parse_mode = 'html', reply_markup=markup)
                

            elif call.data == 'question':
                #bot.delete_message(call.message.chat.id, call.message.id)
                if(opened[-1] > 40):
                        opened.pop(-1)
                if(40 not in opened):
                    opened.append(40) 
                #bot.send_message(call.message.chat.id, f'{opened}'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
                manager_reply = True
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("<< Назад", callback_data=check_back())
                
                markup.add(item1)
               
                bot.edit_message_text(chat_id = call.message.chat.id, text = f'<b>Задать вопрос</b>\n\n📢 Задайте вопрос нашему менеджеру. Он ответит вам в течении суток:'.format(call.message.from_user, bot.get_me()), message_id=call.message.message_id, parse_mode = 'html', reply_markup=markup)
                
            elif call.data == 'reply_to_client_username':

                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("<< Назад", callback_data='delete')
                client_id_input = True

                markup.add(item1)
                bot.send_message(call.message.chat.id, f'✅ Введите username пользователя:'.format(call.message.from_user, bot.get_me()), parse_mode = 'html', reply_markup=markup)
            
            elif call.data == 'start':
                bot.send_message(call.message.chat.id, f'Нажмите /start'.format(call.message.from_user, bot.get_me()), parse_mode = 'html')
            
            elif call.data == 'delete':
                bot.delete_message(call.message.chat.id, call.message.id)



            
            # remove inline buttons
            #bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="лол", reply_markup=None)
 
            # show alert
            #bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
 
    except Exception as e:
        print(repr(e))

# RUN
bot.polling(none_stop=True)
