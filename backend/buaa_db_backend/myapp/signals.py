from django.core.files.storage import default_storage
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
import os

from .models import ProductImage, Product, Classification1, Classification2, Chat, User


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


# def delete_old_file(instance, file_field):
#     # 获取旧文件路径
#     old_instance = instance.__class__.objects.get(pk=instance.pk)
#     old_file_path = getattr(old_instance, file_field).path if getattr(old_instance, file_field) else None
#
#     if old_file_path:
#         try:
#             # 删除旧文件
#             if default_storage.exists(old_file_path):
#                 default_storage.delete(old_file_path)
#         except Exception as e:
#             print(f"Error deleting old file: {e}")
#
#
# @receiver(pre_save, sender=User)
# def delete_old_user_avatar(sender, instance, **kwargs):
#     # 检查数据库中是否存在匹配的记录
#     try:
#         old_instance = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         return
#
#     delete_old_file(old_instance, 'avatar')
#
#
# @receiver(pre_save, sender=Classification1)
# def delete_old_c1_image(sender, instance, **kwargs):
#     # 检查数据库中是否存在匹配的记录
#     try:
#         old_instance = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         return
#
#     delete_old_file(old_instance, 'image')
#
#
# @receiver(pre_save, sender=Classification2)
# def delete_old_c2_image(sender, instance, **kwargs):
#     # 检查数据库中是否存在匹配的记录
#     try:
#         old_instance = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         return
#
#     delete_old_file(old_instance, 'image')
#
#
# @receiver(pre_save, sender=Product)
# def delete_old_product_video(sender, instance, **kwargs):
#     # 检查数据库中是否存在匹配的记录
#     try:
#         old_instance = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         return
#
#     delete_old_file(old_instance, 'video')
#
#
# @receiver(pre_save, sender=Chat)
# def delete_old_chat_image(sender, instance, **kwargs):
#     # 检查数据库中是否存在匹配的记录
#     try:
#         old_instance = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         return
#
#     delete_old_file(old_instance, 'image')
