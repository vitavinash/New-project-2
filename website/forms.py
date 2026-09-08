from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "company", "company_size", "interest", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+91 98765 43210"}),
            "company": forms.TextInput(attrs={"placeholder": "Company name"}),
            "interest": forms.TextInput(attrs={"placeholder": "QMS, training, audits, CAPA..."}),
            "message": forms.Textarea(attrs={"placeholder": "Tell us what quality process you want to improve", "rows": 4}),
        }
