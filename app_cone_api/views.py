from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import numpy


class ConeApiView(APIView):

    params = ['height', 'radius', 'segments']

    def get(self, request):

        # проверка обязательных параметров запроса
        for param in self.params:
            if param not in request.GET:
                return Response({'error': f'no parameter {param}'})
        try:
            height = int(request.GET.get("height"))
            radius = int(request.GET.get("radius"))
            segments = int(request.GET.get("segments"))

        except ValueError:
            return Response({'error': 'all parameters must be integers'})

        # Вычисление угла между каждым сегментом
        angle = 2 * numpy.pi / segments

        # Создание пустых списков для хранения точек и треугольников
        points = []
        triangles = []

        # Добавление верхней точки конуса
        top_point = numpy.array([0, height, 0])
        points.append(top_point)

        # Добавление точек основания конуса
        for i in range(segments):
            x = radius * numpy.cos(i * angle)
            z = radius * numpy.sin(i * angle)
            base_point = numpy.array([x, 0, z])
            points.append(base_point)

        # Добавление треугольников, образующих боковую поверхность конуса
        for i in range(segments):
            j = (i + 1) % segments  # Индекс следующей точки
            triangles.append([0, i + 1, j + 1])  # Верхний треугольник
            triangles.append([j + 1, i + 1, i + 2])  # Нижний треугольник

        # Добавление нижней точки конуса
        base_point = numpy.array([0, 0, 0])
        points.append(base_point)

        # Возврат массивов точек и треугольников
        return Response(
            {
                'points': numpy.array(points),
                'triangles': numpy.array(triangles),
            }
        )
