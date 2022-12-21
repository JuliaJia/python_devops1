from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Employee,Salary


class SalarySerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = "__all__"

class EmpSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        extra_kwargs = {
            "emp_no":{
                "required": True
            },
            "first_name":{
                "required": True,
                "max_length": 14
            },
            "last_name": {
                "required": True,
                "max_length": 16
            },
            "gender": {
                "choices": Employee.Gender.choices
            },
            "hire_date": {
                "required": False
            }
        }

    salaries = SalarySerializerModel(many=True,read_only=True)
class EmpSerializer(serializers.Serializer):
    emp_no = serializers.IntegerField(required=True)
    birth_date = serializers.DateField()
    first_name = serializers.CharField(required=True,max_length=14)
    last_name = serializers.CharField(required=True,max_length=16)
    gender = serializers.ChoiceField(choices=Employee.Gender.choices)
    hire_date = serializers.DateField(required=False)
    # test1 = serializers.IntegerField(write_only=True)
    # def validate_first_name(self,value):
    #     if 4 <= len(value) < 14:
    #         # return value
    #         return "abcd"
    #     raise ValidationError("长度不能小于4或大于14！")


    #对象级别的校验
    def validate(self,value:dict):
        if 4 <= len(value.get("first_name")) < 14:
            pass
        else:
            raise ValidationError("长度不能小于4或大于14！")

        if value.get("last_name").startswith("C") or value.get("last_name").startswith("c"):
            pass
        else:
            raise ValidationError("last_name不是以C或c开头")
        return value

    def create(self,validated_data):
        emp_no = Employee.objects.create(**validated_data)
        return emp_no

    def update(self,instance,validated_data):
        instance.birth_date = validated_data.get("birth_date",instance.birth_date)
        instance.first_name = validated_data.get("first_name",instance.first_name)
        instance.last_name = validated_data.get("last_name",instance.last_name)
        instance.gender = validated_data.get("gender",instance.gender)
        instance.hire_date = validated_data.get("hire_date",instance.hire_date)
        instance.save()
        return instance