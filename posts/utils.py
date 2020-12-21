from django.contrib.contenttypes.models import ContentType
from posts.models import Like, Post
from authentication.models import User


def add_like(obj, user):
    """Add a like to an `obj`"""
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user):
    """Remove a like from an `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()


def liked(obj, user) -> bool:
    """Check whether a user liked an `obj` or not"""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj):
    """Get the users which liked an `obj`"""
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)


def get_post(obj, user):
    """Get the users which liked an `obj`"""
    obj_type = ContentType.objects.get_for_model(obj)
    return Post.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id, user=user)
