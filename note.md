# 1.关于settings.py/[**INSTALLED_APPS**]

- [**django.contrib.admin**](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#module-django.contrib.admin) —— 管理站点。你可以快捷地使用它。
- [**django.contrib.auth**](https://docs.djangoproject.com/en/1.11/topics/auth/#module-django.contrib.auth) —— 认证系统。
- [**django.contrib.contenttypes**](https://docs.djangoproject.com/en/1.11/ref/contrib/contenttypes/#module-django.contrib.contenttypes) —— 内容类型框架。
- [**django.contrib.sessions**](https://docs.djangoproject.com/en/1.11/topics/http/sessions/#module-django.contrib.sessions) —— session 框架。
- [**django.contrib.messages**](https://docs.djangoproject.com/en/1.11/ref/contrib/messages/#module-django.contrib.messages) —— 消息框架。
- [**django.contrib.staticfiles**](https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#module-django.contrib.staticfiles) —— 静态文件管理框架。

# 2.条件查询

```
# 查找 API 的关键字参数可以自动调用关系函数。
# 只需使用双下划线来分隔关系函数。
# 只要你想，这个调用链可以无限长。
# 例如查找所有「所在问题的发布日期是今年」的选项
# （重用我们之前创建的 'current_year' 变量）
>>> Choice.objects.filter(question__pub_date__year=current_year)
```

# 3.URLconf

- 为了将 URL 和视图关联起来，Django 使用了 “URLconfs” 来配置。URLconf 将 URL 模式（表现为一个正则表达式）映射到视图。

# 4. get_object_or_404(Question, id=1)

[**get_object_or_404()**](https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/#django.shortcuts.get_object_or_404) 函数的第一个参数是一个 Django 模型。在此之后可以有任意个的关键字参数，他们会被直接传递给模型的 [**get()**](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#django.db.models.query.QuerySet.get) 函数。如果对象并不存在，此快捷函数将会抛出一个 [**Http404**](https://docs.djangoproject.com/en/1.11/topics/http/views/#django.http.Http404) 异常

> **设计哲学**
>
> 为什么我们使用辅助函数 [**get_object_of_404()**](https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/#django.shortcuts.get_object_or_404) 而不是自己捕获 [**ObjectDoesNotExist**](https://docs.djangoproject.com/en/1.11/ref/exceptions/#django.core.exceptions.ObjectDoesNotExist) 异常呢？或者，为什么模型 API 不直接抛出 [**Http404**](https://docs.djangoproject.com/en/1.11/topics/http/views/#django.http.Http404) 而是抛出 [**ObjectDoesNotExist**](https://docs.djangoproject.com/en/1.11/ref/exceptions/#django.core.exceptions.ObjectDoesNotExist) 呢？
>
> 因为这样做会增加模型层和视图层的耦合度。指导 Django 设计的最重要的思想之一就是要保证松散耦合。一些受控的耦合将会被包含在 [**django.shortcuts**](https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/#module-django.shortcuts) 模块中。

也有 [**get_list_of_404()**](https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/#django.shortcuts.get_object_or_404) 函数，工作原理和 [**get_object_of_404()**](https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/#django.shortcuts.get_object_or_404) 一样，除了 [**get()**](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#django.db.models.query.QuerySet.get) 函数被换成了 [**filter()**](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#django.db.models.query.QuerySet.filter)函数。如果列表为空的话会抛出 [**Http404**](https://docs.djangoproject.com/en/1.11/topics/http/views/#django.http.Http404) 异常。

# 5.关于detail.html的简要说明

- 上面的模板在 Question 的每个 Choice 前添加一个单选按钮。 每个单选按钮的 **value** 属性是对应的各个 Choice 的 ID。每个单选按钮的 **name** 是 **"choice"**。这意味着，当有人选择一个单选按钮并提交表单提交时，它将发送一个 POST 数据 choice=#，其中# 为选择的 Choice 的 ID。这是 HTML 表单的基本概念。
- 我们设置表单的 **action** 为 **{% url 'polls:vote' question.id %}**，并设置 **method="post"**。使用 **method="post"**（与其相对的是**method="get"**）是非常重要的，因为这个提交表单的行为会改变服务器端的数据。 无论何时，当你需要创建一个改变服务器端数据的表单时，请使用 **method="post"**。这不是 Django 的特定技巧；这是优秀的网站开发实践。
- **forloop.counter** 指示 [**for**](https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#std:templatetag-for) 标签已经循环多少次。
- 由于我们创建一个 POST 表单（它具有修改数据的作用），所以我们需要小心跨站点请求伪造。 谢天谢地，你不必太过担心，因为 Django 已经拥有一个用来防御它的非常容易使用的系统。 简而言之，所有针对内部 URL 的 POST 表单都应该使用 [**{% csrf_token %}**](https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#std:templatetag-csrf_token) 模板标签。

# 6.使用通用视图(原理不理解)

# 7.Django 测试工具之 Client





