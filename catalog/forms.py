from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ('version')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_product_name(self):
        product_name = self.cleaned_data['product_name']

        if product_name in ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']:
            raise forms.ValidationError('Слово запрещено в названии продукта')
        return product_name

