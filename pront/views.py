from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from word.models import Word
from appearance.models import Menu, Widget
from .forms import ContactForm, SearchForm
from django.views.generic.edit import CreateView
from contact.models import Contact
from django.core.urlresolvers import reverse_lazy
from django.template.response import TemplateResponse
import re
from django.db.models import Q

class HomePageView(TemplateView):
    template_name = "pront/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context


class AddMessageView(CreateView):
    model = Contact
    success_url = reverse_lazy('add_message')
    fields = ['name', 'email', 'subject', 'message']
    template_name = 'pront/post_list_bay_tax.html'

    def get_context_data(self, **kwargs):
        context = super(AddMessageView, self).get_context_data(**kwargs)
        context['widgets_sidebar'] = Widget.objects.filter(type='sidebar').order_by('position')
        context['widgets_footer1'] = Widget.objects.filter(type='footer1').order_by('position')
        context['widgets_footer2'] = Widget.objects.filter(type='footer2').order_by('position')
        context['widgets_footer3'] = Widget.objects.filter(type='footer3').order_by('position')
        context['widgets_footer4'] = Widget.objects.filter(type='footer4').order_by('position')
        context['contact_form'] = ContactForm
        context['post'] = 'page'
        context['cform'] = 'contact'
        return context

    def form_valid(self, form):
        context = {
            'widgets_sidebar': Widget.objects.filter(type='sidebar').order_by('position'),
            'widgets_footer1': Widget.objects.filter(type='footer1').order_by('position'),
            'widgets_footer2': Widget.objects.filter(type='footer2').order_by('position'),
            'widgets_footer3': Widget.objects.filter(type='footer3').order_by('position'),
            'widgets_footer4': Widget.objects.filter(type='footer4').order_by('position'),
            'post': 'page',
            'cform': 'contact',
            'contact_form': ContactForm,
            'status': True
        }
        if super(AddMessageView, self).form_valid(form):
            return TemplateResponse(self.request, self.template_name, context)

    def form_invalid(self, form):
        form = ContactForm(self.request.POST)
        context = {
            'widgets_sidebar': Widget.objects.filter(type='sidebar').order_by('position'),
            'widgets_footer1': Widget.objects.filter(type='footer1').order_by('position'),
            'widgets_footer2': Widget.objects.filter(type='footer2').order_by('position'),
            'widgets_footer3': Widget.objects.filter(type='footer3').order_by('position'),
            'widgets_footer4': Widget.objects.filter(type='footer4').order_by('position'),
            'post': 'page',
            'cform': 'contact',
            'contact_form': form
        }

        return TemplateResponse(self.request, self.template_name, context)


class PostDetailView(DetailView):
    model = Word
    template_name = 'pront/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['widgets_sidebar'] = Widget.objects.filter(type='sidebar').order_by('position')
        context['widgets_footer1'] = Widget.objects.filter(type='footer1').order_by('position')
        context['widgets_footer2'] = Widget.objects.filter(type='footer2').order_by('position')
        context['widgets_footer3'] = Widget.objects.filter(type='footer3').order_by('position')
        context['widgets_footer4'] = Widget.objects.filter(type='footer4').order_by('position')
        slug = self.kwargs.get('tax', None)
        try:
            Menu.objects.get(slug=slug, type='category')
        except Menu.DoesNotExist:
            try:
                Menu.objects.get(slug=slug, type='tag')
            except Menu.DoesNotExist:
                raise Http404(_('Page not found'))
            else:
                menu = Menu.objects.get(slug=slug, type='tag')
                context['name'] = menu.name
                return context
        else:
            menu = Menu.objects.get(slug=slug, type='category')
            context['name'] = menu.name
            return context


