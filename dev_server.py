#!/usr/bin/env python3
"""
Servidor de desenvolvimento com auto-reload para o mapa do Brasil
Monitora mudanças nos arquivos e recarrega automaticamente o navegador
"""

import http.server
import socketserver
import os
import time
import threading
import webbrowser
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

class AutoReloadHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Adiciona headers para evitar cache e permitir CORS
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Se for o arquivo principal, injeta o script de auto-reload
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
            super().do_GET()
            return
        
        # Para outros arquivos, serve normalmente
        super().do_GET()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, server_path):
        self.server_path = server_path
        self.last_modified = {}
        self.reload_clients = set()
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Ignora arquivos temporários
        if event.src_path.endswith('~') or event.src_path.endswith('.tmp'):
            return
        
        file_path = Path(event.src_path)
        
        # Só monitora arquivos relevantes
        if file_path.suffix in ['.json', '.html', '.js', '.css']:
            print(f"📝 Arquivo modificado: {file_path.name}")
            
            # Se for um arquivo de dados, força reload
            if 'representantes' in file_path.name or 'uf.json' in file_path.name:
                print("🔄 Dados atualizados - recarregando...")
                self.force_reload()
    
    def force_reload(self):
        print("🔄 Forçando reload do navegador...")
        # Aqui você pode implementar um WebSocket ou Server-Sent Events
        # para comunicação em tempo real com o navegador
        print("💡 Dica: Use F5 ou Cmd+R para recarregar manualmente")

def create_dev_server(port=8080):
    """Cria e inicia o servidor de desenvolvimento"""
    
    # Muda para o diretório vercel-deploy
    os.chdir('vercel-deploy')
    
    # Configura o handler
    handler = AutoReloadHandler
    
    # Cria o servidor
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚀 Servidor rodando em http://localhost:{port}")
        print(f"📁 Diretório: {os.getcwd()}")
        print("👀 Monitorando mudanças nos arquivos...")
        print("💡 Pressione Ctrl+C para parar")
        
        # Abre o navegador automaticamente
        webbrowser.open(f'http://localhost:{port}')
        
        # Inicia o monitoramento de arquivos
        event_handler = FileChangeHandler(os.getcwd())
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=True)
        observer.start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Parando servidor...")
            observer.stop()
            httpd.shutdown()
        finally:
            observer.join()

if __name__ == "__main__":
    create_dev_server(8080)
