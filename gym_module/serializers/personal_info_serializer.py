from rest_framework import serializers
from gym_module.models import PersonalInfo

class PersonalInfoSerializer(serializers.ModelSerializer):
    bmi = serializers.FloatField(read_only=True)
    bmr = serializers.FloatField(read_only=True)
    lbm = serializers.FloatField(read_only=True)
    tdee = serializers.FloatField(read_only=True)
    rmr = serializers.FloatField(read_only=True)
    ffmi = serializers.FloatField(read_only=True)
    iac = serializers.FloatField(read_only=True)
    fat_mass = serializers.FloatField(read_only=True)
    whr = serializers.FloatField(read_only=True)
    mhr = serializers.FloatField(read_only=True)
    biotype = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    body_fat_percentage = serializers.SerializerMethodField()

    class Meta:
        model = PersonalInfo
        fields = '__all__'

    def get_body_fat_percentage(self, obj):
        return obj.body_fat_percentage if obj.body_fat_percentage else obj.calculate_body_fat_percentage()
