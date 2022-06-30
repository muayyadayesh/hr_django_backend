from lib2to3.pgen2.parse import ParseError
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from hr.serializers.serializers import CandidateSerializer, CandidateSerializerGet
from .models import Candidate
from rest_framework.parsers import MultiPartParser
from rest_framework import generics, exceptions, status, permissions


class CandidateListApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the candidate items for given requested candidate
        '''
        is_admin = request.headers.get('X-ADMIN')
        if is_admin == '1':

            candidates = Candidate.objects.order_by('-registration_date')
            serializer = CandidateSerializerGet(candidates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.AuthenticationFailed('Auth failed!')

    # 2. Create

    def post(self, request, *args, **kwargs):
        '''
        Create the Candidate with given candidate data
        '''

        if 'resume_file' not in request.data:
            raise ParseError("Empty resume file")

        data = {
            'full_name': request.data.get('full_name'),
            'date_of_birth': request.data.get('date_of_birth'),
            'experience_years': request.data.get('experience_years'),
            'department_id': request.data.get('department_id'),
            'resume_file': request.data.get('resume_file')
        }
        serializer = CandidateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "True", "data": serializer.data, "status": status.HTTP_201_CREATED})

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CandidateDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, candidate_id):
        '''
        Helper method to get the object with given user_id
        '''
        try:
            Candidate.objects.get(id=candidate_id)
            return Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, candidate_id, *args, **kwargs):
        '''
        Retrieves the Candidate with given candidate_id
        '''
        is_admin = request.headers.get('X-ADMIN')
        if is_admin == '1':
            candidate_instance = self.get_object(candidate_id)
            if not candidate_instance:
                return Response(
                    {"res": "Object with candidate id does not exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = CandidateSerializerGet(candidate_instance)
            return Response({'resume': serializer.data}, status=status.HTTP_200_OK)
        else:
            raise exceptions.AuthenticationFailed('Auth failed!')


class FileDownloadListAPIView(generics.ListAPIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, candidate_id):
        '''
        Helper method to get the object with given user_id
        '''
        try:
            Candidate.objects.get(id=candidate_id)
            return Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            return None

    def get(self, request, candidate_id, format=None):
        candidate_instance = self.get_object(candidate_id)

        is_admin = request.headers.get('X-ADMIN')
        if is_admin == '1':
            if not candidate_instance:
                return Response(
                    {"res": "Object with candidate id does not exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            file_handle = candidate_instance.resume_file.path
            document = open(file_handle, 'rb')
            response = HttpResponse(FileWrapper(document))
            response['Content-Disposition'] = 'attachment; filename="%s"' % candidate_instance.resume_file.name
            return response
        else:
            raise exceptions.AuthenticationFailed('Auth failed!')
