from django import forms
from .models import CheckList, CheckSingle


class CheckListForm(forms.ModelForm):

    class Meta:
        model = CheckList
        fields = ['proxy_list']
        widgets = {
            'proxy_list': forms.Textarea(attrs={'class':'form-control h-150px', 'rows':'10', 'id':'proxy_list'}),
        }


class SingleCheckForm(forms.ModelForm):

    class Meta:
        model = CheckSingle
        fields = "__all__"
        widgets = {
            'ip_addr': forms.TextInput(attrs={'class':'form-control', 'type':'text', 'id':'ip_addr', 'placeholder':'0.0.0.0'}),
            'port': forms.NumberInput(attrs={'class':'form-control', 'type':'number', 'id':'port', 'placeholder':'8080'}),
            'username': forms.TextInput(attrs={'class':'form-control', 'type':'text', 'id':'username', 'placeholder':'user'}),
            'password': forms.TextInput(attrs={'class':'form-control', 'type':'text', 'id':'password', 'placeholder':'passwd'}),
        }