from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            org_name = f"{user.first_name}'s Organisation"
            Organisation.objects.create(name=org_name, users=[user])
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': serializer.data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Registration unsuccessful',
            'statusCode': 400,
            'errors': [
                {'field': k, 'message': v[0]} for k, v in serializer.errors.items()
            ]
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):
    def post(self, request):
        from django.contrib.auth import authenticate
        from rest_framework_simplejwt.tokens import RefreshToken

        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': serializer.data
                }
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = User.objects.filter(user_id=id).first()
        if user and (user == request.user or request.user in user.organisations.all()):
            serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'message': 'User retrieved successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Unauthorized',
            'message': 'Access denied',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)
