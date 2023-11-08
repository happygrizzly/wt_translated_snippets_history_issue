from django.http import HttpRequest

from wagtail import hooks
from wagtail.snippets.wagtail_hooks import SnippetsMenuItem
from wagtail.snippets.models import register_snippet

from .views import RecipesViewSetGroup


@hooks.register('construct_main_menu')
def hide_snippets_menu(request: HttpRequest, menu_items):
  menu_items[:] = [item for item in menu_items if not isinstance(item, SnippetsMenuItem)]


register_snippet(RecipesViewSetGroup)

