from django import forms


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField(
        widget=forms.EmailInput,
    )
    message = forms.CharField(
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Your name'
        self.fields['email'].widget.attrs['placeholder'] = 'Your email'
        self.fields['message'].widget.attrs['placeholder'] = 'Please enter your message here...'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control floatingInput rounded'
