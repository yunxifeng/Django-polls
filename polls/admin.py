from django.contrib import admin
from .models import Question, Choice
# Register your models here.


# class ChoiceInLine(admin.StackedInline):  # 使用堆叠的格式显示选项字段
class ChoiceInLine(admin.TabularInline):    # 使用表格式显示选项字段
    model = Choice
    extra = 3   # 设置默认显示3个选项字段,不可删除


class QuestionAdmin(admin.ModelAdmin):
    # 在Question编辑界面按照[ , ]内顺序显示字段
    # fields = ['pub_date', 'question_text'] # 适用于字段较少
    # 当字段较多时,也可分为多个字段集
    fieldsets = [
        (None, {'fields': ['question_text']}),  # 元组里第一个元素是分组名
        ('Date information', {'fields': ['pub_date']}),
    ]
    # Choice对象将会在Question的管理界面里被编辑,默认显示3个选项字段已供编辑
    inlines = [ChoiceInLine]
    # 在Question界面显示其他字段
    list_display = ['question_text', 'pub_date', 'was_published_recently']
    # 在Question界面给Question对象列表添加过滤功能,表现为一个快速过滤侧边栏
    list_filter = ['pub_date']
    # 搜索功能,搜索功能使用的是数据库查询语句中的like关键字
    search_fields = ['question_text']



# 在管理后台注册模型对象和模型管理对象
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)