from django import forms
from .models import Room

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model=Room
        fields="__all__"
        exclude=['host','participant']