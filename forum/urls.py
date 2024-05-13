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
    path("post-comment-reply/<int:ID>/<int:POST_ID>/", views.PostReplyCommentView.as_view(), name="post_comment_reply_view"),
    path("question-comment-reply/<int:ID>/<int:QUESTION_ID>/", views.QuestionReplyCommentView.as_view(), name="question_comment_reply_view"),
]