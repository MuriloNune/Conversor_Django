import os
import tempfile
import pythoncom
import comtypes.client
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
from pdf2docx import Converter
from docx import Document
from docx.shared import Pt
import img2pdf
from pdf2image import convert_from_path
from .utils.poppler_utils import PopplerManager

def convert_file(request):
    context = {}
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                
                fs = FileSystemStorage()
                original_file = request.FILES['original_file']
                target_format = form.cleaned_data['target_format']
                
                
                valid_extensions = ['.pdf', '.docx', '.jpg', '.jpeg', '.png']
                file_ext = os.path.splitext(original_file.name)[1].lower()
                
                if file_ext not in valid_extensions:
                    raise ValueError("Tipo de arquivo não suportado")
                
               
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'converted'), exist_ok=True)
                
                
                output_filename = f"converted_{os.path.splitext(original_file.name)[0]}.{target_format}"
                output_path = os.path.join(settings.MEDIA_ROOT, 'converted', output_filename)
                
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                    for chunk in original_file.chunks():
                        tmp_file.write(chunk)
                    tmp_path = tmp_file.name
                
                try:
                   
                    if target_format == 'docx':
                        if file_ext == '.pdf':
                            convert_pdf_to_docx(tmp_path, output_path)
                        else:
                            raise ValueError("Conversão para DOCX disponível apenas a partir de PDF")
                    
                    elif target_format == 'pdf':
                        if file_ext in ['.jpg', '.jpeg', '.png']:
                            convert_image_to_pdf(tmp_path, output_path)
                        elif file_ext == '.docx':
                            convert_docx_to_pdf(tmp_path, output_path)
                    
                    elif target_format == 'jpg':
                        if file_ext == '.pdf':
                            PopplerManager.convert_pdf_to_jpg(tmp_path, output_path)
                        elif file_ext == '.docx':
                            raise ValueError("Conversão direta de DOCX para JPG não suportada")
                    
                    
                    converted_url = os.path.join(settings.MEDIA_URL, 'converted', output_filename)
                    request.session['converted_file_url'] = converted_url
                    request.session['converted_filename'] = output_filename
                    return redirect('download')
                
                finally:
                    
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                
            except Exception as e:
                context['error'] = f"Erro na conversão: {str(e)}"
                print(f"DETALHES DO ERRO: {str(e)}")
        else:
            context['error'] = "Formulário inválido"
    else:
        form = DocumentForm()
    
    context['form'] = form
    return render(request, 'converter/upload.html', context)

def convert_pdf_to_docx(input_path, output_path):
    """Converte PDF para DOCX preservando layout"""
    try:
        cv = Converter(input_path)
        cv.convert(
            output_path,
            multi_processing=True,
            debug=False,
            keep_blank_lines=True,
            image_settings={
                'image_dpi': 200,
                'image_quality': 90,
                'ignore_duplicate_images': False
            },
            table_settings={
                'row_split': False,
                'flow': False,
                'border_width': 0.1,
                'vertical_strategy': 'lines',
                'horizontal_strategy': 'lines'
            },
            font_settings={
                'bold': True,
                'italic': True,
                'underline': True
            }
        )
        cv.close()

        
        doc = Document(output_path)
        for section in doc.sections:
            section.top_margin = Pt(50)
            section.bottom_margin = Pt(50)
            section.left_margin = Pt(50)
            section.right_margin = Pt(50)
            
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(11)
                run.font.name = 'Calibri'
        
        doc.save(output_path)
        
    except Exception as e:
        raise ValueError(f"Falha na conversão PDF para DOCX: {str(e)}")

def convert_image_to_pdf(input_path, output_path):
    """Converte imagem para PDF"""
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(input_path))

def convert_docx_to_pdf(input_path, output_path):
    """Converte DOCX para PDF"""
    if os.name == 'nt':  
        pythoncom.CoInitialize()
        try:
            word = comtypes.client.CreateObject('Word.Application')
            doc = word.Documents.Open(input_path)
            doc.SaveAs(output_path, FileFormat=17) 
            doc.Close()
            word.Quit()
        finally:
            pythoncom.CoUninitialize()
    else:  
        import subprocess
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', os.path.dirname(output_path),
            input_path
        ], check=True)

def download(request):
    """Lida com o download do arquivo convertido"""
    converted_url = request.session.get('converted_file_url', '')
    filename = request.session.get('converted_filename', '')
    
    if not converted_url or not filename:
        return redirect('home')
    
    file_path = os.path.join(settings.MEDIA_ROOT, converted_url.replace(settings.MEDIA_URL, ''))
    if not os.path.exists(file_path):
        return render(request, 'converter/download.html', {
            'error': 'Arquivo não encontrado no servidor'
        })
    
    return render(request, 'converter/download.html', {
        'converted_file_url': converted_url,
        'filename': filename,
        'file_size': os.path.getsize(file_path),
        'file_type': filename.split('.')[-1].upper()
    })