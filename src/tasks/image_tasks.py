# from PIL import Image
# from io import BytesIO
# import os
# from src.celery_app import celery_app  # Используем существующий celery_app
#
# @celery_app.task(name="src.tasks.image_tasks.process_image")
# def process_image(task_id, image_filename, transformations):
#     image_path = os.path.join("images", image_filename)
#
#     img = Image.open(image_path)
#     for transformation in transformations:
#         if transformation == "rotate":
#             img = img.rotate(90)
#         elif transformation == "gray":
#             img = img.convert("L")
#         elif transformation == "scale":
#             img = img.resize((img.width // 2, img.height // 2))
#
#     processed_image_filename = f"{task_id}_processed.jpg"
#     processed_image_path = os.path.join("images", processed_image_filename)
#     img.save(processed_image_path)
#
#     return processed_image_path
