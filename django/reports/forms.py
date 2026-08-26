from django import forms

from .models import Report


class ReportUploadForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'file')

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if uploaded_file.size > 10 * 1024 * 1024:
            raise forms.ValidationError('The report must be 10 MB or smaller.')
        if uploaded_file.content_type != 'application/pdf' or uploaded_file.read(4) != b'%PDF':
            raise forms.ValidationError('Only valid PDF files are supported.')
        uploaded_file.seek(0)
        return uploaded_file