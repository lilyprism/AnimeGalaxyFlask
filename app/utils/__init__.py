import os

from PIL import Image, ImageOps
from flask_admin.form import FileUploadField, ImageUploadInput
from werkzeug.utils import secure_filename
from wtforms import ValidationError


class S3ImageUploadField(FileUploadField):
	"""
		Image upload field.
		Does image validation, thumbnail generation, updating and deleting images.
		Requires PIL (or Pillow) to be installed.
	"""
	widget = ImageUploadInput()

	keep_image_formats = ('PNG',)
	"""
		If field detects that uploaded image is not in this list, it will save image
		as PNG.
	"""

	def __init__(self, label=None, validators=None,
	             base_path=None, relative_path=None,
	             namegen=None, allowed_extensions=None,
	             max_size=None,
	             thumbgen=None, thumbnail_size=None,
	             permission=0o666,
	             url_relative_path=None, endpoint='static',
	             **kwargs):

		# Check if PIL is installed
		if Image is None:
			raise ImportError('PIL library was not found')

		self.max_size = max_size
		self.thumbnail_fn = thumbgen or thumbgen_filename
		self.thumbnail_size = thumbnail_size
		self.endpoint = endpoint
		self.image = None
		self.url_relative_path = url_relative_path

		if not allowed_extensions:
			allowed_extensions = ('gif', 'jpg', 'jpeg', 'png', 'tiff')

		super(S3ImageUploadField, self).__init__(label, validators,
		                                       base_path=base_path,
		                                       relative_path=relative_path,
		                                       namegen=namegen,
		                                       allowed_extensions=allowed_extensions,
		                                       permission=permission,
		                                       **kwargs)

	def pre_validate(self, form):
		super(S3ImageUploadField, self).pre_validate(form)

		if self._is_uploaded_file(self.data):
			try:
				self.image = Image.open(self.data)
			except Exception as e:
				raise ValidationError('Invalid image: %s' % e)

	# Deletion
	def _delete_file(self, filename):
		super(S3ImageUploadField, self)._delete_file(filename)

		self._delete_thumbnail(filename)

	def _delete_thumbnail(self, filename):
		path = self._get_path(self.thumbnail_fn(filename))

		if os.path.exists(path):
			os.remove(path)

	# Saving
	def _save_file(self, data, filename):
		path = self._get_path(filename)

		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path), self.permission | 0o111)

		# Figure out format
		filename, format = self._get_save_format(filename, self.image)

		if self.image and (self.image.format != format or self.max_size):
			if self.max_size:
				image = self._resize(self.image, self.max_size)
			else:
				image = self.image

			self._save_image(image, self._get_path(filename), format)
		else:
			data.seek(0)
			data.save(self._get_path(filename))

		self._save_thumbnail(data, filename, format)

		return filename

	def _save_thumbnail(self, data, filename, format):
		if self.image and self.thumbnail_size:
			path = self._get_path(self.thumbnail_fn(filename))

			self._save_image(self._resize(self.image, self.thumbnail_size),
			                 path,
			                 format)

	def _resize(self, image, size):
		(width, height, force) = size

		if image.size[0] != width or image.size[1] != height:
			if force:
				return ImageOps.fit(self.image, (width, height), Image.ANTIALIAS)
			else:
				thumb = self.image.copy()
				thumb.thumbnail((width, height), Image.ANTIALIAS)
				return thumb

		return image

	def _save_image(self, image, path, format='JPEG'):
		if image.mode not in ('RGB', 'RGBA'):
			image = image.convert('RGBA')

		with open(path, 'wb') as fp:
			image.save(fp, format)

	def _get_save_format(self, filename, image):
		if image.format not in self.keep_image_formats:
			name, ext = os.path.splitext(filename)
			filename = '%s.jpg' % name
			return filename, 'JPEG'

		return filename, image.format


# Helpers
def namegen_filename(obj, file_data):
	"""
		Generate secure filename for uploaded file.
	"""
	return secure_filename(file_data.filename)


def thumbgen_filename(filename):
	"""
		Generate thumbnail name from filename.
	"""
	name, ext = os.path.splitext(filename)
	return '%s_thumb%s' % (name, ext)
