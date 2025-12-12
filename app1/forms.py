from django import forms
from .models import TipoMascota, Mascota, Persona, PostMascota
from datetime import date

class TipoMascotaForm(forms.ModelForm):
    class Meta:
        model = TipoMascota
        fields = ['nombre', 'descripcion']

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Perro'
            }),
            'descripcion': forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Ej. Mascotas caninas de todas las razas',
                'rows':3
            })
        }

        labels = {
            'nombre':'Nombre del tipo',
            'descripcion': 'Descripcion'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or nombre.strip() == '':
            raise forms.ValidationError("El nombre no puede estar vacio")
        if TipoMascota.objects.filter(nombre__iexact=nombre.strip()).exists():
            raise forms.ValidationError("Este tipo de mascota ya existe")
        return nombre.strip()

    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get('nombre')
        descripcion = cleaned.get('descripcion')
        if nombre and descripcion and nombre.strip().lower() == descripcion.strip().lower():
            raise forms.ValidationError("El nombre y la descripcion no pueden ser iguales")
        return cleaned



    """
        =========================================================
         SECCIÓN: CREAR EL FORMULARIO PostMascotaForm
         ---------------------------------------------------------
         TODO: Crear el formulario con los campos indicados
        =========================================================
    """

class PostMascotaForm(forms.ModelForm):
    class Meta:
        model = PostMascota
        fields = ['titulo', 'descripcion', 'fecha', 'foto']

        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título del post'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción del post (mínimo 20 caracteres)',
                'rows': 4
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Seleccione la fecha'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

        labels = {
            'titulo': 'Título del post',
            'descripcion': 'Descripción',
            'fecha': 'Fecha de publicación',
            'foto': 'Foto del post'
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if not descripcion or len(descripcion.strip()) < 20:
            raise forms.ValidationError("La descripción debe tener como mínimo 20 caracteres")
        return descripcion

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha > date.today():
            raise forms.ValidationError("No se puede registrar una publicación con fecha mayor a la fecha actual")
        return fecha