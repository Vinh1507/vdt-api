from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Student
from .serializers import StudentSerializer
from django.forms.models import model_to_dict

class StudentAPITest(APITestCase):
    def setUp(self):
        self.student1 = Student.objects.create(full_name="Nguyen Van A", gender="Nam", school="PTIT", email="anv@gmail.com", phone="0912345676", country="Vietnam")
        self.student2 = Student.objects.create(full_name="Nguyen Van B", gender="Nữ", school="BKHN", email="anv@gmail.com", phone="0912345676", country="Vietnam")
        self.valid_payload = {
            'full_name': 'Bùi Nam Giang',
            'gender': 'Nam',
            'school': 'UET',
            'email': 'valid@gmail.com',
            'phone': '0914202457',
            'country': 'Nga'
        }
        self.invalid_payload = {
            'full_name': '',
            'gender': 'Nữ',
            'school': 'UET',
            'email': 'valid@gmail.com',
            'phone': '0914202457',
            'country': 'Nga'
        }

    # test api path('students/', views.getStudents, name='student_list'),
    def test_get_all_students(self):
        response = self.client.get(reverse('student_list'))
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # test api path('students/create', views.getCreateStudent, name='student_create') (1)
    def test_create_valid_student(self):
        count_before = Student.objects.count()
        response_create = self.client.post(
            reverse('student_create'),
            data=self.valid_payload,
            format='json'
        )
        count_after = Student.objects.count()
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_before + 1, count_after)

    # test api path('students/create', views.getCreateStudent, name='student_create') (2)
    def test_create_invalid_student(self):
        count_before = Student.objects.count()
        response_create = self.client.post(
            reverse('student_create'),
            data=self.invalid_payload,
            format='json'
        )
        count_after = Student.objects.count()
        self.assertEqual(response_create.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count_before, count_after)

    # test api path('students/update/<id>', views.getUpdateStudent, name='student_update') (1)
    def test_update_valid_student(self):
        count_before = Student.objects.count()
        test_student_id = count_before / 2
        student_before = Student.objects.get(id=test_student_id)
        response_update = self.client.put(
            reverse('student_update', kwargs={'id': student_before.id}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        student_after = Student.objects.get(id=test_student_id)
        self.assertEqual(student_after.full_name, 'Bùi Nam Giang')
        count_after = Student.objects.count()
        self.assertEqual(count_before, count_after)

    # test api path('students/update/<id>', views.getUpdateStudent, name='student_update') (2)
    def test_update_invalid_student(self):
        count_before = Student.objects.count()
        test_student_id = int(count_before / 2)
        student_before = Student.objects.get(id=test_student_id)
        student_before.phone = '012634812312412123412344'
        student_before_dict = model_to_dict(student_before)
        response_update = self.client.put(
            reverse('student_update', kwargs={'id': student_before.id}),
            data=student_before_dict,
            format='json'
        )
        self.assertEqual(response_update.status_code, status.HTTP_400_BAD_REQUEST)
    
    # test api path('students/delete/<id>', views.getDeleteStudent, name='student_delete') (1)
    def test_delete_valid_student(self):
        count_before = Student.objects.count()
        test_student_id = int(count_before - 10)
        student_before = Student.objects.get(id=test_student_id)
        response_delete = self.client.delete(
            reverse('student_delete', kwargs={'id': student_before.id}),
        )
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        count_after = Student.objects.count()
        self.assertEqual(count_before - 1, count_after)

    # test api path('students/delete/<id>', views.getDeleteStudent, name='student_delete') (2)
    def test_delete_invalid_student(self):
        count_before = Student.objects.count()
        test_student_id = int(count_before + 10)
        response_delete = self.client.delete(
            reverse('student_delete', kwargs={'id': test_student_id}),
        )
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)
        count_after = Student.objects.count()
        self.assertEqual(count_before, count_after)

    # test api path('students/<id>', views.getStudentDetail, name='student_get_detail'),
    def test_get_detail_valid_student(self):
        count = Student.objects.count()
        test_student_id = int(count - 10)
        student_before = Student.objects.get(id=test_student_id)
        serializer = StudentSerializer(student_before, many=False)
        response_get = self.client.get(
            reverse('student_get_detail', kwargs={'id': test_student_id}),
        )
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.data, serializer.data)

    # test api path('students/<id>', views.getStudentDetail, name='student_get_detail'),
    def test_get_detail_invalid_student(self):
        count = Student.objects.count()
        test_student_id = int(count + 100)
        print(test_student_id)
        response_get = self.client.get(
            reverse('student_get_detail', kwargs={'id': test_student_id}),
        )
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)