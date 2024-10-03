from rest_framework import serializers
from .models import Add_class,Add_Students

class Add_class(serializers.ModelSerializer):
    class Meta:
        model = Add_class
        fields = ['class_name']