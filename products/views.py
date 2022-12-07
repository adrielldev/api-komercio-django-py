from rest_framework.generics import ListCreateAPIView,ListAPIView,UpdateAPIView
from products.models import Product
from .serializers import GeneralSerializer,DetailSerializer
from .utils.mixins import SerializerByMethodMixin
from .permissions import ProductPermission,ProductOwnerPermission
from rest_framework.authtoken.models import Token

class ProductView(SerializerByMethodMixin,ListCreateAPIView):
    permission_classes = [ProductPermission]
    queryset = Product.objects.all()
    serializer_map = {
        'GET':GeneralSerializer,
        'POST':DetailSerializer
    }
    def perform_create(self, serializer):
        user = Token.objects.get(key=self.request.headers['Authorization'][6:]).user
        serializer.save(seller=user)



class ProductIdView(ListAPIView,UpdateAPIView):
    permission_classes = [ProductOwnerPermission]
    
    serializer_class = DetailSerializer 
    def get_queryset(self):
        queryset = Product.objects.all()
        product_id = self.kwargs['pk']
        queryset = queryset.filter(id=product_id)
        return queryset
    
