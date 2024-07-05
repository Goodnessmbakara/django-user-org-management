from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Organisation
from .serializers import  OrganisationSerializer

class OrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organisations = request.user.organisations.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            'status': 'success',
            'message': 'Organisations retrieved successfully',
            'data': {'organisations': serializer.data}
        }, status=status.HTTP_200_OK)

class SingleOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, org_id):
        organisation = Organisation.objects.filter(org_id=org_id, users=request.user).first()
        if organisation:
            serializer = OrganisationSerializer(organisation)
            return Response({
                'status': 'success',
                'message': 'Organisation retrieved successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Unauthorized',
            'message': 'Access denied',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)

class CreateOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            return Response({
                'status': 'success',
                'message': 'Organisation created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad Request',
            'message': 'Client error',
            'statusCode': 400,
            'errors': [
                {'field': k, 'message': v[0]} for k, v in serializer.errors.items()
            ]
        }, status=status.HTTP_400_BAD_REQUEST)

class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, org_id):
        organisation = Organisation.objects.filter(org_id=org_id, users=request.user).first()
        if not organisation:
            return Response({
                'status': 'Unauthorized',
                'message': 'Access denied',
                'statusCode': 401
            }, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.data.get('userId')
        user = User.objects.filter(user_id=user_id).first()
        if user:
            organisation.users.add(user)
            return Response({
                'status': 'success',
                'message': 'User added to organisation successfully',
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad Request',
            'message': 'User not found',
            'statusCode': 400
        }, status=status.HTTP_400_BAD_REQUEST)
