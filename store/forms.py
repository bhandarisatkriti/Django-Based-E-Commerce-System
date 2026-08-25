from django import forms

from store.models import Category, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image', 'is_sale', 'sale_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_sale = cleaned_data.get('is_sale')
        sale_price = cleaned_data.get('sale_price')
        price = cleaned_data.get('price')

        if is_sale:
            if sale_price is None:
                self.add_error('sale_price', 'Sale price is required when the product is marked as on sale.')
            elif price is not None and sale_price >= price:
                self.add_error('sale_price', 'Sale price must be lower than the regular price.')

        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
