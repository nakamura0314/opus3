from django.db.models import Q
# モデルに対して一件のオブジェクトを取得
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from .forms import CommentCreateForm
from .models import Post, Category, Comment


class IndexView(generic.ListView):
    model = Post
    paginate_by = 10

    # カスタマイズするために、上書きをする
    def get_queryset(self):
        # 'order_by'とすることで、並び替えを行う
        # 標準だと昇順で並び替えが行われる
        # しかし、 'order'の引数に-をつけると降順になる
        # querysetのなかに降順で記事を格納
        queryset = Post.objects.order_by('-created_at')
        # 下記は辞書のようなオブジェクトであり、
        # get('keyword')のkeywordはbase.htmlで指定したもの
        # 入力したものを格納
        keyword = self.request.GET.get('keyword')
        # keywordに格納したものがあった場合
        if keyword:
            # filterの引数にtitle=kewordとすることで、
            # keywordに入力したと完全に一致したものを返す
            # title__icontains=keywordとすることで、
            # 小文字大文字をせずにキーワードを含むかどうかで検索をかける
            # containsとすることで小文字大文字を区別させる
            # filterの引数を、Q() | Q()、とすることで、
            # or検索をすることができる
            # 下記の場合だと、タイトルと本文のどちらかで検索がヒットすれば表示することになる
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )
        return queryset


class CategoryView(generic.ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        """
        #models内のCategoryオブジェクトの指定したpkを一件取得する
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Post.objects.order_by(
            '-created_at').filter(category=category)
        """
        category_pk = self.kwargs['pk']
        # カテゴリーのプライマリーキーで直接検索をかけている
        queryset = Post.objects.order_by(
            '-created_at').filter(category__pk=category_pk)
        return queryset


class DetailView(generic.DetailView):
    model = Post


class CommentView(generic.CreateView):
    model = Comment
    # firlds=('text','name') このような書き方でもいいが、
    form_class = CommentCreateForm

    # これはformの入力内容に不備がなかったら呼び出される
    # コメントの紐付けをここで自動的に行なっている
    def form_valid(self, form):
        # URLに含まれているプライマリキーを取得
        post_pk = self.kwargs['post_pk']
        # commit=Falseとすることで、データを保存する一歩手前の状態を返してくれる
        # コメントはまだデータベースに保存されていない
        # このようにしないと、中身を編集することができない
        comment = form.save(commit=False)
        # だが、コメントモデルのインスタンスは作成されているので、自由に編集可能
        comment.post = get_object_or_404(Post, pk=post_pk)
        # ここでデータベースに保存している
        comment.save()
        # return redirectのように書くと、処理内容によって柔軟にリダイレクトができる
        return redirect('blog:detail', pk=post_pk)
