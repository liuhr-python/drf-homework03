from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from bookapp.models import Book
from .serializers import BookModelSerializer  # 导入序列化
from .serializers import BookDeModelSerializer  # 导入反序列化
from .serializers import BookModelSerializerV2  # 导入整合序列化器


# 在序列化器与反序列化器  分离情况下的类试图

class BookAPIView(APIView):

    # 查询信息
    def get(self, request, *args, **kwargs):
        # 查询单个
        book_id = kwargs.get("id")
        if book_id:

            book_obj = Book.objects.get(pk=book_id)  # 获取id
            book_ser = BookModelSerializer(book_obj).data  # 转化格式
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


# 在序列化器与反序列化器 整合情况下的类试图
class BookAPIViewV2(APIView):

    # 查询信息
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            print(book_id)
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
            print(book_obj, type(book_obj), "1111")
            book_ser = BookModelSerializerV2(book_obj).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询单个图书成功",
                "results": book_ser
            })

        else:
            book_list = Book.objects.filter(is_delete=False)
            book_list_ser = BookModelSerializerV2(book_list, many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询所有图书成功",
                "results": book_list_ser
            })

    # 添加信息
    def post(self, request, *args, **kwargs):

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

        book_ser = BookModelSerializerV2(data=request_data, many=many)
        # 校验数据是否合法 raise_exception：一旦校验失败 立即抛出异常
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            # 当群增多个时，无法序列化多个对象到前台  所以报错
            "result": BookModelSerializerV2(book_obj, many=many).data
        })

    # 删除信息
    def delete(self, request, *args, **kwargs):

        book_id = kwargs.get("id")
        if book_id:
            # 删除单个  也作为删除多个
            ids = [book_id]
        else:
            # 删除多个
            ids = request.data.get("ids")

        # 判断传递过来的图书的id是否在数据库  且还未删除
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败或图书不存在"
        })

    # 修改单个的整体信息
    def put(self, request, *args, **kwargs):

        # 修改的参数
        request_data = request.data
        # 要修改的图书的id
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })

        #  指定instance参数  指定修改的实例
        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)

        # 经过序列化器规则校验 局部全局钩子校验通过后则调用 update()方法完成更新
        book_ser.save()

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializerV2(book_obj).data
        })