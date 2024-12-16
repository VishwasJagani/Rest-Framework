from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status

from django.contrib.auth import authenticate
from home.models import *
from home.serializer import *


@api_view(['POST'])
def login(request):
    try:
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid():
            data = serializer.validated_data
            return Response({"Message": "Success"})

        return Response(serializer.errors)

    except Exception as error:
        return Response(error)


@api_view(['GET', 'POST', 'PUT'])
def index(request):
    course = {
        'name': 'Python',
        'learn': ['Flask', 'Django', 'FastApi'],
        'provider': 'Vishwas'
    }
    if request.method == "GET":
        query = request.GET.get('search')
        if query:
            course['search'] = query
        course.update({'method': 'This is get'})
        return Response(course)

    if request.method == "POST":
        # Here request.data is used to get data from front-end
        data = request.data
        # data.update({"sname":"PQR"})
        return Response(data)

    if request.method == "PUT":
        if 'learn' in course:
            course['learn'].append('ABC')
            return Response(course)
        else:
            course.update({'learn': ['ABC']})
            return Response(course)


@api_view(['GET', 'POST'])
def people(request):
    if request.method == "GET":
        data = person.objects.all()
        serializer = PersonSerializer(data, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


# Put is used when we want to change all the field
# Patch is used when we want to change only one or two fields
@api_view(['PUT', 'PATCH'])
def edit_people(request):
    try:
        # Check if ID is present in request data
        data = request.data
        person_id = data.get('id')
        if not person_id:
            return Response({"error": "'id' field is required"}, status=400)

        obj = person.objects.get(id=person_id)

        if request.method == "PUT":
            # Full update
            serializer = PersonSerializer(obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        if request.method == "PATCH":
            # Partial update
            serializer = PersonSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

    except person.DoesNotExist:
        return Response({"error": "Person not found"}, status=404)


@api_view(['DELETE'])
def delete(request):
    try:
        data = request.data
        person_id = data.get('id')
        if not person_id:
            return Response({"Message": "Please Enter Id"})
        obj = person.objects.get(id=person_id)
        obj.delete()
        return Response({"Message": "Person Deleted"})

    except Exception:
        return Response({"Message": "Person Not Found"})


@api_view(['GET', 'POST'])
def color(request):
    try:
        if request.method == "GET":
            data = Color.objects.all()
            serializer = ColorSerializer(data, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            data = request.data
            serializer = ColorSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors)

    except Exception as error:
        return Response(error)


class PersonApi(APIView):

    def get(self, request):
        # Here We can write get api to get all the data like above
        return Response({"message": "This is a Get Request"})

    def post(self, request):
        # Here We can write post api to post the data like above
        return Response({"message": "This is a Post Request"})

    def put(self, request):
        # Here We can write put api to update the data like above
        return Response({"message": "This is a Put Request"})


# It is used to Create CRUD operation in just two lines
class PeopleViewset(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = person.objects.all()

    # To implement search functionality
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset

        if search:
            queryset = queryset.filter(name__startswith=search)
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)


# Authentication
class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "Message": "User Created"}, status.HTTP_201_CREATED)

        return Response({"status": False, "message": serializer.errors}, status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['username'],password = serializer.data['password'])
            return Response({"status": True, "Message": "Successfull"}, status.HTTP_201_CREATED)

        return Response({"status": False, "message": serializer.errors}, status.HTTP_400_BAD_REQUEST)
