from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
# from django.template import loader
# from django.http import Http404
from .models import Question, Choice
from django.core.urlresolvers import reverse
# 使用通用视图
from django.views import generic
from django.utils import timezone
# Create your views here.


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     context_index = {
#         'latest_question_list': latest_question_list,
#     }
#     # return HttpResponse(template.render(context, request))
#     return render(request, r'polls/index.html', context=context_index)
# -views.index改良如下---------------------------------------------------------------------------
class IndexView(generic.ListView):
    # ListView: 抽象“显示一个对象列表”
    # 类似地，ListView 使用一个叫做 "<app name>/<model name>_detail.html" 的默认模板
    template_name = 'polls/index.html'
    # django提供的是<model name>_list,即question_list
    # 模板中使用的是自定义的latest_question_list
    # 因此这里使用context_object_name自定义来覆盖django提供的<model name>_list
    context_object_name = 'latest_question_list'

    # 得到"列表"的填充内容
    def get_queryset(self):
        # 返回最近时间的5个问题
        # return Question.objects.order_by('-pub_date')[:5]
        # 改善此函数,使不显示未来的问题
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# def detail(request, question_id):
    # try:
    #     question = Question.objects.get(id=question_id)
    #     context_detail = {
    #         "question": question,
    #     }
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist!")
    # else:
    #     return render(request, r'polls/detail.html', context=context_detail)
    # 或者使用get_object_or_404, 推荐下面这种
    # question = get_object_or_404(Question, id=question_id)
    # context_detail = {
    #     "question": question,
    # }
    # return render(request, r'polls/detail.html', context=context_detail)
# -views.detail改良如下-------------------------------------------------------------------------------------
class DetailView(generic.DetailView):
    # DetailView: 抽象“显示一个特定类型对象的详细信息页面”
    # 每个通用视图需要知道它将作用于哪个模型。 这由 model 属性提供。
    # model属性: 告诉视图将要作用的模型是哪个
    # 同时提供question变量
    model = Question
    # 默认情况下，通用视图 DetailView 使用一个叫做 "<app name>/<model name>_detail.html" 的模板。
    # 即'polls/question_detail.html'
    # template_name属性: 告诉django,使用自定义的模板名称,而不使用自动生成的模板名称
    template_name = 'polls/detail.html'

    # 防止用户通过猜测url的方式访问未来的问题
    def get_queryset(self):
        '''
        过滤现在不应该被发布的投票
        测试内容见test.py
        :return:
        '''
        return Question.objects.filter(pub_date__lte=timezone.now())


# def results(request, question_id):
#     question = Question.objects.get(id=question_id)
#     context_results = {
#         "question": question,
#     }
#     return render(request, r'polls/results.html', context=context_results)


# -views.results改良如下----------------------------------------------------------------------------------------------------------
class ResultsView(generic.DetailView):
    model = Question
    # template_name属性也确保DetailView和ResultsView两个在后台同属于DetailView通用视图的视图使用不同的模板
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context_vote = {
            "question": question,
            "error_message": "You didn't select a choice.",
        }
        return render(request, r'polls/detail.html', context=context_vote)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))