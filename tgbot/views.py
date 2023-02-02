import decimal
from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView

from siteservice.models import ModelPhone


class MainPage(TemplateView):
    def get(self, request, **kwargs):
        latest_forecast = ModelPhone.objects.latest('timestamp')
        phone = latest_forecast.phone
        temperature_in_c = latest_forecast.temperatue
        temperature_in_f = (latest_forecast.temperatue * decimal.Decimal(1.8)) + 32
        description = latest_forecast.description.capitalize
        timestamp = "{t.year}/{t.month:02d}/{t.day:02d} - {t.hour:02d}:{t.minute:02d}:{t.second:02d}".format(
            t=latest_forecast.timestamp)

        return render(
            request,
            'in.html',
            {
                'city': city,
                'temperature_in_c': temperature_in_c,
                'temperature_in_f': round(temperature_in_f, 2),
                'desctiprion': description,
                'utc_update_time': timestamp}
        )









# __gt для сравнений если больше
# __ls если меньше
# __gte больше или равно
# exclude не равно
# __isnull true or false
# schedule.every(10).minutes.do(job)
# schedule.every().day.at().do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)
# нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
# for object in data:
#     object.save(update_fields=["price_phone"])
#     print(object)

# def main():
#     try:
#         bot.polling(none_stop=True, timeout=123, interval=1)
#         while True:
#             schedule.run_pending()
#             time.sleep(10)
#     except Exception as e:
#         print(f'Error {e}')
#     except UnboundLocalError as connect:
#         return main
# else:
#     bot.send_message(chat_id,
#                      text='А вот это мне не знакомо, пожалуй запомню ☺️', reply_markup=kb.markup_menu)

#     # if not user_data:
#     #     try:
#     #         user_name, _ = Profile.objects.get_or_create(external_id=chat_id,
#     #                                                      defaults={'name': message.from_user.first_name,
#     #                                                                'admin_or_not': False})
#     #         user_message = Message(profile=user_name, text=text_user)
#     #         user_message.save()
#     #     except Exception as m:
#     #         error_message = f'Произошла ошибка: {m}'
#     #         print(error_message)
#     #         raise m

# for s in range(len(user_id)):
#     bot.send_message(user_id[s][0], message.text)
#     bot.send_message('Рассылка завершена', reply_markup=kb.markup_menu)
#     bot.delete_state(message.from_user.id, message.chat.id)

# bot.set_state(message.from_user.id, message.chat.id)
# with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#     data['price'] = message.text
#     write_data(data['price'])
#     # print(data['price'])
# bot.delete_state(message.from_user.id, message.chat.id)
# send_ok(message)


#
#
# def admin_text(message):
#     chat_id = message.chat.id
#     ad_text = message.text.lower()
#
#     if message.from_user.id == get_all_users_admin:
#         return print(get_all_users_admin)
#     elif admin_text == 'Рассылка':
#         return bot.send_message(chat_id, text="Рассылка")
