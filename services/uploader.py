from django.utils.text import slugify


class Uploader:

    @staticmethod
    def upload_profile_photo(instance, filename):
        return f"users/{instance.user.fullname()}/{filename}"

    @staticmethod
    def upload_background_image(instance, filename):
        return f"profiles/background/{slugify(instance.user.fullname())}/{filename}"
