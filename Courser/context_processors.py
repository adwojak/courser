from .models import Category


def categories_items(context):
    categories = Category.objects.all()
    return {'menu_categories': categories}
