from flask import Flask, jsonify, render_template_string
import datetime
import socket
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Práctica CI/CD - Resumen</title>
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #34495e;
            --accent-color: #3498db;
            --text-dark: #2c3e50;
            --bg-light: #f8f9fa;
            --border-radius: 8px;
            --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            margin: 0; padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: var(--text-dark);
        }
        .container {
            background: #ffffff;
            padding: 40px;
            border-radius: var(--border-radius);
            width: 90%; max-width: 900px;
            box-shadow: var(--box-shadow);
        }
        h1 {
            text-align: center;
            color: var(--primary-color);
        }
        .section {
            margin-top: 30px;
            padding: 20px;
            background: var(--bg-light);
            border-left: 4px solid var(--accent-color);
            border-radius: var(--border-radius);
        }
        .tech-badge {
            background: var(--accent-color);
            color: #fff;
            padding: 8px 16px;
            border-radius: 20px;
            margin: 5px;
            display: inline-block;
        }
        .team-box {
            margin-top: 20px;
            padding: 20px;
            background: #eef3f7;
            border-radius: var(--border-radius);
        }
    </style>
</head>
<body>
    <div class=\"container\">
        <h1>Resumen de la Práctica CI/CD en AKS</h1>

        <div class=\"section\">
            <h3>Descripción General</h3>
            <p>
                Esta práctica implementa un pipeline CI/CD completo utilizando herramientas modernas de DevOps.
                El objetivo es demostrar la automatización del ciclo de vida de una aplicación contenedorizada,
                desde su construcción hasta su despliegue en Azure Kubernetes Service (AKS).
            </p>
        </div>

        <div class=\"section\">
            <h3>Tecnologías Utilizadas</h3>
            <div>
                <span class=\"tech-badge\">Docker</span>
                <span class=\"tech-badge\">GitHub Actions</span>
                <span class=\"tech-badge\">Kubernetes</span>
                <span class=\"tech-badge\">Azure AKS</span>
                <span class=\"tech-badge\">Azure Container Registry</span>
                <span class=\"tech-badge\">Terraform</span>
            </div>
        </div>

        <div class=\"section\">
            <h3>Objetivo Principal</h3>
            <p>
                El objetivo del proyecto es demostrar la capacidad de construir, empaquetar, enviar y desplegar
                una aplicación a un entorno orquestado en la nube de manera completamente automatizada.
            </p>
        </div>

        <div class=\"section team-box\">
            <h3>Equipo de Trabajo</h3>
            <p>Integrantes:</p>
            <ul>
                <li>Luis Felipe Mutis Chavez</li>
                <li>Victor Campo</li>
                <li>Andres Ruiz</li>
                <li>Javier Ortiz</li>
            </ul>
        </div>

        <div class=\"section\">
            <h3>Información del Servidor</h3>
            <p><strong>Hostname:</strong> {{ hostname }}</p>
            <p><strong>Fecha y Hora:</strong> {{ current_time }}</p>
            <p><strong>Versión:</strong> {{ version }}</p>
        </div>
    </div>
</body>
</html>
"""


def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "3.0.0"
    }

@app.route('/')
def home():
    sys = get_system_info()
    return render_template_string(HTML_TEMPLATE, **sys)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "api",
        "version": "3.0.0",
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
