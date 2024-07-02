from dal import autocomplete
from django import forms
from .models import Alet, Teknisyen, AletHareketi, Raf

class AletForm(forms.ModelForm):
    raf = forms.ModelChoiceField(
        queryset=Raf.objects.all(),  # Raf modelinden tüm rafları al
        widget=autocomplete.ModelSelect2(url='raf-autocomplete')
    )
    teknisyen = forms.ModelChoiceField(
        queryset=Teknisyen.objects.all(),
        widget=autocomplete.ModelSelect2(url='teknisyen-autocomplete'),
        required=False
    )

    class Meta:
        model = Alet
        fields = ['isim', 'marka', 'model', 'raf', 'durum', 'teknisyen']
        widgets = {
            'durum': forms.Select(choices=Alet.DURUM_SECENEKLERI),
        }

    def __init__(self, *args, **kwargs):
        super(AletForm, self).__init__(*args, **kwargs)
        self.fields['teknisyen'].queryset = Teknisyen.objects.all()
        # self.fields['raf'].queryset = Alet.objects.values_list('raf', flat=True).distinct()

        # Eğer alet düzenleme ise, başlangıçta seçili olan teknisyeni ve rafı ayarla
        if self.instance.pk:
            self.fields['teknisyen'].initial = self.instance.teknisyen
            self.fields['raf'].initial = self.instance.raf

class TeknisyenForm(forms.ModelForm):
    class Meta:
        model = Teknisyen
        fields = ['isim', 'telefon']

class AletHareketiForm(forms.ModelForm):
    alet = forms.ModelChoiceField(
        queryset=Alet.objects.all(),
        widget=autocomplete.ModelSelect2(url='alet-autocomplete')
    )
    teknisyen = forms.ModelChoiceField(
        queryset=Teknisyen.objects.all(),
        widget=autocomplete.ModelSelect2(url='teknisyen-autocomplete')
    )

    class Meta:
        model = AletHareketi
        fields = ['alet', 'teknisyen']

class RafForm(forms.ModelForm):
    class Meta:
        model = Raf
        fields = ['isim']
