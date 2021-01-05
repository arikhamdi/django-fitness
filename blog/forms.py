from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Message', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'usercomment',
        'rows': '10',
        'cols': '3',
    }))

    class Meta:
        model = Comment
        fields = ['content', ]
