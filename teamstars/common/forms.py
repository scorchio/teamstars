from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

# todo for some reason, the validator message never gets translated
class UserSettingsForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               validators=[RegexValidator('^[\\w.@+-]+$',
                                                          _('Enter a valid username. '
                                                            'This value may contain only letters, numbers '
                                                            'and @/./+/-/_ characters.'),
                                                          'invalid')])

    class Meta:
        model = User
