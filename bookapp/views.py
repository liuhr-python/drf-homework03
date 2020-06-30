from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from bookapp.models import Book
from .serializers import BookModelSerializer  # 导入序列化
from .serializers import BookDeModelSerializer  # 导入反序列化

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

    # 添加信息
    def post(self, request, *args, **kwargs):

        # 添加单个  （暂时与多个独立存在）
        # request_data = request.data
        #
        # # 将前端发送过来的数据交给反序列化器进行校验
        # book_ser = BookDeModelSerializer(data=request_data)
        #
        # # 校验数据是否合法 raise_exception：一旦校验失败 立即抛出异常
        # book_ser.is_valid(raise_exception=True)
        # book_obj = book_ser.save()
        #
        # return Response({
        #     "status": status.HTTP_200_OK,
        #     "message": "添加图书成功",
        #     "result": BookModelSerializer(book_obj).data
        # })

        # 添加多个
        request_data = request.data
        if isinstance(request_data, dict):  # 代表增加的是单个图书
            # 将前端发送过来的数据交给反序列化器进行校验
            many = False
        elif isinstance(request_data, list):  # 代表添加多个图书
            many = True
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "请求参数格式有误",
            })

        book_ser = BookDeModelSerializer(data=request_data, many=many)
        # 校验数据是否合法 raise_exception：一旦校验失败 立即抛出异常
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            # 当群增多个时，无法序列化多个对象到前台  所以报错
            "result": BookDeModelSerializer(book_obj, many=many).data
        })