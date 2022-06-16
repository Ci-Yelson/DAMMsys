from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # 0.过滤不需要此中间件的页面
        if request.path_info == '/' or request.path_info == '/register/':
            return None

        # 1.校验通过
        info_dict = request.session.get('info')
        if info_dict:
            # print(info_dict)
            return None
        
        # 2.没有登录过，返回登录页面
        return redirect('/')