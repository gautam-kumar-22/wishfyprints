from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from django.template.defaultfilters import slugify


class TimeStampedModel(models.Model):
    """TimeStampedModel.
    An abstract base class model that provides self-managed "created" and
    "updated" fields.
    """

    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        get_latest_by = 'modified_on'
        ordering = ('-modified_on', '-created_on',)
        abstract = True


class Menu(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    absolute_url = models.CharField(max_length=255, null=True, blank=True)
    has_submenu = models.BooleanField(default=False)
    rank = models.IntegerField(default=1)
    background_image = models.FileField(upload_to='Media/menu', blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Submenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    absolute_url = models.CharField(max_length=255, null=True, blank=True)
    background_image = models.FileField(upload_to='Media/menu', blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ValidPage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)


class Settings(models.Model):
    company_name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.FileField(upload_to='Media/logo', blank=True, null=True)
    office_time = models.CharField(max_length=200, null=True, blank=True)
    office_day = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    technology_title = models.CharField(max_length=200, null=True, blank=True)
    technology_description = models.TextField(null=True, blank=True)


class Contact(models.Model):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    info_email = models.CharField(max_length=50, null=True, blank=True)
    team_email = models.CharField(max_length=50, null=True, blank=True)
    career_email = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    pin_code = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)


class Slider(models.Model):
    page = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True, blank=True)
    sub_page = models.ForeignKey(Submenu, on_delete=models.CASCADE, null=True, blank=True)
    welcome_message = models.CharField(max_length=255, null=True, blank=True)
    heading = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    image = models.FileField(upload_to='Media/slider', blank=True, null=True)
    status = models.BooleanField(default=True)


class AboutUs(models.Model):
    heading = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    image = models.FileField(upload_to='Media/aboutus', blank=True, null=True, default='Media/default.jpg')
    project_done = models.IntegerField(default=0)
    satisfied_clients = models.IntegerField(default=0)
    awards_won = models.IntegerField(default=0)
    expert_team = models.IntegerField(default=0)
    status = models.BooleanField(default=True)


class Service(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    image = models.FileField(upload_to='Media/service', blank=True, null=True, default='Media/default.jpg')
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Service, self).save(*args, **kwargs)


class Features(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    icon = models.CharField(blank=True, null=True, max_length=255)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Features, self).save(*args, **kwargs)


class Industry(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    image = models.FileField(upload_to='Media/industry', blank=True, null=True, default='Media/default.jpg')
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Industry, self).save(*args, **kwargs)


class Category(models.Model):
    type = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    discount = models.FloatField(null=True, blank=True, default=0.0)
    available_quantity = models.IntegerField(default=5)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.type)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.type


class Project(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    sub_title = models.CharField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    image = models.FileField(upload_to='Media/project', blank=True, null=True, default='Media/default.jpg')
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True, default=None)
    tag = models.CharField(max_length=255, null=True, blank=True)
    about = RichTextUploadingField(blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Photo(models.Model):
    def generate_path(instance, file_name):
        return f"Media/product/{instance.Product.id}/{file_name}"

    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to=generate_path, default='Media/default.jpg')

    # resizing the image, you can change parameters like size and quality.
    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 1125 or img.width > 1125:
            img.thumbnail((500, 500))
        img.save(self.photo.path, quality=100, optimize=True)


class AdditionalInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_information', null=True,
                                blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)


class Technology(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    image = models.FileField(upload_to='Media/technology', blank=True, null=True, default='Media/default.jpg')
    status = models.BooleanField(default=True)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(upload_to='Media/blog', default='Media/default.jpg')
    tags = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    CUSTOMER_TYPE = (
        ('customer', 'Customer'),
        ('seller', 'Seller')
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=20, choices=CUSTOMER_TYPE, default='customer')
    testimonial = RichTextUploadingField(blank=True, null=True)
    image = models.FileField(upload_to='Media/testimonial', blank=True, null=True, default='Media/default.jpg')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Faq(models.Model):
    question = models.CharField(max_length=255, null=True, blank=True)
    answer = RichTextUploadingField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.question


class ContactUs(TimeStampedModel):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.CharField(max_length=200, null=False, blank=False)
    subject = models.CharField(max_length=200, null=False, blank=False)
    message = models.TextField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.subject
