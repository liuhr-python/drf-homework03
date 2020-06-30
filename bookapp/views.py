from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from bookapp.models import Book
from .serializers import BookModelSerializer  # 导入序列化


class BookAPIView(APIView):

    # 查询信息
    def get(self, request, *args, **kwargs):
        # 查询单个
        book_id = kwargs.get("id")
        if book_id:

            book_obj = Book.objects.get(pk=book_id)  # 获取id
            book_ser = BookModelSerializer(book_obj).data   # 转化格式
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询单个图书成功",
                "results": book_ser
            })

        else:
            # 查询全部
            book_list = Book.objects.all()
            book_list_ser = BookModelSerializer(book_list, many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询所有图书成功",
                "results": book_list_ser
            })

