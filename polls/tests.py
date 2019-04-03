from django.test import TestCase
from .models import Question
import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your tests here.


class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        对于pub_date在未来的Question, was_published_date()应该返回False
        :return:
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    # 更全面的测试
    def test_was_published_recently_with_old_question(self):
        '''
        对于pub_date在一天之前的Question, was_published_date()应该返回False
        :return:
        '''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''
        对于当前时间前一天之内的Question, was_published_date()应该返回True
        :return:
        '''
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), True)


# 测试IndexView
def create_question(question_text, days):
    '''
    创建一个以question_text为标题,pub_date为days的Question
    :param question_text: Question's Title
    :param days: pub_date, days为正表示将来,为负表示过去
    :return: Question
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        '''
        如果数据库里没有保存问题,给出相应提示
        :return:
        '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        '''
        如果值是过去的,问题应该被显示在主页上
        :return:
        '''
        create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['last_question_list'], ['<Question: Past question>'])

    def test_future_question(self):
        '''
        如果值是未来的,问题不应该显示在主页上
        :return:
        '''
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        '''
        如果pub_date值包含过去的和未来的,那么只显示过去的那些
        :return:
        '''
        create_question(question_text="Future question", days=30)
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

    def test_two_past_questions(self):
        '''
        Question索引页应该可以显示多个问题
        :return:
        '''
        create_question(question_text="Past question 1", days=-30)
        create_question(question_text="Past question 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2>',
                                                                            '<Question: Past question 1>'])


# 测试DetailView
class QuestionDetailTests(TestCase):
    def test_future_question(self):
        '''
        访问将来发布的问题详情页应该会收到一个404错误
        :return:
        '''
        future_question = create_question(question_text="Future question", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        访问过去发布的问题详情页, 页面上应该显示问题描述
        :return:
        '''
        past_question = create_question(question_text="Past question", days=-5)
        url = reverse('polls:detail', args=past_question.id)
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


'''
# 测试未通过
(Django_Study) E:\mysite>python manage.py test polls
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_was_published_recently_with_future_question (polls.tests.QuestionModelTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "E:\mysite\polls\tests.py", line 17, in test_was_published_recently_with_future_question
    self.assertIs(future_question.was_published_recently(), False)
AssertionError: True is not False

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
Destroying test database for alias 'default'...

'''


'''
1.python manage.py test polls 将会寻找 polls 应用里的测试代码
2.它找到了一个 django.test.TestCase 的子类
3.它创建一个特殊的数据库供测试使用
4.它在类中寻找测试方法——以 test 开头的方法。
5.在 test_was_published_recently_with_future_question 方法中，它创建了一个 pub_date 值为未来第 30 天的 Question 实例。
6.然后使用 assertIs() 方法，发现 was_published_recently() 返回了 True，而我们希望它返回 False
'''

'''
# 测试通过
Creating test database for alias 'default'...
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'...

'''