from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsAccountOwner

class AccountView(CreateAPIView,ListAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer


class NewestAccountView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
       filter_number = self.kwargs["num"]
       return self.queryset.order_by("-date_joined")[0:filter_number]

        
class PatchAccountView(UpdateAPIView):
        permission_classes = [IsAccountOwner]

        queryset = User.objects.all()
        serializer_class = UserSerializer

class SoftDeleteView(UpdateAPIView):
        permission_classes = [IsAdminUser]
        serializer_class = UserSerializer

        def get_queryset(self):
                user_id = self.kwargs['pk']
                queryset = User.objects.filter(id=user_id)
                queryset.update(is_active=not queryset[0].is_active)
                return queryset









