from rest_framework.serializers import ModelSerializer
from base.models import Student
from base.models import VdtUser

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class VdtUserSerializer(ModelSerializer):
    class Meta:
        model = VdtUser
        fields = '__all__'