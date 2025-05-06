import os
import platform
import requests
import zipfile
import tarfile
from io import BytesIO
from django.conf import settings

class PopplerManager:
    @staticmethod
    def _download_poppler():
        """Baixa e extrai os binários do Poppler direto do GitHub"""
        poppler_dir = os.path.join(settings.BASE_DIR, 'temp', 'poppler')
        os.makedirs(poppler_dir, exist_ok=True)

        # URLs dos binários pré-compilados
        repo_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.11.0/"
        bin_url = repo_url + "poppler-23.11.0_x86.7z" if platform.system() == "Windows" else None

        if not bin_url:
            raise RuntimeError("Sistema não suportado para download automático")

        # Download e extração
        response = requests.get(bin_url)
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(poppler_dir)

        return os.path.join(poppler_dir, 'Library', 'bin')

    @staticmethod
    def convert_pdf_to_jpg(pdf_path, output_path, dpi=300):
        poppler_path = PopplerManager._download_poppler()
        
        from pdf2image import convert_from_path
        images = convert_from_path(
            pdf_path,
            poppler_path=poppler_path,
            dpi=dpi,
            first_page=1,
            last_page=1
        )
        images[0].save(output_path, 'JPEG', quality=95)