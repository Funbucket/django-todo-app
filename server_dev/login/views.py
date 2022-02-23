from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LoginUser
from django.contrib.auth.hashers import make_password, check_password
from .serialize import LoginUserSerializer


class AppLogin(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', "")
        user_pw = request.data.get('user_pw', "")
        user = LoginUser.objects.filter(user_id=user_id).first()

        if user is None:
            return Response(dict(msg="해당 ID의 사용자가 없습니다."))

        if check_password(user_pw, user.user_pw):
            return Response(dict(msg="로그인 성공", user_id=user.user_id))
        else:
            return Response(dict(msg="로그인 실패. 패스워드 불일치"))


class RegistUser(APIView):
    def post(self, request):
        user_id = request.data['user_id']
        user_pw = request.data['user_pw']

        if user_id == '' or user_id is None or user_pw == '' or user_pw is None:
            return Response(data=dict(msg='아이디와 비밀번호는 공백이 될 수 없습니다.'))

        user_pw = make_password(user_pw)
        if LoginUser.objects.filter(user_id=user_id).exists():
            return Response(data=dict(msg='이미 존재하는 아이디입니다.'))
        LoginUser.objects.create(user_id=user_id, user_pw=user_pw)

        return Response(data=dict(msg="회원가입이 완료되었습니다.", user_id=user_id))


# class AppLogin(APIView):
#     def post(self, request):
#         serializer = LoginUserSerializer(request.data)
#         user = LoginUser.objects.filter(user_id=serializer.data["user_id"]).first()
#         user_pw = request.data.get('user_pw', "")
#
#         if user is None:
#             return Response(dict(msg="해당 사용자가 없습니다."))
#
#         if check_password(user_pw, user.user_pw):
#             return Response(dict(msg="로그인 성공"))
#         else:
#             return Response(dict(msg="비밀번호가 틀립니다."))


# class RegistUser(APIView):
#     def post(self, request):
#         serializer = LoginUserSerializer(request.data)
#
#         # 아이디 중복 확인
#         if LoginUser.objects.filter(user_id=serializer.data['user_id']).exists():
#             user = LoginUser.objects.filter(user_id=serializer.data['user_id']).first()
#             data = dict(
#                 msg='이미 존재하는 아이디입니다.',
#                 user_id=user.user_id,
#                 user_pw=user.user_pw
#             )
#             return Response(data)
#
#         user = serializer.create(request.data)
#
#         return Response(LoginUserSerializer(user).data)
