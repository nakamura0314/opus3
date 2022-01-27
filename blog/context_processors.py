from .models import Category


def common(request):
    """テンプレートに毎回渡すデータ"""
    context = {
        'category_list': Category.objects.all(),
    }
    return context
    # 最後にsettings.pyのTEMPLATESのOPTIONSに書き込み、
    # プロジェクトにcommon関数を使うことを教える
