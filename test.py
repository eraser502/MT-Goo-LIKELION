from django.test import Client, TestCase
from django.test.utils import setup_test_environment
import json

# Django 설정 초기화
setup_test_environment()

client = Client()

# 로그인
login_data = {
    'email': 'dohun@naver.com',
    'password': 'a13579246'
}
response = client.post('/accounts/user/signin/', data=json.dumps(login_data), content_type='application/json')
access_token = response.json().get('token')

# 로그인 후 리뷰 작성
data = {
    'lodging_id': 1,
    'score': 4.5,
    'contents': '좋은 숙소였습니다.'
}
headers = {'HTTP_AUTHORIZATION': 'Bearer ' + access_token}
response = client.post('/lodging/create_review/', data=json.dumps(data), content_type='application/json', **headers)
print(response.status_code)
print(response.json())

