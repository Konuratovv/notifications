from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import Notification
from .serializers import NotificationSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
# Create your views here.

class CreateMessageAPIView(CreateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        text = serializer.validated_data['text']
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                "type": "send_notifications",
                "message": text,
            }
        )
        return Response({"message": "message send!"})
