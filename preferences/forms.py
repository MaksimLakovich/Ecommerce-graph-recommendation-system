from django import forms

from catalog.models import Aisle


class UserPreferencesForm(forms.Form):
    """Форма выбора явных предпочтений покупателем (товарные ряды/aisles)."""

    aisles = forms.ModelMultipleChoiceField(
        queryset=Aisle.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        # label="Зафиксируйте товарные категории, которые вам интересны",
    )
