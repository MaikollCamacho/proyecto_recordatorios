from django import forms
from .models import Recordatorio


class RecordatorioForm(forms.ModelForm):

    class Meta:
        model = Recordatorio
        fields = ["titulo", "descripcion", "fecha", "prioridad"]

    def clean_titulo(self):
        titulo = self.cleaned_data.get("titulo")

        if len(titulo) < 3:
            raise forms.ValidationError(
                "El título debe tener al menos 3 caracteres"
            )

        return titulo