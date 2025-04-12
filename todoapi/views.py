
from .models import Todo
from .serializers import TodoSerializer, SignupSerializer, CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound




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


class TodoDetail(APIView):

    permission_classes = [permissions.IsAuthenticated]  # Ensures request.user is available

    def get_object(self, pk, user):
        try:
            return Todo.objects.get(pk=pk, user=user)
        except Todo.DoesNotExist:
            raise NotFound("Todo not found")

    def get(self, request, *args, **kwargs):
        print(kwargs['pk'],'....................')
        todo = self.get_object(kwargs['pk'], request.user)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs): # Full update – all fields must be provided
        todo = self.get_object(kwargs['pk'], request.user)
        serializer = TodoSerializer(todo, data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        todo = self.get_object(kwargs['pk'], request.user)
        todo.delete()
        return Response({"message": "Todo has been deleted"}, status=status.HTTP_204_NO_CONTENT)        


'''we dont haave this view in web app . you can add that but not necessry.
But in API apps, we usually add /api/user/ because:
-We need a way to get the currently logged-in user's info.
-Frontend apps (like React or mobile apps) often use this.'''

class UserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # User.objects.get(pk=request.user.id)  #  not necessary. You’re not editing other users, just the logged-in user — so there's no need to pass a pk in the URL or retrieve another user.
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request): #  Partial update – only send fields you want to change
        serializer = CustomUserSerializer(instance=request.user, data=request.data, partial=True) # partial(not required to send all fields)
        if serializer.is_valid():
            for field, value in serializer.validated_data.items():
                setattr(request.user, field, value)
            request.user.save()
            return Response({'message': 'Profile partially updated', 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
