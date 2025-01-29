from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import ImageFeedForm
from .utils import detect_objects, plot_results
from django.conf import settings
import os
# Create your views here.


def home(request):
    return render(request, 'object_detection/home.html')


def dashboard(request):
    # Здесь можно добавить логику для получения изображений пользователя
    images = []  # Пример данных
    return render(request, 'object_detection/dashboard.html', {'images': images})


def add_image(request):
    if request.method == 'POST' and request.FILES['image']:
        # Получаем загруженное изображение
        uploaded_image = request.FILES['image']
        image_path = os.path.join(settings.MEDIA_ROOT, 'images', uploaded_image.name)

        # Создаем директорию, если она не существует
        os. makedirs(os.path.dirname(image_path), exist_ok=True)

        # Сохраняем изображение на сервере
        with open(image_path, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        # Выполняем детекцию объектов с помощью модели
        boxes, labels, scores = detect_objects(image_path)

        # Отображаем результаты
        plot_results(image_path, boxes, labels, scores)

        return render(request, 'object_detection/add_image_feed.html', {
            'image_url': uploaded_image.url,
            'boxes': boxes,
            'labels': labels,
            'scores': scores,
        })
    return render(request, 'object_detection/add_image_feed.html')


def login_view(request):
    return render(request, 'object_detection/login.html')


def register(request):
    return render(request, 'object_detection/register.html')


