from rest_framework.serializers import (DateField, IntegerField,
                                        ModelSerializer)


class BaseHistoricGroupByMonthSerializer(ModelSerializer):
    month = DateField(format='%Y-%m')
    total = IntegerField()

    class Meta:
        model = None
        fields = '__all__'
