from flask import Flask, jsonify, render_template_string
import os
import datetime
import subprocess
import json
import socket

app = Flask(__name__)

# HTML template para la página principal
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Pipeline CI/CD - AKS Demo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 900px;
            margin: 20px;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .subtitle {
            font-size: 1.3em;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .info-box {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            text-align: left;
        }
        .tech-stack {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }
        .tech-badge {
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 30px;
            flex-wrap: wrap;
            gap: 15px;
        }
        .stat-item {
            text-align: center;
            flex: 1;
            min-width: 120px;
        }
        .stat-value {
            font-size: 1.8em;
            font-weight: bold;
            display: block;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }
        .footer {
            margin-top: 30px;
            font-size: 0.9em;
            opacity: 0.7;
        }
        .status-up {
            color: #4CAF50;
        }
        .status-down {
            color: #f44336;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 ¡Pipeline CI/CD Exitoso!</h1>
        <div class="subtitle">
            Microservicios desplegados en Azure Kubernetes Service (AKS)
        </div>
        
        <div class="info-box">
            <h3>📊 Estado del Cluster en Tiempo Real:</h3>
            <p><strong>🏗️ Nuestros Pods:</strong> <span class="status-up">{{ our_pods }} ejecutándose</span></p>
            <p><strong>📈 Total en Cluster:</strong> {{ total_pods }} pods ({{ running_pods }} activos)</p>
            <p><strong>⏰ Uptime:</strong> {{ deployment_time }}</p>
            <p><strong>🔗 Estado:</strong> <span class="status-up">{{ cluster_status }}</span></p>
            <p><strong>🖥️ Host:</strong> {{ hostname }}</p>
        </div>

        <div class="info-box">
            <h3>📋 Práctica Realizada:</h3>
            <p>Implementación completa de pipeline CI/CD para microservicios con:</p>
            <ul>
                <li><strong>GitHub Actions</strong> para automatización</li>
                <li><strong>Azure Container Registry (ACR)</strong> para imágenes</li>
                <li><strong>Azure Kubernetes Service (AKS)</strong> para orquestación</li>
                <li><strong>Infraestructura como Código</strong> con Terraform</li>
                <li><strong>Despliegue automatizado</strong> con health checks</li>
            </ul>
        </div>

        <div class="tech-stack">
            <span class="tech-badge">🐳 Docker</span>
            <span class="tech-badge">⚙️ GitHub Actions</span>
            <span class="tech-badge">☸️ Kubernetes</span>
            <span class="tech-badge">🚀 Azure AKS</span>
            <span class="tech-badge">📦 ACR</span>
            <span class="tech-badge">🏗️ Terraform</span>
        </div>

        <div class="stats">
            <div class="stat-item">
                <span class="stat-value">{{ our_pods }}</span>
                <span>Nuestros Pods</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{{ running_pods }}</span>
                <span>Pods Activos</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{{ deployment_time }}</span>
                <span>Uptime</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{{ version }}</span>
                <span>Versión</span>
            </div>
        </div>

        <div class="footer">
            <p>🛠️ Desarrollado con DevOps Engineering - Pipeline CI/CD</p>
            <p>📅 {{ current_time }} | 🖥️ {{ hostname }}</p>
        </div>
    </div>
</body>
</html>
"""

def run_kubectl_command(command):
    """Ejecutar comando kubectl y retornar resultado"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        return result.stdout.strip() if result.returncode == 0 else "Error"
    except Exception as e:
        return f"Error: {str(e)}"

def get_dynamic_data():
    """Obtener datos dinámicos del cluster Kubernetes"""
    try:
        # 1. Obtener todos los pods
        pods_output = run_kubectl_command("kubectl get pods --all-namespaces --no-headers")
        if pods_output and not pods_output.startswith("Error"):
            pod_lines = [line for line in pods_output.split('\n') if line.strip()]
            running_pods = len([line for line in pod_lines if "Running" in line])
            total_pods = len(pod_lines)
        else:
            running_pods = total_pods = "N/A"

        # 2. Obtener nuestros pods específicos
        our_pods_output = run_kubectl_command("kubectl get pods -l app --no-headers")
        if our_pods_output and not our_pods_output.startswith("Error"):
            our_pods = len([line for line in our_pods_output.split('\n') if line.strip() and "Running" in line])
        else:
            our_pods = "N/A"

        # 3. Obtener tiempo del primer pod
        age_output = run_kubectl_command("kubectl get pods --sort-by=.status.startTime --no-headers -o jsonpath='{.items[0].status.startTime}' 2>/dev/null || echo 'unknown'")
        deployment_time = "Desconocido"
        if age_output and age_output != "unknown" and not age_output.startswith("Error"):
            try:
                start_time = datetime.datetime.fromisoformat(age_output.replace('Z', '+00:00'))
                now = datetime.datetime.now(datetime.timezone.utc)
                delta = now - start_time
                minutes = int(delta.total_seconds() / 60)
                if minutes < 60:
                    deployment_time = f"{minutes}m"
                else:
                    hours = minutes // 60
                    deployment_time = f"{hours}h {minutes % 60}m"
            except:
                deployment_time = "N/A"
        else:
            deployment_time = "N/A"

        return {
            "total_pods": total_pods,
            "running_pods": running_pods,
            "our_pods": our_pods,
            "deployment_time": deployment_time,
            "cluster_info": "Conectado ✅" if pods_output and not pods_output.startswith("Error") else "Error ❌"
        }
        
    except Exception as e:
        return {
            "total_pods": "Error",
            "running_pods": "Error",
            "our_pods": "Error", 
            "deployment_time": "Error",
            "cluster_info": f"Excepción: {str(e)}"
        }

def get_system_info():
    """Obtener información del sistema"""
    return {
        "hostname": socket.gethostname(),
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "2.1.0"
    }

@app.route('/')
def home():
    """Página principal con datos dinámicos"""
    dynamic_data = get_dynamic_data()
    system_info = get_system_info()
    
    return render_template_string(HTML_TEMPLATE, 
        our_pods=dynamic_data["our_pods"],
        total_pods=dynamic_data["total_pods"],
        running_pods=dynamic_data["running_pods"],
        version=system_info["version"],
        deployment_time=dynamic_data["deployment_time"],
        current_time=system_info["current_time"],
        cluster_status=dynamic_data["cluster_info"],
        hostname=system_info["hostname"]
    )

@app.route('/health')
def health():
    """Endpoint de health check (para el pipeline)"""
    return jsonify({
        "status": "healthy",
        "service": "api",
        "version": "2.1.0",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/info')
def api_info():
    """Endpoint API tradicional (para compatibilidad)"""
    return jsonify({
        "service": "ci-cd-demo-api",
        "version": "2.1.0", 
        "status": "healthy",
        "description": "Demo de Pipeline CI/CD con AKS y datos dinámicos",
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
