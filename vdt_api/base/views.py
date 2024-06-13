from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Student
from base.models import VdtUser
from .serializers import StudentSerializer
from django.db.models import Q
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt

@api_view(['GET', 'POST'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/students',
        'GET /api/students/:id',
    ]
    return Response(routes)

@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['GET'])
def getStudents(request):
    query = request.GET.get('query')
    if query is None: 
        query = ''
    students = Student.objects.filter(Q(full_name__icontains=query)).order_by('id')
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = VdtUser.objects.get(username=username, password=password)
            # Tạo token
            payload = {
                'user_id': user.id,
                'username': user.username,
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse({'token': token})
        except VdtUser.DoesNotExist:
            return JsonResponse({'error': 'Đăng nhập không thành công'}, status=401)
    else:
        return JsonResponse({'error': 'Phương thức không được hỗ trợ'}, status=405)