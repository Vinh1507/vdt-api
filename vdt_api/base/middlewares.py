import jwt
from django.conf import settings
from .models import VdtUser
from django.http import JsonResponse

class JWTMiddleware:
    EXCLUDED_PATHS = ['/api/login/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization', None)

        path = request.path_info
        if path in self.EXCLUDED_PATHS:
            return self.get_response(request)
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                print(payload)
                user_id = payload.get('user_id', None)
                
                if user_id:
                    user = VdtUser.objects.get(id=user_id)
                    request.user_info = user
                    response = self.get_response(request)
                    return response
                else:
                    return JsonResponse({'error': 'Tài khoản không tồn tại'}, status=403)
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token hết hạn'}, status=403)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Token không hợp lệ'}, status=403)

        return JsonResponse({'error': 'Token không hợp lệ'}, status=403)


class AuthorMiddleware:
    EXCLUDED_PATHS = ['/api/login/']
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        if path in self.EXCLUDED_PATHS:
            return self.get_response(request)
        user = request.user_info
        
        if request.method in ["POST", "DELETE"]:
            if user.role == 'admin':
                return self.get_response(request)
            else:
                return JsonResponse({'error': 'User không đủ thẩm quyền'}, status=403)
        return self.get_response(request)