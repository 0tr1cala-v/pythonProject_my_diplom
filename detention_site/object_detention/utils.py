from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import numpy as np
import requests
import matplotlib.pyplot as plt
from io import BytesIO

# Загрузка модели и процессора для DETR (Detection Transformer)
model_name = "facebook/detr-resnet-50"
processor = DetrImageProcessor.from_pretrained(model_name)
model = DetrForObjectDetection.from_pretrained(model_name)

def detect_objects(image_path):
    # Загружаем изображение
    image = Image.open(image_path)

    # Предобработка изображения (конвертация в формат, необходимый для модели)
    inputs = processor(images=image, return_tensors="pt")

    # Получение предсказания
    outputs = model(**inputs)

    # Извлечение предсказанных объектов
    target_sizes = torch.tensor([image.size[::-1]])  # Указываем размер изображения для восстановления
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    # Отображаем результаты
    boxes = results["boxes"]
    labels = results["labels"]
    scores = results["scores"]

    # Возвращаем результаты в виде объектов
    return boxes, labels, scores


def plot_results(image_path, boxes, labels, scores):
    image = Image.open(image_path)
    plt.imshow(image)
    ax = plt.gca()

    # Рисуем прямоугольники вокруг объектов
    for box, label, score in zip(boxes, labels, scores):
        xmin, ymin, xmax, ymax = box.tolist()
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color="red", linewidth=3))
        ax.text(xmin, ymin, f"{model.config.id2label[label.item()]}: {score:.3f}",
                color="white", fontsize=8, bbox=dict(facecolor="red", alpha=0.5))

    plt.axis("off")
    plt.show()