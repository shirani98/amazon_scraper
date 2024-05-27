from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product

class AmazonProductDetailView(APIView):
    def get(self, request, *args, **kwargs):
        product_id = request.query_params.get("product_id")
        if not product_id:
            return Response(
                {"error": "Product Id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            product_data = Product.fetch_data(product_id)
        except Exception:
            product_data = None
        if not product_data:
            return Response(
                {"error": "Failed to retrieve product data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
