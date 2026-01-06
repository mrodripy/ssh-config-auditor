🔐 SSH Configuration Auditor & Hardening Tool

https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/License-MIT-green.svg
https://img.shields.io/github/issues/tu-usuario/ssh-config-auditor
https://img.shields.io/github/stars/tu-usuario/ssh-config-auditor?style=social

Herramienta profesional en Python para auditar y asegurar configuraciones SSH (sshd_config) contra benchmarks de seguridad CIS. Detecta vulnerabilidades críticas como PermitRootLogin yes y PasswordAuthentication yes, generando reportes claros de cumplimiento.

Proyecto en dos fases: Auditoría automatizada (✓ Completado) → Contenerización con Docker (🚧 En progreso).
✨ Características

    ✅ Auditoría automática de archivos de configuración SSH

    ✅ Comparación contra baseline CIS/NIST personalizable

    ✅ Detección de configuraciones críticas: PermitRootLogin, Protocol 1, contraseñas vacías

    ✅ Reportes múltiples: Texto claro y JSON para integración

    ✅ Clasificación por severidad: HIGH, MEDIUM, LOW

    ✅ Fácil de extender: Arquitectura modular para nuevas reglas

    ✅ Pruebas unitarias: Cobertura para funcionalidad principal

📸 Demostración Rápida
Ejecución Básica
bash

$ python src/ssh_audit.py samples/insecure_sshd_config
[+] Baseline cargado: 12 reglas de seguridad
[+] Auditing: samples/insecure_sshd_config
[+] Auditoría completada: 12 hallazgos

Reporte de Ejemplo
text

============================================================
SSH CONFIGURATION AUDIT REPORT
============================================================
✅ Protocol: Expected='2', Actual='2' | Status: COMPLIANT (LOW)
❌ PermitRootLogin: Expected='no', Actual='yes' | Status: NON_COMPLIANT (HIGH)
❌ PasswordAuthentication: Expected='no', Actual='yes' | Status: NON_COMPLIANT (HIGH)
...
============================================================
SUMMARY
============================================================
Total Rules Checked: 12
✅ Compliant: 2
❌ Non-Compliant: 6
🔶 Not Set (Missing): 4

🚀 Comenzando
Prerrequisitos

    Python 3.8 o superior

    Git (para clonación)

Instalación Rápida
bash

# 1. Clona el repositorio
git clone https://github.com/tu-usuario/ssh-config-auditor.git
cd ssh-config-auditor

# 2. (Opcional) Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3. Prueba inmediatamente
python src/ssh_audit.py samples/insecure_sshd_config

📖 Uso
Auditoría Básica
bash

# Usa el baseline por defecto (CIS)
python src/ssh_audit.py /etc/ssh/sshd_config

# Especifica un archivo de configuración personalizado
python src/ssh_audit.py /ruta/a/mi_ssh.conf -b configs/mi_baseline.conf

Opciones de Reporte
bash

# Formato JSON para integración con otras herramientas
python src/ssh_audit.py samples/insecure_sshd_config -o json

# Guardar reporte en archivo
python src/ssh_audit.py samples/insecure_sshd_config -f reporte_seguridad.txt

# Combinar opciones
python src/ssh_audit.py /etc/ssh/sshd_config -o json -f auditoria.json

Ayuda Completa
bash

python src/ssh_audit.py --help

# Salida:
# usage: ssh_audit.py [-h] [-b BASELINE] [-o {text,json}] [-f OUTPUT_FILE] config_file
# 
# SSH Configuration Auditor - Fase 1
# 
# positional arguments:
#   config_file           Ruta al archivo de configuración SSH a auditar
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -b BASELINE, --baseline BASELINE
#                         Ruta al archivo baseline de seguridad (default: configs/cis_baseline.conf)
#   -o {text,json}, --output {text,json}
#                         Formato del reporte de salida (default: text)
#   -f OUTPUT_FILE, --output-file OUTPUT_FILE
#                         Guardar reporte en un archivo

📁 Estructura del Proyecto
text

ssh-config-auditor/
├── src/                    # Código fuente principal
│   ├── ssh_audit.py       # Clase principal del auditor
│   └── __init__.py
├── tests/                  # Pruebas unitarias
│   └── test_basic.py      # Pruebas de funcionalidad básica
├── configs/               # Baselines de seguridad
│   └── cis_baseline.conf  # Baseline CIS por defecto
├── samples/               # Configuraciones de ejemplo
│   └── insecure_sshd_config
├── docs/                  # Documentación adicional
├── .gitignore            # Archivos ignorados por Git
├── requirements.txt      # Dependencias Python
├── LICENSE              # Licencia MIT
└── README.md           # Este archivo

🧪 Ejecutar Pruebas
bash

# Ejecutar todas las pruebas
python -m pytest tests/

# Ejecutar pruebas específicas
python tests/test_basic.py

# Con cobertura (opcional)
pip install pytest-cov
python -m pytest tests/ --cov=src

🔧 Personalización
Crear tu Propio Baseline

    Copia configs/cis_baseline.conf a configs/mi_baseline.conf

    Modifica las reglas según tus necesidades:

bash

# configs/mi_baseline.conf
Protocol 2
PermitRootLogin prohibit-password  # Más permisivo que 'no'
PasswordAuthentication no
MaxAuthTries 4                     # Ajustado a tu política
# ... añade tus propias reglas

    Usa tu baseline:

bash

python src/ssh_audit.py mi_config.conf -b configs/mi_baseline.conf

Extender con Nuevas Reglas

El auditor está diseñado para ser extendido. Añade nuevas reglas al archivo baseline y serán automáticamente incluidas en la auditoría.
🗺️ Roadmap
✅ Fase 1 - Completada

    Auditoría básica de configuraciones SSH

    Baseline CIS preconfigurado

    Reportes en texto y JSON

    Pruebas unitarias

🚧 Fase 2 - En Desarrollo

    Contenerización con Docker

    Imagen Docker pública en Docker Hub

    Integración CI/CD con GitHub Actions

    Dashboard web básico con Flask/FastAPI

🔮 Futuro

    Módulo de auto-remediación (sugerencia de comandos fix)

    Soporte para auditoría remota (vía SSH)

    Plugin para Ansible/Puppet/Chef

🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

    Haz fork del repositorio

    Crea una rama para tu característica (git checkout -b feature/AmazingFeature)

    Haz commit de tus cambios (git commit -m 'Add some AmazingFeature')

    Push a la rama (git push origin feature/AmazingFeature)

    Abre un Pull Request

Por favor, asegúrate de actualizar las pruebas según corresponda.
📄 Licencia

Distribuido bajo la Licencia MIT. Ver LICENSE para más información.
👨‍💻 Autor

Tu Nombre

    GitHub: @tu-usuario

    LinkedIn: Tu Perfil

    Portfolio: Más proyectos

🙏 Agradecimientos

    CIS Benchmarks por las mejores prácticas de seguridad

    Comunidad de seguridad open source por la inspiración

    Python community por las herramientas increíbles

⭐ Si este proyecto te es útil, ¡dale una estrella en GitHub!
