# ScannerARP

Aplicação desktop simples para visualizar dispositivos presentes na tabela ARP do computador e gerar relatórios individuais em formato texto.

## Requisitos

- Python 3.8 ou superior
- Tkinter instalado
- Comando `arp` disponível no sistema operacional
- Permissão para consultar a tabela ARP local

No Windows, o Tkinter normalmente já acompanha a instalação padrão do Python. Em distribuições Linux, pode ser necessário instalar o pacote `python3-tk`.

## Execução

Na raiz do projeto, execute:

```bash
python scanner_arp.py
```

Uma janela será aberta com os endereços IP, endereços MAC e tipos de entrada encontrados.

## Funcionamento

1. Executa o comando `arp -a` no sistema local.
2. Extrai IP, MAC e tipo de cada entrada reconhecida.
3. Ignora os endereços `255.255.255.255` e `224.0.0.22`.
4. Atualiza a lista automaticamente a cada 60 segundos.
5. Gera um relatório ao clicar duas vezes em um dispositivo.

O relatório é salvo no diretório atual com o nome:

```text
Relatorio_Executivo_<ip>.txt
```

## Estrutura

- `scanner_arp.py`: interface gráfica, leitura da tabela ARP e geração de relatórios.
- `README.md`: documentação do projeto.

## Limitações

- A aplicação consulta somente a tabela ARP já existente no computador.
- Ela não realiza varredura ativa de portas ou descoberta completa da rede.
- O parser depende do formato retornado pelo comando `arp -a`.
- Erros durante a consulta são exibidos no terminal e resultam em uma lista vazia.