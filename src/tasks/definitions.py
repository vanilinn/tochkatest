from celery import shared_task
from PIL import Image
import os


@shared_task(name="src.tasks.definitions.process_image")
def process_image(task_id, image_filename, transformations):
    print(f"Processing task {task_id} for file {image_filename}")

    # Путь к исходному изображению
    image_path = os.path.join("images", image_filename)
    img = Image.open(image_path)

    # Список для хранения путей к обработанным изображениям
    processed_images = []

    # Устанавливаем имена файлов для каждой трансформации
    transform_names = {
        "rotate": f"{task_id}_rotated.jpg",
        "gray": f"{task_id}_gray.jpg",
        "scale": f"{task_id}_scaled.jpg"
    }

    # Создаем обработанные изображения
    for transformation in ["rotate", "gray", "scale"]:
        processed_image = img.copy()  # Копируем исходное изображение для каждой трансформации

        if transformation == "rotate":
            processed_image = processed_image.rotate(90)
            processed_image_filename = transform_names["rotate"]
        elif transformation == "gray":
            processed_image = processed_image.convert("L")
            processed_image_filename = transform_names["gray"]
        elif transformation == "scale":
            processed_image = processed_image.resize((processed_image.width // 2, processed_image.height // 2))
            processed_image_filename = transform_names["scale"]

        # Сохраняем обработанное изображение
        processed_image_path = os.path.join("images", processed_image_filename)
        processed_image.save(processed_image_path)
        processed_images.append(processed_image_path)

    return processed_images
