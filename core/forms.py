from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, label='Your Name')
    email = forms.EmailField(label='Email Address')
    subject = forms.CharField(max_length=150, label='Subject')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='Message')
    phone = forms.CharField(max_length=30, required=False, label='Phone (optional)')
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # honeypot

    def clean_website(self):
        # Simple honeypot: bots often fill every field
        val = self.cleaned_data.get('website', '')
        if val:
            raise forms.ValidationError('Spam detected')
        return val

