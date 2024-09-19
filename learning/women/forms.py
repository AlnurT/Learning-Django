from django import forms
from django.core.exceptions import ValidationError

from women.models import Category, Husband, Women


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="Категория не выбрана"
    )
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        required=False, label="Муж",
        empty_label="Не замужем"
    )

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published',
                  'cat', 'husband', 'tags']
        labels = {'slug': "URL"}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")
