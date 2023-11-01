from django.db.models.functions import TruncMonth
from django.db.models import Count

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class GeneralListApiView(ListAPIView):
    serializer_class = None

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(state=True)


class TotalListApiView(ListAPIView):
    serializer_class = None

    def get_queryset(self):
        model = self.get_serializer().Meta.model.objects.all()
        total = model.count()
        return total

    def get(self, request, *args, **kwargs):
        model_name = (self.get_serializer().Meta.model.__name__).lower()
        response_label = f"total_{model_name}s"
        total = self.get_queryset()
        try:
            response = Response(
                {response_label: total},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            response = Response(
                {'error': 'There is a problem with the query.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return response


class BaseHistoricGroupByMonthListAPIView(ListAPIView):
    serializer_class = None

    def get_queryset(self):
        base = self.get_serializer_class().Meta.model.objects
        query = base.annotate(month=TruncMonth('created_date')).values('month').annotate(total=Count('id'))
        return query

    def list(self, request, *args, **kwargs):
        try:
            base_serializer = self.get_serializer(self.get_queryset(),
                                                  many=True)
        except Exception as e:
            response = Response({'message': str(e)},
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            response = Response(base_serializer.data,
                                status=status.HTTP_200_OK)

        return response
