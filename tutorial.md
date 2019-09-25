# 创建项目
```
django-admin startproject sspanel
```
# 创建console应用
一个网站可能由多个部分组成，比如，主要页面，博客，wiki，下载区域等。
Django鼓励将这些部分作为分开的应用开发。如果这样的话，在需要时可以在不同的工程中复用这些应用。
```
python manage.py start app console
```
# 注册console应用
打开`sspanel/settings.py`找到  INSTALLED_APPS 列表里的定义。 如下所示，在列表的最后添加新的一行。
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'console.apps.ConsoleConfig', 
]
```

# 配置数据库
还是在settings.py里面
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sspanel',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
```

# 一些其他设置
· 设置时区: TIME_ZONE = 'Asia/Shanghai'
有两个设置你现在不会用到，留意一下：

SECRET_KEY. 这个密匙值是Django网站安全策略的一部分。如果在开发环境中没有包好这个密匙，把代码投入生产环境时最好用不同的密匙代替。（可能从环境变量或文件中读取）。
DEBUG. 这个会在debug日志里输出错误信息，而不是输入HTTP的返回码。在生产环境中，它应设置为false，因为输出的错误信息会帮助想要攻击网站的人。

# 链接URL映射器
```python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('console.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


```

# 测试网站框架
```shell
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```
重要信息: 每次模型改变，都需要运行以上命令，来影响需要存储的数据结构（包括添加和删除整个模型和单个字段）

该 makemigrations 命令创建（但不适用）项目中安装的所有应用程序的迁移（你可以指定应用程序名称，也可以为单个项目运行迁移）。这让你有机会在应用这些迁移之前检查这些迁移代码—当你是Django专家时，你可以选择稍微调整它们。

这 migrate 命令 明确应用迁移你的数据库（Django跟踪哪些已添加到当前数据库）。

# 运行网站
```shell
docker-compose up
```