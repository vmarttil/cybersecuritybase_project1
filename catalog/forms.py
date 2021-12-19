import datetime
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in the past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class LoanBookForm(forms.Form):
    User = get_user_model()
    all_users = User.objects.all()
    user_list = []
    for user in all_users:
        user_list.append((user.id,user.username))
    borrower = forms.ChoiceField(choices=user_list)
    return_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    
    def clean_return_date(self):
        data = self.cleaned_data['return_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - return date in the past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - return more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class ReviewBookForm(forms.Form):
    STAR_RATINGS = [
      (1, '*'),
      (2, '**'),
      (3, '***'),
      (4, '****'),
      (5, '*****'),
    ]
    stars = forms.ChoiceField(choices=STAR_RATINGS)
    review_text = forms.CharField(max_length=4096)