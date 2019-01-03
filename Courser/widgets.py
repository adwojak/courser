from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):

        def is_initial(self, value):
            pass
