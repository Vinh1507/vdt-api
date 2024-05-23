from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Student
from .serializers import StudentSerializer
from django.db.models import Q
import json

@api_view(['GET', 'POST'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/students',
        'GET /api/students/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getStudents(request):
    query = request.GET.get('query')
    if query is None: 
        query = ''
    students = Student.objects.filter(Q(full_name__icontains=query)).order_by('id')
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def getUpdateStudent(request, id):
    try:
        student = Student.objects.get(id=id)
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        student.full_name = body_data.get("full_name")
        student.gender = body_data.get("gender")
        student.school = body_data.get("school")
        student.email = body_data.get("email")
        student.phone = body_data.get("phone")
        student.country = body_data.get("country")
        student.save()
        serializer = StudentSerializer(student, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": "Update student failed"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def getCreateStudent(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def getDeleteStudent(request, id):
    try:
        student = Student.objects.get(id=id)
        student.delete()
        return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def getStudentDetail(request, id):
    try:
        student = Student.objects.get(id=id)
        serializer = StudentSerializer(student, many=False)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)