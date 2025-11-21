from flask import Flask, jsonify, render_template_string
import os
import datetime
import socket
from kubernetes import client, config
from kubernetes.stream import stream
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# HTML template PROFESIONAL - Sin emojis y con diseño corporativo
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pipeline CI/CD - AKS Dashboard</title>
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #34495e;
            --accent-color: #3498db;
            --success-color: #27ae60;
            --warning-color: #e67e22;
            --danger-color: #e74c3c;
            --text-light: #ecf0f1;
            --text-dark: #2c3e50;
            --bg-light: #f8f9fa;
            --border-radius: 8px;
            --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: var(--text-light);
            line-height: 1.6;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: var(--border-radius);
            padding: 40px;
            text-align: center;
            box-shadow: var(--box-shadow);
            max-width: 1000px;
            margin: 20px;
            color: var(--text-dark);
        }
        
        .header {
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.2em;
            margin-bottom: 10px;
            color: var(--primary-color);
            font-weight: 600;
        }
        
        .subtitle {
            font-size: 1.1em;
            color: var(--secondary-color);
            margin-bottom: 30px;
            font-weight: 300;
        }
        
        .info-section {
            background: var(--bg-light);
            border-radius: var(--border-radius);
            padding: 25px;
            margin: 20px 0;
            text-align: left;
            border-left: 4px solid var(--accent-color);
        }
        
        .info-section h3 {
            color: var(--primary-color);
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .info-label {
            font-weight: 600;
            color: var(--secondary-color);
        }
        
        .info-value {
            font-weight: 500;
        }
        
        .status-up {
            color: var(--success-color);
            font-weight: 600;
        }
        
        .status-down {
            color: var(--danger-color);
            font-weight: 600;
        }
        
        .tech-stack {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 12px;
            margin: 25px 0;
        }
        
        .tech-badge {
            background: var(--accent-color);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
            transition: transform 0.2s ease;
        }
        
        .tech-badge:hover {
            transform: translateY(-2px);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            text-align: center;
            border-top: 4px solid var(--accent-color);
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: 700;
            color: var(--primary-color);
            display: block;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: var(--secondary-color);
            font-weight: 500;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
            margin: 15px 0;
        }
        
        .feature-list li {
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }
        
        .feature-list li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: var(--success-color);
            font-weight: bold;
        }
        
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            font-size: 0.85em;
            color: var(--secondary-color);
        }
        
        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
                margin: 10px;
            }
            
            h1 {
                font-size: 1.8em;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Pipeline CI/CD - AKS Dashboard</h1>
            <div class="subtitle">
                Microservicios desplegados en Azure Kubernetes Service
            </div>
        </div>
        
        <div class="info-section">
            <h3>Estado del Cluster en Tiempo Real</h3>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Nuestros Pods:</span>
                    <span class="info-value status-up">{{ our_pods }} ejecutándose</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Total en Cluster:</span>
                    <span class="info-value">{{ total_pods }} pods ({{ running_pods }} activos)</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Tiempo de Actividad:</span>
                    <span class="info-value">{{ deployment_time }}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Conexión Kubernetes:</span>
                    <span class="info-value {{ status_class }}">{{ cluster_status }}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Servidor:</span>
                    <span class="info-value">{{ hostname }}</span>
                </div>
            </div>
        </div>

        <div class="info-section">
            <h3>Práctica Implementada</h3>
            <p>Implementación completa de pipeline CI/CD para microservicios con:</p>
            <ul class="feature-list">
                <li>GitHub Actions para automatización</li>
                <li>Azure Container Registry (ACR) para gestión de imágenes</li>
                <li>Azure Kubernetes Service (AKS) para orquestación</li>
                <li>Infraestructura como Código con Terraform</li>
                <li>Despliegue automatizado con verificaciones de salud</li>
            </ul>
        </div>

        <div class="tech-stack">
            <span class="tech-badge">Docker</span>
            <span class="tech-badge">GitHub Actions</span>
            <span class="tech-badge">Kubernetes</span>
            <span class="tech-badge">Azure AKS</span>
            <span class="tech-badge">Azure Container Registry</span>
            <span class="tech-badge">Terraform</span>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-value">{{ our_pods }}</span>
                <span class="stat-label">Nuestros Pods</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{{ running_pods }}</span>
                <span class="stat-label">Pods Activos</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{{ deployment_time }}</span>
                <span class="stat-label">Tiempo Activo</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{{ version }}</span>
                <span class="stat-label">Versión</span>
            </div>
        </div>

        <div class="footer">
            <div class="footer-grid">
                <div>
                    <strong>Desarrollado con DevOps Engineering</strong>
                    <br>Pipeline CI/CD
                </div>
                <div>
                    <strong>Fecha y Hora</strong>
                    <br>{{ current_time }}
                </div>
                <div>
                    <strong>Servidor</strong>
                    <br>{{ hostname }}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def get_kubernetes_client():
    """Configurar y retornar cliente de Kubernetes"""
    try:
        # Intentar carga in-cluster (cuando corre en K8s)
        config.load_incluster_config()
        app.logger.info("Configuración in-cluster cargada")
        return client.CoreV1Api()
    except Exception as e:
        app.logger.error(f"Error carga in-cluster: {e}")
        try:
            # Fallback a kubeconfig (desarrollo)
            config.load_kube_config()
            app.logger.info("Configuración kubeconfig cargada")
            return client.CoreV1Api()
        except Exception as e2:
            app.logger.error(f"Error carga kubeconfig: {e2}")
            return None

def get_dynamic_data():
    """Obtener datos dinámicos usando Kubernetes Client"""
    try:
        v1 = get_kubernetes_client()
        if not v1:
            return {
                "total_pods": "N/A",
                "running_pods": "N/A", 
                "our_pods": "N/A",
                "deployment_time": "N/A",
                "cluster_status": "No conectado",
                "status_class": "status-down"
            }
        
        # 1. Obtener todos los pods en todos los namespaces
        pods = v1.list_pod_for_all_namespaces(watch=False)
        total_pods = len(pods.items)
        running_pods = len([p for p in pods.items if p.status.phase == "Running"])
        
        # 2. Obtener nuestros pods específicos (en namespace default con label app)
        our_pods = 0
        deployment_time = "N/A"
        
        for pod in pods.items:
            # Contar nuestros pods
            if (pod.metadata.namespace == "default" and 
                pod.metadata.labels and 
                "app" in pod.metadata.labels and
                pod.status.phase == "Running"):
                our_pods += 1
            
            # Obtener tiempo del primer pod running
            if pod.status.phase == "Running" and pod.status.start_time:
                if deployment_time == "N/A":
                    start_time = pod.status.start_time.replace(tzinfo=None)
                    now = datetime.datetime.utcnow()
                    delta = now - start_time
                    minutes = int(delta.total_seconds() / 60)
                    if minutes < 60:
                        deployment_time = f"{minutes}m"
                    else:
                        hours = minutes // 60
                        deployment_time = f"{hours}h {minutes % 60}m"
        
        return {
            "total_pods": total_pods,
            "running_pods": running_pods,
            "our_pods": our_pods,
            "deployment_time": deployment_time,
            "cluster_status": "Conectado",
            "status_class": "status-up"
        }
        
    except Exception as e:
        app.logger.error(f"Error obteniendo datos: {e}")
        return {
            "total_pods": "Error",
            "running_pods": "Error",
            "our_pods": "Error", 
            "deployment_time": "Error",
            "cluster_status": f"Error: {str(e)}",
            "status_class": "status-down"
        }

def get_system_info():
    """Obtener información del sistema"""
    return {
        "hostname": socket.gethostname(),
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "2.2.0"
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
        cluster_status=dynamic_data["cluster_status"],
        status_class=dynamic_data["status_class"],
        hostname=system_info["hostname"]
    )

@app.route('/health')
def health():
    """Endpoint de health check"""
    return jsonify({
        "status": "healthy",
        "service": "api",
        "version": "2.2.0",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/info')
def api_info():
    """Endpoint API tradicional"""
    return jsonify({
        "service": "ci-cd-demo-api",
        "version": "2.2.0", 
        "status": "healthy",
        "description": "Demo de Pipeline CI/CD con AKS - Datos en Tiempo Real",
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)