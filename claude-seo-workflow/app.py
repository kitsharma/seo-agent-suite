"""
Claude SEO Workflow System - Main Application

Path: /app.py
Purpose: Entry point for the achievewith.ai SEO Workflow System that runs the web UI.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import os
import json
import uuid
import base64
from datetime import datetime

from claude_workflow_orchestrator import ClaudeSEOWorkflowOrchestrator

# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'achievewith-ai-seo-workflow-secret-key'

# Initialize orchestrator
orchestrator = ClaudeSEOWorkflowOrchestrator()

@app.route('/')
def index():
    """Render the main dashboard"""
    workflows = orchestrator.get_available_workflows()
    
    # Get recent results
    results = []
    results_dir = os.path.join(os.getcwd(), 'results')
    if os.path.exists(results_dir):
        result_files = sorted(
            [f for f in os.listdir(results_dir) if f.endswith('.json')],
            key=lambda x: os.path.getmtime(os.path.join(results_dir, x)),
            reverse=True
        )[:5]  # Get 5 most recent results
        
        for result_file in result_files:
            try:
                with open(os.path.join(results_dir, result_file), 'r') as f:
                    result_data = json.load(f)
                    
                result_id = os.path.splitext(result_file)[0]
                timestamp = datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(results_dir, result_file))
                ).strftime('%Y-%m-%d %H:%M:%S')
                
                results.append({
                    'id': result_id,
                    'workflow_type': result_data.get('workflow_type', 'Unknown'),
                    'timestamp': timestamp,
                    'steps': len(result_data.get('execution_summary', {}).get('execution_log', []))
                })
            except Exception as e:
                print(f"Error loading result file {result_file}: {str(e)}")
    
    return render_template('index.html', workflows=workflows, results=results)

@app.route('/workflow/<workflow_type>')
def workflow_config(workflow_type):
    """Render the workflow configuration page"""
    workflows = orchestrator.get_available_workflows()
    
    if workflow_type == 'custom':
        workflow_description = "Build your own workflow by combining specialized agents."
        agents = orchestrator.get_agent_descriptions()
    else:
        if workflow_type not in workflows:
            return redirect(url_for('index'))
            
        workflow_description = workflows[workflow_type]
        agents = {}
    
    return render_template(
        'workflow_config.html',
        workflow_type=workflow_type,
        workflow_description=workflow_description,
        agents=agents
    )

@app.route('/start_workflow', methods=['POST'])
def start_workflow():
    """Start a workflow with the provided configuration"""
    data = request.json
    workflow_type = data.get('workflow_type')
    workflow_data = data.get('data', {})
    
    if workflow_type == 'custom':
        steps = data.get('steps', [])
        if not steps:
            return jsonify({'error': 'No steps selected for custom workflow'}), 400
            
        try:
            result = orchestrator.run_custom_workflow(steps, workflow_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        try:
            result = orchestrator.run_workflow(workflow_type, workflow_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Generate a unique ID for the result
    result_id = str(uuid.uuid4())
    
    # Save the result
    results_dir = os.path.join(os.getcwd(), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    with open(os.path.join(results_dir, f"{result_id}.json"), 'w') as f:
        json.dump(result, f, indent=2)
    
    return jsonify({'success': True, 'result_id': result_id})

@app.route('/results/<result_id>')
def view_result(result_id):
    """Render the result view page"""
    result_file = os.path.join(os.getcwd(), 'results', f"{result_id}.json")
    
    if not os.path.exists(result_file):
        return redirect(url_for('index'))
    
    with open(result_file, 'r') as f:
        result = json.load(f)
    
    return render_template('result_view.html', result=result, result_id=result_id)

@app.route('/download/<result_id>')
def download_result(result_id):
    """Download the result as a JSON file"""
    result_file = os.path.join(os.getcwd(), 'results', f"{result_id}.json")
    
    if not os.path.exists(result_file):
        return redirect(url_for('index'))
    
    return send_file(result_file, as_attachment=True, download_name=f"{result_id}.json")

def create_placeholder_logo():
    """Create a placeholder logo if it doesn't exist"""
    img_dir = os.path.join(app.static_folder, 'img')
    os.makedirs(img_dir, exist_ok=True)
    
    logo_path = os.path.join(img_dir, 'logo.png')
    
    if not os.path.exists(logo_path):
        # Simple teal circle as a placeholder
        with open(logo_path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00\x18tEXtSoftware\x00paint.net 4.0.5e\xe7\xb8\x92\x00\x00\x03\xd2IDATx^\xed\xdd\xb1\x8d\xdc@\x10\x05Q\x15\x13\x13\x96\x9e,\xf7\xa8i`\xc7:\x81\xeezuE\xf0\x15j\tC\x04\xbb\xcf\xffUZ;\xe5\x83\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"G\x14\xf2|\xf3\xbb\xbf\xed\xfd\xcd\xaf\xb0G\x14\xf2\xf5\xcdO\xe0\x10\x12\x83\x10\x12\x83\x10\x12\x83\xbc\x15\xf2\xfa?\x06\xf8\x82H\x0e!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06!$\x06\x89\xff\x8b]\xf81e\xf5\xe5\xcdO\xc1\xf1\xfa\xe6\xff\x11\x1d\x82x$=\xc6\xfd;B"\x89\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8!$r\x08\x89\x1cB"\x87\x90\xc8y~\x7f\x01\xbd\xbd\xfa\xf9\xad\xb7\xf6\xec\x00\x00\x00\x00IEND\xaeB`\x82')

if __name__ == '__main__':
    # Create directories and logo
    create_placeholder_logo()
    
    print("Starting achievewith.ai SEO Workflow System...")
    print("Access the web interface at http://127.0.0.1:8082")
    app.run(debug=True, host='127.0.0.1', port=8082)
