from django import forms
from .models import ProgresoUsuario


class ProgresoUsuarioForm(forms.ModelForm):
    """Formulario para crear y editar progreso de usuario"""
    
    class Meta:
        model = ProgresoUsuario
        fields = ['actividad', 'progreso', 'completado', 'resultado']
        widgets = {
            'actividad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la actividad'
            }),
            'progreso': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'completado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'resultado': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Resultado o notas adicionales (opcional)'
            }),
        }
        labels = {
            'actividad': 'Actividad',
            'progreso': 'Progreso (%)',
            'completado': 'Completado',
            'resultado': 'Resultado',
        }
    
    def clean_progreso(self):
        progreso = self.cleaned_data.get('progreso')
        if progreso is not None:
            if progreso < 0:
                raise forms.ValidationError('El progreso no puede ser negativo.')
            if progreso > 100:
                raise forms.ValidationError('El progreso no puede ser mayor a 100%.')
        return progreso
    
    def clean(self):
        cleaned_data = super().clean()
        progreso = cleaned_data.get('progreso')
        completado = cleaned_data.get('completado')
        
        # Si está marcado como completado, asegurar que el progreso sea 100%
        if completado and progreso != 100:
            cleaned_data['progreso'] = 100
            self.add_error('progreso', 'Si está completado, el progreso debe ser 100%.')
        
        return cleaned_data


class FiltroProgresoForm(forms.Form):
    """Formulario para filtrar el progreso"""
    
    actividad = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por actividad...'
        })
    )
    
    completado = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('true', 'Completados'),
            ('false', 'En progreso'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
