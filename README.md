# MentorHUB

MentorHUB es una plataforma web diseñada para conectar mentores y aprendices, facilitando la interacción, el aprendizaje y el intercambio de conocimientos.  
Incluye funcionalidades como registro de usuarios, inicio de sesión, perfiles personalizados, mensajería, foros y recomendaciones personalizadas.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Rutas Principales](#rutas-principales)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## 🚀 Características

- **Registro e inicio de sesión**: Permite a los usuarios crear cuentas y autenticarse.
- **Gestión de perfiles**: Personalización de perfil, incluyendo foto y nombre.
- **Mensajería**: Comunicación entre usuarios mediante un sistema de mensajes.
- **Recomendaciones**: Sugerencias personalizadas de perfiles y publicaciones.
- **Foros**: Espacios de discusión y publicación de temas.
- **Seguridad**: Contraseñas encriptadas y autenticación segura.

---

## 🗂️ Estructura del Proyecto


TFC-THECNOHUB/
├── formularios/             # Módulo para formularios y rutas relacionadas
├── perfil/                  # Módulo para gestión de perfiles
├── mensajes/                # Módulo para mensajería
├── static/                  # Archivos estáticos (CSS, JS, imágenes)
│   ├── styles/              # Estilos CSS y scripts JS
│   ├── css_components/      # Estilos específicos para componentes
│   ├── profile_components/  # Componentes HTML dinámicos para perfiles
├── templates/               # Plantillas HTML
│   ├── components/          # Componentes reutilizables
├── BaseManager.py           # Gestión de la base de datos
├── Encripter.py             # Encriptación de contraseñas
├── User.py                  # Modelo de usuario
├── main.py                  # Archivo principal de la aplicación Flask
├── requirements.txt         # Dependencias del proyecto
├── .gitignore               # Archivos ignorados por Git
├── README.md                # Documentación del proyecto
└── LICENSE                  # Licencia del proyecto

## ✅ Requisitos Previos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Entorno virtual (opcional pero recomendado)

---

## 🛠️ Instalación

### 🔧 Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/TFC-THECNOHUB.git
cd TFC-THECNOHUB
```

## 🐍 Crea un entorno virtual y actívalo:

```bash
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
```

## 📦 Instala las dependencias:

```bash
pip install -r requirements.txt
```

## 🔑 Configura las variables de entorno en un archivo .env:

```ini
MASTER_KEY=tu_clave_maestra
```

## 🔥 Configura Firebase:
- **Coloca el archivo de credenciales JSON en la raíz del proyecto.**

## 🌐 Rutas Principales

### 🔑 Autenticación

- `/` → Página de inicio de sesión.
- `/register` → Registro de nuevos usuarios.
- `/incorrect` → Página de error de credenciales incorrectas.

### 🏠 Funcionalidades

- `/index` → Página principal con recomendaciones y publicaciones.
- `/profile/main` → Gestión del perfil del usuario.
- `/mensajes/main/mensajes` → Sistema de mensajería.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
  <img src="https://img.shields.io/badge/Flask-%23000000.svg?style=for-the-badge&logo=flask&logoColor=white" alt="Flask Badge">
  <img src="https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black" alt="Firebase Badge">
  <img src="https://img.shields.io/badge/Development-Active-brightgreen?style=for-the-badge" alt="Development Badge">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License Badge">
</p>

