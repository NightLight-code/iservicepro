from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from services.models import AllServices
from .serializers import NewPhoneSerializer, AllServiceSerializer

from siteservice.models import NewPhone

# Create your views here.
menu = ["О Нас", "Контакты", "Каталог"]


class NewPhoneSetView(APIView):
    def get(self, request):
        new_phone = NewPhone.objects.all()
        return Response({'phone': NewPhoneSerializer(new_phone, many=True).data})

    def post(self, request):
        post_new_phone = NewPhone.objects.get_or_create(model_phone=request.data['model_phone_name_phone'],
                                                        memory_phone=request.data['memory_phone_memory'],
                                                        colors_phone=request.data['colors_phone_colors'],
                                                        region_phone=request.data['region_phone_regions'],
                                                        price_phone=request.data['price_phone'])
        return Response({'posts': model_to_dict(post_new_phone).data})


class AllServicesSetView(APIView):
    def get(self, request):
        all_service = AllServices.objects.all()
        return Response({'service': AllServiceSerializer(all_service, many=True).data})


def index(request):
    phone = NewPhone.objects.all()[:20]
    return render(request, 'index.html', {'phone': phone, 'menu': menu, "title": 'Главная страница'})

#
# def login_post():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     remember = True if request.form.get('remember') else False

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponseNotFound
# from .models import NewiPhone
#
#
# # получение данных из бд
# def index(request):
#     people = Person.objects.all()
#     return render(request, "in.html", {"people": people})
#
#
# # сохранение данных в бд
# def create(request):
#     if request.method == "POST":
#         person = Person()
#         person.name = request.POST.get("name")
#         person.age = request.POST.get("age")
#         person.save()
#     return HttpResponseRedirect("/")
#
#
# # изменение данных в бд
# def edit(request, id):
#     try:
#         person = Person.objects.get(id=id)
#
#         if request.method == "POST":
#             person.name = request.POST.get("name")
#             person.age = request.POST.get("age")
#             person.save()
#             return HttpResponseRedirect("/")
#         else:
#             return render(request, "edit.html", {"person": person})
#     except Person.DoesNotExist:
#         return HttpResponseNotFound("<h2>Person not found</h2>")
#
#
# # удаление данных из бд
# def delete(request, id):
#     try:
#         person = Person.objects.get(id=id)
#         person.delete()
#         return HttpResponseRedirect("/")
#     except Person.DoesNotExist:
#         return HttpResponseNotFound("<h2>Person not found</h2>")
