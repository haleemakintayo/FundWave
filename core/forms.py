from django import forms
from decimal import Decimal

class DonationForm(forms.Form):
    DONATION_TYPES = [
        ('regular', 'Regular Donation'),
        ('test', 'Test Donation'),
        ('offline', 'Offline Donation'),
    ]
    
    # Amount fields
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        required=False
    )
    custom_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        required=False
    )
    
    # Personal information
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    comment = forms.CharField(
        widget=forms.Textarea,
        required=False,
        max_length=500
    )
    
    # Donation options
    donation_type = forms.ChoiceField(
        choices=DONATION_TYPES,
        required=True
    )
    anonymous_donation = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        custom_amount = cleaned_data.get('custom_amount')

        if not amount and not custom_amount:
            raise forms.ValidationError("Please specify either a predefined or custom amount")
        
        if amount and custom_amount:
            raise forms.ValidationError("Please specify either a predefined or custom amount, not both")
        
        # Set the final amount
        cleaned_data['final_amount'] = amount or custom_amount
        
        return cleaned_data
