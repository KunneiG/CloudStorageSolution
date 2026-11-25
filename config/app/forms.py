from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserFile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file', 'title', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название (необязательно)'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.size > 100 * 1024 * 1024:
            raise forms.ValidationError("Файл слишком большой (максимум 100 МБ).")
        allowed = (
            '.jpg', '.jpeg', '.png', '.gif', '.webp',
            '.mp4', '.avi', '.mov', '.mkv', '.webm',
            '.pdf', '.doc', '.docx', '.txt', '.xlsx',
        )
        name = file.name.lower()
        if not name.endswith(allowed):
            raise forms.ValidationError("Недопустимый тип файла.")
        return file