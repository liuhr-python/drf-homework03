from rest_framework import serializers, exceptions

from bookapp.models import Book, Press

"""
   出版社的序列化器  用于多表嵌套查询
 """
class PressModelSerializer(serializers.ModelSerializer):

    class Meta:
        # 指定序列化的模型
        model = Press
        # 指定要序列化的字段
        fields = ("press_name", "address", "pic",)


class BookModelSerializer(serializers.ModelSerializer):

    # TODO 自定义连表查询  查询图书时将图书对应的出版的信息完整的查询出来
    # 可以在序列化器中嵌套另一个序列化器来完成多表查询
    # 需要与图书表的中外键名保持一致  在连表查询较多字段时推荐使用
    publish = PressModelSerializer()

    class Meta:
        # 指定当前序列化器要序列化的模型
        model = Book
        # 指定你要序列化模型的字段
        # fields = ("book_name", "price", "pic", "publish","publish_name", "press_address", "author_list")
        fields = ("book_name", "price", "pic", "publish")

        # 直接查询所有字段
        # fields = "__all__"

        # 可以指定不展示哪些字段
        # exclude = ("is_delete", "create_time", "status")

        # 指定查询深度  关联对象的查询  可以查询出有外键关系的信息
        # depth = 1


