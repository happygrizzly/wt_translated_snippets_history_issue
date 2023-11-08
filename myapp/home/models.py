from unidecode import unidecode

from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models, transaction, router, IntegrityError

from wagtail.models import (
    Page,
    TranslatableMixin,
    PreviewableMixin,
    RevisionMixin,
    DraftStateMixin,
    WorkflowMixin,
)

from wagtail.fields import RichTextField
from wagtail.admin.panels import TabbedInterface, ObjectList, FieldPanel


class HomePage(Page):
    pass


class Recipe(
    WorkflowMixin,
    PreviewableMixin,
    DraftStateMixin,
    RevisionMixin,
    TranslatableMixin
):
    workflow_states = GenericRelation(
        'wagtailcore.WorkflowState',
        content_type_field='base_content_type',
        object_id_field='object_id',
        related_query_name='recipes',
        for_concrete_model=False,
    )

    _revisions = GenericRelation(
        to='wagtailcore.Revision',
        related_query_name='recipes'
    )

    slug = models.SlugField(null=True, blank=True, max_length=100, allow_unicode=False)

    title = models.TextField()

    body = RichTextField()

    primary_content_panels = [
        FieldPanel('slug'),
        FieldPanel('title'),
        FieldPanel('body'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(primary_content_panels, heading=_('Primary content')),
    ])

    class Meta:
        ordering = ['-last_published_at']
        unique_together = (('translation_key', 'locale'), ('locale', 'slug'))

    @property
    def revisions(self):
        return self._revisions

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(unidecode(self.title))

            using = kwargs.get('using') or \
                router.db_for_write(type(self), instance=self)

            kwargs['using'] = using

            try:
                with transaction.atomic(using=using):
                    save_result = super().save(*args, **kwargs)
                    return save_result
            except IntegrityError:
                pass

            slugs = set(
                type(self)
                ._default_manager.filter(slug__startswith=self.slug)
                .values_list('slug', flat=True)
            )

            i = 1
            while True:
                slug = slugify(unidecode(self.title)) + '_%d' % i
                if slug not in slugs:
                    self.slug = slug
                    # We purposely ignore concurrency issues here for now.
                    # (That is, till we found a nice solution...)
                    return super().save(*args, **kwargs)
                i += 1

        else:
            return super().save(*args, **kwargs)

    def get_preview_template(self, request, mode_name):
        return 'home/previews/recipe.html'

    def __str__(self):
        return self.title

