from django import forms

from .models import Post


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'subtitle', 'body')

class UpdatePostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'subtitle', 'body')

    def save(self, commit=True):
        if self.is_valid():
            post = self.instance
            post.title = self.cleaned_data['title']
            post.subtitle = self.cleaned_data['subtitle']
            post.body = self.cleaned_data['body']

            
            if commit:
                post.save()
            
            return post