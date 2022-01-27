from django.db import models
from django.utils import timezone


class Category(models.Model):
    """"カテゴリ"""

    name = models.CharField('カテゴリ名', max_length=255)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.name


class Post(models.Model):
    """モデルの記事"""

    title = models.CharField('タイトル', max_length=255)
    text = models.TextField('本文')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    # カテゴリを削除しようとしたときに、中身があればそれをできないようにする
    category = models.ForeignKey(
        Category, verbose_name='カテゴリ', on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """"ブログのコメント"""

    name = models.CharField('お名前', max_length=30, default='名無し')
    text = models.TextField('本文')
    # この場合だと、コメントを記事と紐づかせて、
    # コメントを全て削除しないと、その記事も削除されない
    post = models.ForeignKey(Post, verbose_name='紐づく記事',
                             on_delete=models.PROTECT)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:10]