class PostSearchView(ListView):
    model = Word

    template_name = 'pront/post_search_list.html'
    paginate_by = 10
    context_object_name = "data"

    def get_context_data(self, **kwargs):
        context = super(PostSearchView, self).get_context_data(**kwargs)
        context['widgets_sidebar'] = Widget.objects.filter(type='sidebar').order_by('position')
        context['widgets_footer1'] = Widget.objects.filter(type='footer1').order_by('position')
        context['widgets_footer2'] = Widget.objects.filter(type='footer2').order_by('position')
        context['widgets_footer3'] = Widget.objects.filter(type='footer3').order_by('position')
        context['widgets_footer4'] = Widget.objects.filter(type='footer4').order_by('position')
        context['post'] = 'post'
        context['slug'] = 'post'
        context['q'] = self.request.GET.get('q', '')
        return context

    def normalize_query(self, query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

    def get_query(self, query_string, search_fields):

        query = None  # Query to search for every search term
        terms = self.normalize_query(query_string)

        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    def get_queryset(self):

        try:
            q = self.request.GET['q']
            search_fields = ['title', 'content', 'status']
            str = self.get_query(q, search_fields)
            query = Word.objects.filter(str).order_by('-created_at')
        except:
            query = super(PostSearchView, self).get_queryset()
        return query


class TaxView(ListView):
    model = Word
    template_name = 'pront/post_list_bay_tax.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TaxView, self).get_context_data(**kwargs)
        context['widgets_sidebar'] = Widget.objects.filter(type='sidebar').order_by('position')
        context['widgets_footer1'] = Widget.objects.filter(type='footer1').order_by('position')
        context['widgets_footer2'] = Widget.objects.filter(type='footer2').order_by('position')
        context['widgets_footer3'] = Widget.objects.filter(type='footer3').order_by('position')
        context['widgets_footer4'] = Widget.objects.filter(type='footer4').order_by('position')
        context['contact_form'] = ContactForm
        slug = self.kwargs.get('tax', None)
        perpage = self.paginate_by
        try:
            Menu.objects.filter(slug=slug, type='category')[:1].get()
        except Menu.DoesNotExist:
            try:
                Menu.objects.filter(slug=slug, type='tag')[:1].get()
            except Menu.DoesNotExist:
                try:
                    Menu.objects.filter(slug=slug, type='category')[:1].get()
                except Menu.DoesNotExist:
                    try:
                        Menu.objects.filter(slug=slug, type='menu_page')[:1].get()
                    except Menu.DoesNotExist:
                        raise Http404(_('Page not found'))
                    else:
                        menu = Menu.objects.filter(slug=slug, type='menu_page')[:1].get()
                        context['data'] = Word.objects.filter(relationships=menu.id, type='page')
                        context['slug'] = slug
                        context['name'] = menu.name
                        context['description'] = menu.description
                        context['post'] = 'page'
                        return context
            else:
                menu = Menu.objects.filter(slug=slug, type='tag')[:1].get()
                posts_list = Word.objects.filter(relationships=menu.id, type='post')
                paginator = Paginator(posts_list, perpage)
                try:
                    page = self.request.GET['page']
                except MultiValueDictKeyError:
                    page = 1

                try:
                    posts = paginator.page(page)
                except PageNotAnInteger:
                    posts = paginator.page(1)
                except EmptyPage:
                    posts = paginator.page(paginator.num_pages)

                context['data'] = posts
                context['slug'] = slug
                context['name'] = menu.name
                context['description'] = menu.description
                context['perpage'] = perpage
                context['pagecount'] = paginator.count
                context['post'] = 'post'
                return context
        else:
            menu = Menu.objects.filter(slug=slug, type='category')[:1].get()
            posts_list = Word.objects.filter(relationships=menu.id, type='post')
            paginator = Paginator(posts_list, perpage)
            try:
                page = self.request.GET['page']
            except MultiValueDictKeyError:
                page = 1

            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            context['data'] = posts
            context['slug'] = slug
            context['name'] = menu.name
            context['description'] = menu.description
            context['perpage'] = perpage
            context['pagecount'] = paginator.count
            context['post'] = 'post'
            return context
