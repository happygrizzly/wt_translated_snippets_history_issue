from django.utils.translation import gettext_lazy as _

from wagtail.admin.ui.tables import (
  UpdatedAtColumn,
  LiveStatusTagColumn,
)

from wagtail.snippets.views.snippets import (
  SnippetViewSet,
  SnippetViewSetGroup
)

from .models import Recipe


class RecipesViewSet(SnippetViewSet):
  model = Recipe
  list_display = ['title', 'slug', UpdatedAtColumn()]
  list_per_page = 10
  list_filter = ['title']
  menu_label = _('Recipes')
  menu_name = 'recipes_items'
  add_to_admin_menu = False


class RecipesViewSetGroup(SnippetViewSetGroup):
  items = (RecipesViewSet,)
  menu_label = _('Recipes')
  menu_name = 'recipes_root'

