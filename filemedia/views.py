from PIL import Image as PilImage
from django.conf import settings
from django.utils.translation import ugettext as _
from django.http import JsonResponse, Http404
from django.views.generic import FormView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_str
from .forms import ImageForm
from wysiwyg.utils import import_class, is_module_image_installed
from .models import Media

# deal with python3 basestring
try:
    unicode = unicode
except NameError:
    basestring = (str, bytes)
else:
    basestring = basestring


class LoadImageView():
    pass


class UploadView(FormView):
    form_class = ImageForm
    http_method_names = ('post',)
    upload_to = getattr(settings, 'REDACTOR_UPLOAD', 'redactor/')
    upload_handler = getattr(settings, 'REDACTOR_UPLOAD_HANDLER', 'wysiwyg.handlers.UUIDUploader')
    auth_decorator = getattr(settings, 'REDACTOR_AUTH_DECORATOR',
                             staff_member_required)
    tax_id = int
    if isinstance(auth_decorator, basestring):
        # Given decorator is string, probably because user can't import eg.
        # django.contrib.auth.decorators.login_required in settings level.
        # We are expected to import it on our own.
        auth_decorator = import_class(auth_decorator)

    @method_decorator(csrf_exempt)
    @method_decorator(auth_decorator)
    def dispatch(self, request, *args, **kwargs):
        try:
            self.tax_id = request.POST['tax']
        except:
            self.tax_id = None
        if request.method == 'POST' and request.is_ajax():
            if not is_module_image_installed():
                data = {
                    'error': _(
                            "ImproperlyConfigured: Neither Pillow nor PIL could be imported: No module named 'Image'"),
                }
                return JsonResponse(data)

            return super(UploadView, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404('Page not found')

    def form_invalid(self, form):
        # TODO: Needs better error messages
        try:
            error = form.errors.values()[-1][-1]
        except:
            error = _('Invalid file.')
        data = {
            'error': error,
        }
        return JsonResponse(data)

    def form_valid(self, form):
        file_ = form.cleaned_data['file']
        handler_class = import_class(self.upload_handler)
        uploader = handler_class(file_, upload_to=self.kwargs.get('upload_to', None))
        uploader.save_file()
        file_name = force_str(uploader.get_filename())
        file_url = force_str(uploader.get_url())

        """
        inser image to database
        """
        img = Media()
        img.name = uploader.upload_file.name
        img.file = 'image/' + file_name
        img.unique_name = file_name
        img.type = 'i'
        img.save()
        if (self.tax_id):
            img.relationships.add(self.tax_id)

        src = settings.MEDIA_ROOT + 'image/' + file_name
        dst1024 = settings.MEDIA_ROOT + 'image/' + file_name
        dst512 = settings.MEDIA_ROOT + 'image/thumbnail/512x288/' + file_name
        dst256 = settings.MEDIA_ROOT + 'image/thumbnail/256x144/' + file_name
        dst128 = settings.MEDIA_ROOT + 'image/thumbnail/128x72/' + file_name
        dst144 = settings.MEDIA_ROOT + 'image/thumbnail/144x144/' + file_name
        dst100 = settings.MEDIA_ROOT + 'image/thumbnail/100x100/' + file_name
        dst848 = settings.MEDIA_ROOT + 'image/thumbnail/848x309/' + file_name

        self.resize_image(src, dst1024, 1024)
        self.resize_image(src, dst512, 512, 288)
        self.resize_image(src, dst848, 848)
        self.resize_image(src, dst256, 256)
        self.resize_image(src, dst128, 128)
        self.crop_image(dst256, dst144, 144, 144)
        self.resize_image(dst144, dst100, 100)

        data = {
            'imgid': img.id,
            'description': img.description,
            'filelink': file_url,
            'filename': uploader.upload_file.name,
            'uniquename': file_name,
        }
        return JsonResponse(data)

    def crop_image(self, src, dst, width, hight):
        img = PilImage.open(src)
        w = width / 2
        h = hight / 2
        half_the_width = img.size[0] / 2
        half_the_height = img.size[1] / 2
        newimg = img.crop(
                (
                    half_the_width - w,
                    half_the_height - h,
                    half_the_width + w,
                    half_the_height + h
                )
        )
        return newimg.save(dst)

    def resize_image(self, src, dst, width):
        size = (width, width)
        img = PilImage.open(src)
        img.thumbnail(size, PilImage.ANTIALIAS)
        return img.save(dst)
