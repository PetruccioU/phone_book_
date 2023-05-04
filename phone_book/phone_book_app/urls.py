from django.contrib import admin
from django.urls import path, re_path, include
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    #path('home/', index, name='home'),
    # path('cats/', categories),
    path('', PhoneCardsView.as_view(), name='all_cards'),
    path('card/<slug:phone_card_slug>/', ShowPhoneCard.as_view(), name='card'),
    path('add_card/', AddPhoneCardForm.as_view(), name='add_card'),
    path('delete_card/<slug:phone_card_slug>/', delete_todo_view),
    re_path(r'^card/(?P<slug>[\w-]+)/update_form', CardUpdateView.as_view(), name='update'),
    path('category/<slug:cat_slug>/', ShowCatView.as_view(), name='category'),

    path('about/', AboutForm.as_view(), name='about'),
    path('search/', SearchResultsView.as_view(), name='search'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LogUser.as_view(), name='login'),
    path('logout_user/', LogUser.logout_user),

#     path('', TodoView.as_view(), name='home'),  # todoView.as_view() - call of function only
#     #path('', cache_page(60)(TodoView.as_view()), name='home')   #from django.views.decorators.cache import cache_page
#     path('donelist/', DoneList.as_view(), name='donelist'),
#     path('add/', AddForm.as_view(), name='add'),
#
#     path('motivation/', MotivationForm.as_view(), name='motivation'),
#     path('about/', AboutForm.as_view(), name='about'),
#
#     path('deleteTodoItem/<slug:post_slug>/', delete_todo_view),
#     path('YourTodoDone/<slug:post_slug>/', get_your_todo_done),
# #<int:i>
#     re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
#
#     path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
#     path('category/<slug:cat_slug>/', ShowCatView.as_view(), name='category'),
#
#     path('register/', RegisterUser.as_view(), name='register'),
#     path('login/', LogUser.as_view(), name='login'),
#     path('logout_user/', LogUser.logout_user),
#
#     path('feedback/', FeedbackView.as_view(), name='feedback'),
#
#     path('search/', SearchResultsView.as_view(), name='search'),
#
#     re_path(r'^post/(?P<slug>[\w-]+)/update_form', PostUpdateView.as_view(), name='update'),

]