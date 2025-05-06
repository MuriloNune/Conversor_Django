# Conversor de Arquivos Django

🔁 Um aplicativo web para conversão de arquivos com interface moderna e responsiva, desenvolvido em Django.

## ✨ Funcionalidades
- Upload de arquivos para conversão
- Visualização do status do processamento em tempo real
- Download do arquivo convertido
- Interface limpa com feedback visual (alertas, animações)
- Design responsivo seguindo padrões modernos

## 🛠️ Tecnologias Utilizadas
- **Backend**: Django (Python)
- **Frontend**: 
  - HTML/CSS puro com variáveis CSS modernas
  - JavaScript (Fetch API para chamadas assíncronas)
- **Estilo**: 
  - Design system com cores semânticas (sucesso, erro, etc.)
  - Componentes reutilizáveis (cards, botões)
  - Efeitos de hover e transições suaves

## 🎨 Design System
O projeto utiliza um sistema de cores profissional inspirado em plataformas modernas:
```css
:root {
    --linkedin-blue: #0A66C2;
    --dark-text: #1D2226;
    --gray-text: #666666;
    --light-bg: #F9FAFB;
    --white: #FFFFFF;
    --border-color: #E0E0E0;
    --success-green: #00A884;
    --error-red: #D32F2F;
}
🚀 Como Executar o Projeto
Pré-requisitos
Python 3.8+

Django 3.2+

Node.js (opcional para assets)

Instalação
Clone o repositório:

bash
git clone https://github.com/seu-usuario/conversor-django.git
cd conversor-django
Crie e ative um ambiente virtual:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instale as dependências:

bash
pip install -r requirements.txt
Execute as migrações:

bash
python manage.py migrate
