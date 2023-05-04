# ========================================================
# import:
from django.db.models import Count
from .models import *
from django.core.cache import cache


# ========================================================
# menu:

menu = [{'title': "Все абоненты", 'url_name': 'all_cards'},
        {'title': "Добавить абонента", 'url_name': 'add_card'},
        {'title': "О нас", 'url_name': 'about'}
]

# ===========================================================


class DataMixinPhoneCard:
    paginate_by = 3
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('phonecard'))
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
            context['auth'] = False
        else:
            context['auth'] = True
        context['menu'] = user_menu
        context['cats'] = cats
        return context


# class DataMixinCompany:
#     paginate_by = 3
#     def get_user_context(self, **kwargs):
#         context = kwargs
#         cats = Category.objects.annotate(Count('company'))
#         user_menu = menu.copy()
#         if not self.request.user.is_authenticated:
#             user_menu.pop(2)
#             context['auth'] = False
#         else:
#             context['auth'] = True
#         context['menu'] = user_menu
#         context['cats'] = cats
#         return context