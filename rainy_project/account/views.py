from django.shortcuts import render

import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import UserAccount


# Create your views here.
def index(request):
    return HttpResponse("account page.")

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        UserAccount(
            email = data['email'],
            password = data['password']
        ).save()

        return HttpResponse({'message':'Sign Up Finish'}, status = 200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        if UserAccount.objects.filter(email = data['email']).exists():
            user = UserAccount.objects.get(email = data['email'])
            if user.password == data['password'] :
                return JsonResponse({'message':'{user.email}님 로그인 성공!'}, status=200)
            else :
                return JsonResponse({'message':'비밀번호가 틀렸어요'},status = 200)

        return HttpResponse({'message':'등록되지 않은 이메일 입니다.'},status=200)