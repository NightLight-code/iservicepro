from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from services.models import AllServices
from siteservice.models import NewPhone


class PhoneModel:
    def __init__(self, model_phone, memory_phone, colors_phone, region_phone, price_phone):
        self.model_phone = model_phone
        self.memory_phone = memory_phone
        self.colors_phone = colors_phone
        self.region_phone = region_phone
        self.price_phone = price_phone


class NewPhoneSerializer(serializers.Serializer):
    model_phone = serializers.CharField(max_length=150)
    memory_phone = serializers.CharField()
    colors_phone = serializers.CharField()
    region_phone = serializers.CharField()
    price_phone = serializers.CharField()
    created_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()
    status = serializers.CharField()
    activ_or_not = serializers.CharField()

    class Meta:
        model = NewPhone
        fields = ('model_phone', 'memory_phone', 'colors_phone', 'region_phone', 'price_phone')


class AllServiceSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    imei_or_serial = serializers.CharField()
    model = serializers.CharField()
    name_owner = serializers.CharField()
    phone_number = serializers.CharField()
    defect = serializers.CharField()
    created_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()
    status = serializers.CharField()
    price = serializers.CharField()
    income = serializers.CharField()
    comment = serializers.CharField()

    class Meta:
        all_service = AllServices
        fields = ('user_id', 'imei_or_serial', 'model', 'name_owner', 'phone_number', 'defect', 'status', 'price')

# def encode():
#     phone = PhoneModel('model_phone', 'memory_phone', 'colors_phone', 'region_phone', 'price_phone')
#     phone_sr = NewPhoneSerializer(phone)
#     print(phone_sr.data, type(phone_sr.data), sep='\n')
#     json = JSONRenderer().render(phone_sr.data)
#     print(json)
#
#
# def decode():
#     data = JSONParser().parse(stream)
#     serializers = NewPhoneSerializer(data=data)
#     serializers.is_valid()
#     print(serializers.validated_data)
