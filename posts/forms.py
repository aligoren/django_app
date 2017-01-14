from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "content_desc",
            "content",
            "meta_desc",
            "category",
            "keywords",
            "image",
        ]
        widgets = {
          'content_desc': forms.Textarea(attrs={'rows': 2, 'cols': 120, 'data-provide': 'markdown'}),
          'content': forms.Textarea(attrs={'rows': 20, 'cols': 120, 'data-provide': 'markdown'}),
          'title': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
          'slug': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
          'meta_desc': forms.Textarea(attrs={'rows': 2, 'cols': 55, 'placeholder': 'Max 150 Character for Google Meta'}),
          'category': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
          'keywords': forms.TextInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
        }
