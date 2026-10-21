import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import datetime
import os


class ArpScanner:
    """Responsável por executar comandos de rede e extrair os dados."""

    @staticmethod
    def get_arp_table():
        try:
            # Especifica a codificação cp850 (padrão do CMD em português) e ignora erros de parsing
            result = subprocess.run(['arp', '-a'], capture_output=True, encoding='cp850', errors='ignore', check=True)
            return ArpScanner._parse_output(result.stdout)
        except Exception as e:
            print(f"Erro ao escanear rede: {e}")
            return []

    @staticmethod
    def _parse_output(output):
        devices = []
        # Regex básico para extrair IP e MAC. Funciona na maioria dos retornos do Windows/Linux
        pattern = re.compile(r'((?:[0-9]{1,3}\.){3}[0-9]{1,3})\s+([0-9A-Fa-f\-:]+)\s+(\w+)')

        for line in output.split('\n'):
            match = pattern.search(line)
            if match:
                ip, mac, tipo = match.groups()
                # Ignorar IPs de broadcast comuns
                if ip not in ['255.255.255.255', '224.0.0.22']:
                    devices.append({'ip': ip, 'mac': mac, 'tipo': tipo})
        return devices


class ReportGenerator:
    """Responsável pela criação de relatórios executivos."""

    @staticmethod
    def generate_executive_report(device_data):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"Relatorio_Executivo_{device_data['ip'].replace('.', '_')}.txt"

        report_content = (
            f"====================================================\n"
            f"           RELATÓRIO EXECUTIVO DE ATIVO             \n"
            f"====================================================\n\n"
            f"Data da Análise : {timestamp}\n"
            f"Endereço IP     : {device_data['ip']}\n"
            f"Endereço MAC    : {device_data['mac'].upper()}\n"
            f"Tipo de Alocação: {device_data['tipo'].capitalize()}\n\n"
            f"Status do Ativo : Detectado ativo na rede local via\n"
            f"                  tabela ARP do host de monitoramento.\n\n"
            f"====================================================\n"
        )

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return filename, report_content


class MinimalistScannerApp:
    """Interface Gráfica Minimalista para o Scanner."""

    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Rede Minimalista")
        self.root.geometry("600x400")
        self.root.configure(bg="#f4f4f9")

        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        # Estilo minimalista
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#333333", rowheight=30)
        style.configure("Treeview.Heading", background="#e0e0e0", foreground="#000000", font=('Segoe UI', 10, 'bold'))

        # Título
        header = tk.Label(self.root, text="Ativos na Rede Local", font=('Segoe UI', 16), bg="#f4f4f9", fg="#333333")
        header.pack(pady=10)

        # Tabela (Treeview)
        columns = ('ip', 'mac', 'tipo')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading('ip', text='Endereço IP')
        self.tree.heading('mac', text='Endereço MAC')
        self.tree.heading('tipo', text='Tipo')

        self.tree.column('ip', anchor=tk.CENTER, width=150)
        self.tree.column('mac', anchor=tk.CENTER, width=200)
        self.tree.column('tipo', anchor=tk.CENTER, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Evento de clique
        self.tree.bind('<Double-1>', self.on_device_click)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Iniciando monitoramento...")
        status_bar = tk.Label(self.root, textvariable=self.status_var, font=('Segoe UI', 9), bg="#f4f4f9", fg="#666666",
                              anchor="w")
        status_bar.pack(fill=tk.X, padx=20, pady=5)

    def refresh_data(self):
        # Limpa tabela atual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Busca novos dados
        devices = ArpScanner.get_arp_table()

        # Preenche tabela
        for dev in devices:
            self.tree.insert('', tk.END, values=(dev['ip'], dev['mac'], dev['tipo']))

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"Última atualização: {timestamp}. Próxima em 60s.")

        # Agenda próxima execução para daqui a 60000ms (1 minuto)
        self.root.after(60000, self.refresh_data)

    def on_device_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_values = self.tree.item(selected_item[0])['values']
        device_data = {
            'ip': item_values[0],
            'mac': item_values[1],
            'tipo': item_values[2]
        }

        # Gera o relatório
        filename, content = ReportGenerator.generate_executive_report(device_data)

        # Mostra confirmação
        messagebox.showinfo(
            "Relatório Gerado",
            f"Relatório executivo salvo localmente como:\n{filename}\n\nResumo:\n{content}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = MinimalistScannerApp(root)
    root.mainloop()