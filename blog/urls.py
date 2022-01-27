from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # プライマリーキーをURLに入れて、その一覧を表示、名前はcategory
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    # int:pkだけでも可能、しかしわかりやすくする方がいいだろう
    # ここではpostのpkということを表してる
    # class baseviewを使う場合は.as_view()を使う
    path('comment/<int:post_pk>', views.CommentView.as_view(), name='comment'),
]
