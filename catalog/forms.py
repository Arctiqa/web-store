from django import forms

from catalog.models import Product, Version


class MixinFormControl:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(MixinFormControl, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('owner',)

    def clean_product_name(self):
        product_name = self.cleaned_data['product_name']

        if product_name in ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                            'радар']:
            raise forms.ValidationError('Слово запрещено в названии продукта')
        return product_name


class VersionForm(MixinFormControl, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def clean_version_name(self):
        valid_version = self.cleaned_data['version']

        if valid_version < 0:
            raise forms.ValidationError('Номер версии не может быть отрицательным')
        return valid_version


