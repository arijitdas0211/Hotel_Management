from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from django.db.models import Model
import traceback

# GET Method
def handleGetMethod(ModelName: Model, model, ModelSerlializer: ModelSerializer, pk=int | None):
    try:
        if pk is not None:
            model = ModelName.objects.filter(id=pk).first()
            if not model:
                return Response({"error": f"{model} not found."})
            else:
                serializer = ModelSerlializer(model)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            model_list = ModelName.objects.all()
            serializer = ModelSerlializer(model_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception:
        traceback.print_exc()
        return Response({"error": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PATCH Method
def handlePatchMethod():
    pass


# DELETE Method
def handleDeleteMethod():
    pass


