from rest_framework import serializers, exceptions

from bookapp.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    """
    出版社的序列化器
    """

    class Meta:
        # 指定序列化的模型
        model = Press
        # 指定要序列化的字段
        fields = ("press_name", "address", "pic",)


class BookModelSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定当前序列化器要序列化的模型
        model = Book
        # 指定你要序列化模型的字段
        fields = ("book_name", "price", "pic", "publish","publish_name", "press_address", "author_list")

        # 直接查询所有字段
        # fields = "__all__"

        # 可以指定不展示哪些字段
        # exclude = ("is_delete", "create_time", "status")

        # 指定查询深度  关联对象的查询  可以查询出有外键关系的信息
        # depth = 1


