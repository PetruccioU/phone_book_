from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from .utils import *
from django.views.generic.edit import UpdateView


# Create your views here.

# Exeption 404,
def pageNotFound(request,exception):
    return HttpResponseNotFound('<h1> Извините, страница не найдена. </h1>')


# Главная страница со всеми абонентами.
class PhoneCardsView(DataMixinPhoneCard, ListView):
    model = PhoneCard
    template_name = 'all_phone_cards.html'
    context_object_name = 'cards'   # Имя переменной, которую мы используем в шаблоне a_phone_card.html

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Все абоненты')
        context['cat_selected'] = 0
        return {**context, **c_def}

    def get_queryset(self):
        return PhoneCard.objects.filter(is_published=1,).select_related('cat')


# Показать абонента детально.
class ShowPhoneCard(DataMixinPhoneCard, DetailView):
    model = PhoneCard
    template_name = 'a_phone_card.html'  # Имя шаблона.
    slug_url_kwarg = 'phone_card_slug'
    context_object_name = 'card' # Имя переменной, которую мы используем в шаблоне a_phone_card.html

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return {**context, **c_def}


# Добавление нового абонента.
class AddPhoneCardForm(LoginRequiredMixin, DataMixinPhoneCard, CreateView):
    form_class = AddPersonCardForm
    template_name = 'add_phone_card.html'
    success_url = reverse_lazy('all_cards')
    login_url = reverse_lazy('all_cards')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Добавить новое физическое лицо')
        return {**context, **c_def}


# Редактирование данных абонента:
class CardUpdateView(LoginRequiredMixin, DataMixinPhoneCard, UpdateView):
    model = PhoneCard
    form_class = AddPersonCardForm
    success_message = "Информация абонента успешно обновлена"
    template_name = 'update_form.html'
    template_name_suffix = 'update_form'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return PhoneCard.objects.filter(slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        catid = PhoneCard.objects.get(slug=self.kwargs['slug'])
        context['post'] = catid
        c_def=self.get_user_context(title='Обновить информацию об абоненте')
        return {**context, **c_def}


# Удаление абонента:
def delete_todo_view(request, phone_card_slug):
    if request.user.is_authenticated: # Если пользователь
        y = PhoneCard.objects.get(slug=phone_card_slug) # Найдем запись по слагу.
        y.delete()  # Удалим запись.
        return redirect('all_cards',permanent = True)
    else:
        return redirect('all_cards', permanent=True)


# Типы регистрации(Категории).
class ShowCatView(DataMixinPhoneCard, ListView):
    model = PhoneCard
    template_name = 'all_phone_cards.html'
    context_object_name = 'cards'
    allow_empty = False

    def get_queryset(self):
        return PhoneCard.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        catid = Category.objects.get(slug=self.kwargs['cat_slug'])
        context['cat_selected'] = catid.id
        context['cat_selected_name'] = catid.name
        c_def = self.get_user_context(title='Category - ' + str(catid.name))    #(title='Category - ' + str(catid.cat), cat_selected = catid.pk)
        return {**context, **c_def}


# Поиск:
class SearchResultsView(DataMixinPhoneCard, ListView):
    model = PhoneCard
    template_name = 'search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Поиск')
        return {**context, **c_def}

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        object_list = PhoneCard.objects.filter( # Перечислим поля для поиска.
            Q(name__icontains=query) | Q(phone_number__icontains=query) | Q(address__icontains=query)
        )
        return object_list


# О нас:
class AboutForm(DataMixinPhoneCard, ListView):
    template_name = 'about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='О нас')
        return {**context, **c_def}

    def get_queryset(self):
        return PhoneCard.objects.all()


# Регистрация, вход и выход.
class RegisterUser(DataMixinPhoneCard, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Registration')
        return {**context, **c_def}

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('all_cards')


class LogUser(DataMixinPhoneCard, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Login')
        return {**context, **c_def}

    def get_success_url(self):
            return reverse_lazy('all_cards')

    def logout_user(request):
        logout(request)
        return redirect('login')





# class CompanyView(DataMixinCompany, ListView):
#     model = Person
#     template_name = 'companies.html'
#     context_object_name = 'cards'   # Имя переменной, которую мы используем в шаблоне a_phone_card.html
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Физические лица')
#         context['cat_selected'] = 0
#         return {**context, **c_def}
#
#     def get_queryset(self):
#         return Person.objects.filter(is_published=1,).select_related('cat')
#
#
# class ShowCompanyCard(DataMixinCompany, DetailView):
#     model = Person
#     template_name = 'company_card.html'  # Имя шаблона.
#     slug_url_kwarg = 'company_card_slug'
#     context_object_name = 'company_card' # Имя переменной, которую мы используем в шаблоне a_phone_card.html
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context()
#         return {**context, **c_def}
#
#
# class AddCompanyForm(LoginRequiredMixin, DataMixinCompany, CreateView):
#     form_class = AddPersonCardForm
#     template_name = 'add_company.html'
#     success_url = reverse_lazy('companies')
#     login_url = reverse_lazy('companies')
#     raise_exception = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def=self.get_user_context(title='Добавить новое юридическое лицо')
#         return {**context, **c_def}