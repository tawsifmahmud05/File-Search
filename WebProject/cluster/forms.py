from django import forms
from django.forms import (formset_factory, modelformset_factory)

from .models import (Url, Cluster, File)

#Create File model form
class FileModelForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['fileurl', 'filetype', 'content', 'mainurl', 'filecluster']
#Create Cluster Form

class ClusterModelForm(forms.ModelForm):

    class Meta:
        model = Cluster
        fields = ('name', )
        labels = {
            'name': 'Cluster name'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter cluster name'
            }
            )
        }

#Create Searchform
class SearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['usercluster'].queryset = Cluster.objects.filter(
            owner=user)

    usercluster = forms.ModelChoiceField(
        queryset=None, widget=forms.Select(attrs={'class': "form-control"}), required=True)
    keyword = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control"}))


UrlFormset = modelformset_factory(
    Url,
    fields=('url', 'depth', 'crawling_strategy'),
    extra=1,
    widgets={'url': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Url'
    }), 'depth': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter depth'
    }), 'crawling_strategy': forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Enter desired strategy'
    })
    }
)
