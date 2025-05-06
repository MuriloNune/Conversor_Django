from django import forms

class DocumentForm(forms.Form):
    original_file = forms.FileField(
        label="Selecione o arquivo",
        widget=forms.ClearableFileInput(attrs={
            'accept': '.pdf,.docx,.jpg,.jpeg,.png',
            'class': 'file-input' 
        })       
    )
    target_format = forms.ChoiceField(
        label="Converter para",
        choices=[
            ('docx', 'DOCX (Word)'),
            ('pdf', 'PDF'),
            ('jpg', 'JPG (Imagem)')
        ],
        widget=forms.Select(attrs={'class': 'format-select'})  
    )