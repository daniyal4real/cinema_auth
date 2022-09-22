from django.shortcuts import render
from rest_framework import status
from apps.kinopark.models import Movie, User
from apps.kinopark.models import Movie_details
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from apps.kinopark.serializers import MovieSerializer
from apps.kinopark.serializers import MovieDetailsSerializer
import pickle
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime, re


@api_view(['GET', 'POST', 'DELETE'])
def movies_list(request):
    if request.method == 'GET':
        # QuerySet
        movies = Movie.objects.all()
        # added the loader
        movies.query = pickle.loads(pickle.dumps(movies.query))
        movies.reverse()
        print(movies.query)
        print(movies.reverse())

        title = request.GET.get('title', None)
        if title is not None:
            movies = movies.filter(movie__icontains=title)
        movies_serializer = MovieSerializer(movies, many=True)
        return JsonResponse(movies_serializer.data, safe=False)

    elif request.method == 'POST':
        movie_data = JSONParser().parse(request)
        movie_serializer = MovieSerializer(data=movie_data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Movie.objects.all().delete()
        return JsonResponse({'message': '{} Фильмы были удалены!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


def movie_detail(request, id):
    try:
        movie_detail = Movie_details.objects.get(id=id)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie detail does not exit'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        movie_detail_serializer = MovieDetailsSerializer(movie_detail)
        return JsonResponse(movie_detail_serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_by_id(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return JsonResponse({'message': 'Movie does not exit'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        movie_serializer = MovieSerializer(movie)
        return JsonResponse(movie_serializer.data)

    elif request.method == 'PUT':
        movie_data = JSONParser().parse(request)
        movie_serializer = MovieSerializer(movie, data=movie_data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return JsonResponse(movie_serializer.data)
        return JsonResponse(movie_serializer.errors, stat=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movie.delete()
        return JsonResponse({'message': 'Movie was deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def unpublished_movies(request):
    movies = Movie.objects.filter(published=False)
    if request.method == 'GET':
        movies_serializer = MovieSerializer(movies, many=True)
        return JsonResponse(movies_serializer.data, safe=False)


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        # pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
        # container = JSONParser().parse(request)
        # print(container)
        # input_email = container.get("email")
        # print(input_email)
        # if re.search(pattern, input_email):
        #     if serializer.is_valid(raise_exception=True):
        #         serializer.save()
        #         return Response(serializer.data)
        #     else:
        #         return Response("Invalid email")
        # return Response("Invalid email")

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # response = Response({
        #     "jwt": token,
        #     'message': 'signed in successfully'
        # })

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Не авторизованный пользователь')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Не авторизованный пользователь')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'вышли успешно'
        }
        return response
