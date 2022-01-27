from django import template

# タグやフィルターを登録すための初期化処理をする
# フィルターも同様に作成できる
register = template.Library()


# デコレーター
@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータを一部置き換える"""
    url_dict = request.GET.copy()
    url_dict[field] = value
    return url_dict.urlencode()
