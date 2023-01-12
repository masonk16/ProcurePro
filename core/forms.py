from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model

User = get_user_model()


class NewUserForm(UserCreationForm):

    CATEGORY_CHOICES = (
        ('Advertising', 'Advertising'),
        ('Agriculture', 'Agriculture'),
        ('Chemicals', 'Chemicals'),
        ('Construction', 'Construction'),
        ('Economics', 'Economics'),
        ('Education', 'Education'),
        ('Energy', 'Energy'),
        ('Engineering', 'Engineering'),
        ('Finance', 'Finance'),
        ('Food', 'Food'),
        ('Forestry', 'Forestry'),
        ('Goods', 'Goods'),
        ('Healthcare', 'Healthcare'),
        ('Infrastructure', 'Infrastructure'),
        ('Manufacturing', 'Manufacturing'),
        ('Market Research', 'Market Research'),
        ('Mining', 'Mining'),
        ('Pharmaceuticals', 'Pharmaceuticals'),
        ('Production', 'Production'),
        ('Real Estate', 'Real Estate'),
        ('Research', 'Research'),
        ('Retail', 'Retail'),
        ('Telecommunications', 'Telecommunications'),
    )
    email = forms.EmailField(required=True)
    company_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    industry = forms.ChoiceField(choices=CATEGORY_CHOICES)
    phone_number = forms.CharField(required=True)
    website = forms.URLField()
    user_type = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ("email", 'company_name', 'address', 'industry', 'phone_number',
                  'website', 'user_type', "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
