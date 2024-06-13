from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:list', args=[self.id, self.slug])
    
    def save(self, *args, **kwargs):
        if self.get_current_language() == 'en':
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    translations = TranslatedFields(
        name=models.CharField(_('name'), max_length=200, db_index=True, unique=True),
    )

    slug = models.SlugField(_('slug'), max_length=200, db_index=True, blank=True)


class Product(TranslatableModel):
    class Meta:
        index_together = [('id', 'slug')]
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:detail', args=[self.id, self.slug])

    def get_first_image(self):
        return self.images.first().get_url()
    
    def save(self, *args, **kwargs):
        from core.redis import Redis
        if self.get_current_language() == 'en':
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        Redis.update_product(self)

    translations = TranslatedFields(
        name=models.CharField(_('name'), max_length=200, db_index=True),
        description=models.TextField(_('description'), blank=True)
    )

    category = models.ForeignKey('Category', verbose_name=_('category'), related_name='products', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(_('slug'), max_length=200, db_index=True, blank=True)
    price = models.PositiveIntegerField(_('price'))
    quantity = models.PositiveIntegerField(_('quantity'))
    available = models.BooleanField(_('available'))
    created = models.DateField(_('created'), auto_now_add=True)
    updated = models.DateField(_('updated'), auto_now=True)


class Image(models.Model):
    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return f'image from {self.product}'

    def get_url(self):
        return self.image.url

    product = models.ForeignKey('Product', verbose_name=_('product'), related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to='products/%Y/%m/%d')
