from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os

from .models import ProductImage, Product, Classification1, Classification2, Chat


@receiver(post_delete, sender=Classification1)
def delete_c1_image(sender, instance, **kwargs):
    # 删除关联的图片文件
    image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))

    if os.path.exists(image_path):
        # os.remove(image_path)
        try:
            os.remove(image_path)
        except PermissionError as e:
            print(f"PermissionError: {e}")


@receiver(post_delete, sender=Classification2)
def delete_c2_image(sender, instance, **kwargs):
    # 删除关联的图片文件
    image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))

    if os.path.exists(image_path):
        # os.remove(image_path)
        try:
            os.remove(image_path)
        except PermissionError as e:
            print(f"PermissionError: {e}")


@receiver(post_delete, sender=ProductImage)
def delete_product_image(sender, instance, **kwargs):
    # 删除关联的图片文件
    image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))

    if os.path.exists(image_path):
        # os.remove(image_path)
        try:
            os.remove(image_path)
        except PermissionError as e:
            print(f"PermissionError: {e}")


@receiver(post_delete, sender=Product)
def delete_product_video(sender, instance, **kwargs):
    # 删除关联的视频文件
    video_path = os.path.join(settings.MEDIA_ROOT, str(instance.video))

    if os.path.exists(video_path):
        # os.remove(video_path)
        try:
            os.remove(video_path)
        except PermissionError as e:
            print(f"PermissionError: {e}")


@receiver(post_delete, sender=Chat)
def delete_chat_image(sender, instance, **kwargs):
    # 删除关联的图片文件
    image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))

    if os.path.exists(image_path):
        # os.remove(image_path)
        try:
            os.remove(image_path)
        except PermissionError as e:
            print(f"PermissionError: {e}")



