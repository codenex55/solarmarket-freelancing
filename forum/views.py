from django.shortcuts import render, redirect
from django.db.models import Value, CharField, Count
from django.views import View
from .forms import PostForm
from .models import Question, Post, PostComment, QuestionComment
from django.shortcuts import render, get_object_or_404

# Create your views here.

class ForumHomeView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()

        # Fetch all posts and annotate content_type as 'Post'
        posts = Post.objects.annotate(content_type=Value('Post', output_field=CharField())).values('id', 'title', 'content', 'author', 'date_posted', 'image', 'content_type')
        # Fetch all questions and annotate content_type as 'Question'
        questions = Question.objects.annotate(content_type=Value('Question', output_field=CharField())).values('id', 'content', 'author', 'date_posted', 'image', 'content_type')
        # Combine the querysets and order by date_posted
        all_records = sorted(list(posts) + list(questions), key=lambda x: x['date_posted'], reverse=True)

        
        # Annotate posts with the count of comments
        annotated_posts = Post.objects.annotate(num_comments=Count('postcomment'))
        # Annotate questions with the count of comments
        annotated_questions = Question.objects.annotate(num_comments=Count('questioncomment'))
        # Combine annotated querysets for posts and questions
        combined_records = list(annotated_posts) + list(annotated_questions)
        # Sort the combined records by the count of comments in descending order
        sorted_records = sorted(combined_records, key=lambda x: x.num_comments, reverse=True)
        # Get the first 5 records
        trending_discussion = sorted_records[:5]

        context = {
            "form":form,
            "all_records":all_records,
            "trending_discussion":trending_discussion
        }
        return render(request, "forum/forum-home.html", context)
    

class createPostView(View):
    def post(self, request, *args, **kwargs):
        print("Post")
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Check if image field is provided
            if 'image' not in request.FILES:
                post.image = None  # Set image field to None if not provided

            post.save()

            return redirect('forum:forum_home_view')
        

class createQuestionView(View):
    def post(self, request, *args, **kwargs):
        question = request.POST.get("question")
        author=request.user
        Question.objects.create(author=author, content=question)
        return redirect('forum:forum_home_view')
        

class PostDetailView(View):
    def get(self, request, ID, *args, **kwargs):
        # Get the current question
        post = get_object_or_404(Post, id=ID)

        # Get the question before the current question
        previous_post = Post.objects.filter(id__lt=ID).order_by('-id').first()

        # Get the question after the current question
        next_post = Post.objects.filter(id__gt=ID).order_by('id').first()

        # Get comments for the current question
        post_comments = PostComment.objects.filter(post=post)

        # Count the total number of comments for the current question
        total_comments_count = post_comments.count()

        context = {
            "post": post,
            "previous_post": previous_post,
            "next_post": next_post,
            "post_comments": post_comments,
            "total_comments_count": total_comments_count
        }
        return render(request, "forum/post-detail.html", context)
    

class QuestionDetailView(View):
    def get(self, request, ID, *args, **kwargs):
        # Get the current question
        question = get_object_or_404(Question, id=ID)

        # Get the question before the current question
        previous_question = Question.objects.filter(id__lt=ID).order_by('-id').first()

        # Get the question after the current question
        next_question = Question.objects.filter(id__gt=ID).order_by('id').first()

        # Get comments for the current question
        question_comments = QuestionComment.objects.filter(question=question)

        # Count the total number of comments for the current question
        total_comments_count = question_comments.count()

        context = {
            "question": question,
            "previous_question": previous_question,
            "next_question": next_question,
            "question_comments": question_comments,
            "total_comments_count": total_comments_count
        }
        return render(request, "forum/question-detail.html", context)