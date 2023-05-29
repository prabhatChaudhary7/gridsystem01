from django.shortcuts import render

# Create your views here.
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StudentSerializer
from .models import Student

class StudentPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as per your requirements

class LoadStudentDetailsAPI(APIView):
    def get(self, request):
        paginator = StudentPagination()
        students = Student.objects.all()
        page = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class FilterStudentAPI(APIView):
    def get(self, request):
        # Extract filter criteria from the request parameters
        name = request.GET.get('name', '')
        min_marks = request.GET.get('min_marks', None)
        max_marks = request.GET.get('max_marks', None)
        
        # Apply filters on the student queryset
        students = Student.objects.all()
        if name:
            students = students.filter(name__icontains=name)
        if min_marks:
            students = students.filter(total_marks__gte=min_marks)
        if max_marks:
            students = students.filter(total_marks__lte=max_marks)
        
        # Paginate the filtered results
        paginator = StudentPagination()
        page = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
