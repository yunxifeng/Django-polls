from django.db import models
from django.utils import timezone
import datetime
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date publish')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        # 此处有bug-->
        # 期望: polls发生在当前时间的前一天之内
        # bug: polls发生在超出当前时间时同样返回true
        # 自动化测试代码见test.py
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

        # 修复bug
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()
    # 给方法增加属性来扩展功能
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    # on_update=cascade 关系表的级联更新：
    # on_delete=cascade 是级联删除的意思
    # 意思是当你更新或删除主键表时,那么外键表也会跟随一起更新或删除
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text



