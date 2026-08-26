from django import forms


class ChatMessageForm(forms.Form):
    content = forms.CharField(max_length=4000, strip=True, widget=forms.Textarea)