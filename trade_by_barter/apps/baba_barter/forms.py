from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, Row, Column


class SignUpForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=20)
    last_name = forms.CharField(required=True, max_length=20)
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(required=True)
    description = forms.CharField(max_length=255, widget=forms.Textarea())
    password = forms.PasswordInput()
    confirm_password = forms.PasswordInput()
    consent = forms.CheckboxInput()

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'signup_form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('baba:process_signup')
        self.helper.add_input(
            Submit(
                'submit', 
                'SIGN UP', 
                css_class='mt-12 mt-md-10 btn text-black signup_signup_button border-dark p-1',
                style='background-color: #f07167; height: 50px; width: 200px;'
            )
        )
        self.helper.layout = Layout(
                Column(
                    'first_name',
                    placeholder='First Name', 
                    css_class='form-control mb-4 border-dark',
                    type='text, new',
                    name='first_name',
                    title='Your first name',
                    style='background-color: #f07167;'
                )
            
        )