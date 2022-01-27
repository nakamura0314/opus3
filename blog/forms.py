from django import forms
from .models import Comment


# ModelFormとすることで、Commentモデルを元に入力欄を自動生成
# そしてコメントを保存するときもform.saveのようにすると簡単
class CommentCreateForm(forms.ModelForm):

    # 初期化処理
    def __init__(self, *args, **kwargs):
        # nameとtextにform-controlの機能を渡している
        # form-controlとは、Bootstrap4に対応するためのカスタマイズ
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        # model.formが作られた際に、入力欄に名前と本文だけ表示される
        fields = ('name', 'text')
