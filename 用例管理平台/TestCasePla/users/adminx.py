# users/adminx.py

import xadmin

from .models import Userpro
from xadmin import views


#创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True

# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '测试用例管理平台'
    # 修改footer
    site_footer = '链为科技'
    # 收起菜单
    menu_style = 'accordion'



class UserproAdmin(object):
    list_display = ['loginName']


#
# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)

# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)