from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"commands": {}, "buttons": []}

def save_config(config):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@app.route('/api/command', methods=['POST'])
def add_command():
    data = request.json
    config = load_config()
    config['commands'][data['name']] = data['response']
    save_config(config)
    return jsonify({"status": "success"})

@app.route('/api/command/<name>', methods=['DELETE'])
def delete_command(name):
    config = load_config()
    if name in config['commands']:
        del config['commands'][name]
        save_config(config)
    return jsonify({"status": "success"})

@app.route('/api/button', methods=['POST'])
def add_button():
    data = request.json
    config = load_config()
    config['buttons'].append(data)
    save_config(config)
    return jsonify({"status": "success"})

@app.route('/api/button/<int:index>', methods=['DELETE'])
def delete_button(index):
    config = load_config()
    if 0 <= index < len(config['buttons']):
        del config['buttons'][index]
        save_config(config)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
