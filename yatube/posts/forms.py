from django.forms import ModelForm

from posts.models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        context = {
            'group': 'Группа',
            'text': 'Текст',
        }

        fields = ('text', 'group')