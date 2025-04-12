
from .models import Todo,CustomUser
from .serializers import TodoSerializer, SignupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class SignupView(APIView):
    def post(self,request):
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'user created succesfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)



class TodoListCreate(APIView):
    """
    List all todos or create a new todo.
    in settings mention the authentication. else we will not get request.user 

    """
    def get(self, request):
        todos = Todo.objects.filter(user=request.user) # Python queryset
        serializer = TodoSerializer(todos, many=True)  # Serialization (Python ➡️ Python dict)
        return Response(serializer.data)   # .data ➡️ Python list of dicts ➡️ DRF converts to JSON

    def post(self, request):
        serializer = TodoSerializer(data=request.data, context={'user':request.user})   # Deserialization (JSON ➡️ Python)
        if serializer.is_valid():
            serializer.save()     # Save as Python model instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # .data ➡️ Python dict ➡️ DRF converts to JSON
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




'''we dont haave this view in web app . you can add that but not necessry.
But in API apps, we usually add /api/user/ because:
-We need a way to get the currently logged-in user's info.
-Frontend apps (like React or mobile apps) often use this.'''
