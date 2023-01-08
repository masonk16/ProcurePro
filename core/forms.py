from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model

User = get_user_model()

class NewUserForm(UserCreationForm):
    MANUFACTURING = 'MANU'
    PRODUCTION = 'PRO'
    AGRICULTURE = 'AGR'
    CONSTRUCTION = 'CON'
    RETAIL = 'RT'
    MINING = 'MIN'
    MARKET_RESEARCH = 'MR'
    FINANCE = 'FIN'
    ECONOMICS = 'ECOS'
    EDUCATION = 'EDU'
    CHEMICALS = 'CHEM'
    ADVERTISING = 'ADS'
    GOODS = 'GD'
    REAL_ESTATE = 'RE'
    HEALTHCARE = 'HC'
    FOOD = 'FD'
    RESEARCH = 'RES'
    FORESTRY = 'FOR'
    ENERGY = 'ENE'
    ENGINEERING = 'ENG'
    TELECOMMUNICATIONS = 'TELE'
    INFRASTRUCTURE = 'INFRA'
    PHARMACEUTICAL = 'PHARMA'

    CATEGORY_CHOICES = [
        (MANUFACTURING, 'Manufacturing'),
        (PRODUCTION, 'Production'),
        (AGRICULTURE, 'Agriculture'),
        (CONSTRUCTION, 'Construction'),
        (RETAIL, 'Retail'),
        (MINING, 'Mining'),
        (MARKET_RESEARCH, 'Market Research'),
        (FINANCE, 'Finance'),
        (ECONOMICS, 'Economics'),
        (EDUCATION, 'Education'),
        (CHEMICALS, 'Chemicals'),
        (ADVERTISING, 'Advertising'),
        (GOODS, 'Goods'),
        (REAL_ESTATE, 'Real Estate'),
        (HEALTHCARE, 'Healthcare'),
        (FOOD, 'Food'),
        (RESEARCH, 'Research'),
        (FORESTRY, 'Forestry'),
        (ENERGY, 'Energy'),
        (INFRASTRUCTURE, 'Infrastructure'),
        (ENGINEERING, 'Engineering'),
        (TELECOMMUNICATIONS, 'Telecommunications'),
        (PHARMACEUTICAL, 'Pharmaceutical')
    ]

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


class UserLogin(AuthenticationForm):
    email = forms.EmailField(required=True)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ("email", "password")
