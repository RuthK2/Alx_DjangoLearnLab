from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'message': 'User created successfully', 'token': token.key}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful', 'token': token.key}, 
                        status=status.HTTP_200_OK)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            if user_id == request.user.id:
                return Response({'error': 'You cannot follow yourself'},
                                status=status.HTTP_400_BAD_REQUEST)
            user_to_follow = CustomUser.objects.get(id=user_id)
            request.user.following.add(user_to_follow)
            return Response({'message': f'You are now following {user_to_follow.username}'},
                            status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)
       
    
class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            if user_id == request.user.id:
                return Response({'error': 'You cannot unfollow yourself'},
                                status=status.HTTP_400_BAD_REQUEST)
            user_to_unfollow = CustomUser.objects.get(id=user_id)
            request.user.following.remove(user_to_unfollow)
            return Response({'message': f'You have unfollowed {user_to_unfollow.username}'},
                            status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)
        
    



