from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.ForumHomeView.as_view(), name="forum_home_view"),
    path("create-post/", views.createPostView.as_view(), name="create_post_view"),
    path("create-question/", views.createQuestionView.as_view(), name="create_question_view"),
    path("create-question/", views.createQuestionView.as_view(), name="create_question_view"),
    path("detail-post/<int:ID>/", views.PostDetailView.as_view(), name="detail_post_view"),
    path("detail-question/<int:ID>/", views.QuestionDetailView.as_view(), name="detail_question_view"),
]