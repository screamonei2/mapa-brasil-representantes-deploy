#!/usr/bin/env python3
"""
Servidor simples com monitoramento de arquivos para desenvolvimento
Usa apenas Python padrão - sem dependências externas
"""

import http.server
import socketserver
import os
import time
import threading
import webbrowser
from pathlib import Path
import json

class DevServerHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Headers para evitar cache
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

class FileWatcher:
    def __init__(self, directory, callback):
        self.directory = directory
        self.callback = callback
        self.running = False
        self.last_modified = {}
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()
        print(f"👀 Monitorando mudanças em: {self.directory}")
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _watch_loop(self):
        while self.running:
            try:
                self._check_files()
                time.sleep(1)  # Verifica a cada segundo
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
    
    def _check_files(self):
        for file_path in Path(self.directory).rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.json', '.html', '.js', '.css']:
                current_mtime = file_path.stat().st_mtime
                last_mtime = self.last_modified.get(str(file_path), 0)
                
                if current_mtime > last_mtime:
                    self.last_modified[str(file_path)] = current_mtime
                    if last_mtime > 0:  # Não é a primeira verificação
                        self._file_changed(file_path)
    
    def _file_changed(self, file_path):
        filename = file_path.name
        print(f"📝 Arquivo modificado: {filename}")
        
        # Se for um arquivo de dados importante
        if 'representantes' in filename or 'uf.json' in filename:
            print("🔄 Dados atualizados!")
            print("💡 Use F5 ou Cmd+R para recarregar o navegador")
            self.callback(filename)

def create_dev_server(port=8080):
    """Cria e inicia o servidor de desenvolvimento com monitoramento"""
    
    # Muda para o diretório vercel-deploy
    os.chdir('vercel-deploy')
    
    def on_file_change(filename):
        print(f"🔄 Arquivo {filename} foi modificado - recarregue o navegador!")
    
    # Inicia o monitoramento de arquivos
    watcher = FileWatcher('.', on_file_change)
    watcher.start()
    
    # Configura o servidor
    handler = DevServerHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🚀 Servidor rodando em http://localhost:{port}")
            print(f"📁 Diretório: {os.getcwd()}")
            print("👀 Monitorando mudanças nos arquivos...")
            print("💡 Pressione Ctrl+C para parar")
            print("💡 O navegador será aberto automaticamente")
            
            # Abre o navegador
            webbrowser.open(f'http://localhost:{port}')
            
            # Inicia o servidor
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Parando servidor...")
        watcher.stop()
    except Exception as e:
        print(f"Erro: {e}")
        watcher.stop()

if __name__ == "__main__":
    create_dev_server(8080)
