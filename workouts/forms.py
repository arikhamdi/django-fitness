from django import forms
from django.forms import ModelForm

from .models import Workout, Member, Comments_coach


class DateInput(forms.DateInput):
    input_type = 'date'


class WorkoutForm(ModelForm):
    def __init__(self, user, *arg, **kwargs):
        super(WorkoutForm, self).__init__(*arg, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(
            user_id=user)

    class Meta:
        model = Workout
        fields = '__all__'
        widget = {'date_of_training': DateInput()}


class MemberForm(ModelForm):

    class Meta:
        model = Member
        fields = ['profile_pic']


class Comments_coachForm(forms.ModelForm):
    content = forms.CharField(label='Message', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'usercomment',
        'rows': '10',
        'cols': '3',
    }))

    class Meta:
        model = Comments_coach
        fields = ['content', ]
