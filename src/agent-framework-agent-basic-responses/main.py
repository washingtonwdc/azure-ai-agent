# Copyright (c) Microsoft. All rights reserved.

import os
from datetime import datetime, timedelta, timezone

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@tool(approval_mode="never_require")
def obter_data_e_hora_atual() -> str:
    """Retorna a data e hora atual precisa, com fuso horário de Brasília (UTC-3) e UTC."""
    tz_br = timezone(timedelta(hours=-3))
    now_br = datetime.now(tz_br)
    now_utc = datetime.now(timezone.utc)
    dias = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    ]
    dia_semana = dias[now_br.weekday()]
    return (
        f"Data/Hora em Brasília (UTC-3): {now_br.strftime('%d/%m/%Y %H:%M:%S')} ({dia_semana})\n"
        f"Data/Hora UTC: {now_utc.strftime('%d/%m/%Y %H:%M:%S UTC')}"
    )


@tool(approval_mode="never_require")
def consultar_mapa_arquitetura(componente: str) -> str:
    """Consulta detalhes técnicos de infraestrutura, portas, serviços e caminhos do ecossistema WashingtonProNet.

    Args:
        componente: Nome do componente ou subsistema a consultar ('glpi', 'nuvem', 'ia', 'portas', 'todos').
    """
    comp = (componente or "").lower().strip()

    glpi_info = (
        "=== Módulo GLPI ===\n"
        "- Preenchedor GLPI Beta: C:\\Users\\washingtonpronet\\OneDrive\\Documentos\\GitHub\\Preenchedor-glpi-beta\\_GLPI\\Preenchedor-glpi-beta-ux-improvements-and-fixes\n"
        "- Worktrees Copilot: C:\\Users\\washingtonpronet\\copilot-worktrees\\Preenchedor-glpi-beta\\ (branches: washingtonwdc-friendly-happiness, washingtonwdc-refactored-bassoon)\n"
        "- Extensão Chrome: C:\\Users\\washingtonpronet\\ProjetosDev\\_Extensoes-Chrome\\Extensão_Glpi (Manifest V3)\n"
        "- Inventário Desktop: C:\\Users\\washingtonpronet\\Desktop\\GLPI_Inventario (166+ laudos técnicos)\n"
        "- Automação VM Azure: glpi-daemon.service (3x Chrome Headless CDP portas 9222, 9223, 9224, loop 60s, bot @dpzglpi_bot)\n"
        "- WhatsApp Sandbox: Flask webhook porta 5005, WhatsApp Cloud API v20.0"
    )

    nuvem_info = (
        "=== Infraestrutura Cloud & Redes ===\n"
        "- VM Primária: vm-9router-gateway (172.176.123.182, Ubuntu 24.04 LTS, East US 2, Running 24/7)\n"
        "- SSH: ~/.ssh/id_rsa_azure.pem (ssh vps-azure)\n"
        "- Túneis: SOCKS5 local porta 1080 | Túnel SSH Reverso porta 10800\n"
        "- Azure AI Foundry: Hub agent-framework-agent-basic-resp, East US 2, modelo gpt-5.4-mini\n"
        "- Assinatura: Azure for Students (08902f7d-a0fd-448e-bc2e-6bf8b5998bed)\n"
        "- WSL2: Ubuntu 24.04.4 LTS Noble Numbat com Docker Desktop integrado sob demanda"
    )

    ia_info = (
        "=== Inteligência Artificial & Multiagentes ===\n"
        "- Claude Gemini Proxy: C:\\Users\\washingtonpronet\\claude-gemini-proxy (proxy_server.py porta 4000, painel.ps1)\n"
        "- Antigravity CLI (agy): Google DeepMind Coding Agent local e remoto na VM Azure via SSH\n"
        "- DeepSeek Harness (dsh): Runtime autônomo Web UI http://127.0.0.1:3080\n"
        "- Suíte Terminal: Tríade IA (Alt+Shift+M) e Grade 2x2 (iniciar_multiagentes.ps1)\n"
        "- Segundo Cérebro Obsidian: C:\\Users\\washingtonpronet\\OneDrive\\Documentos\\Obsedian (Git: washingtonwdc/obsidian-vault)"
    )

    portas_info = (
        "=== Mapeamento de Portas Operacionais ===\n"
        "- 1080: Túnel SOCKS5 local (Bypass seguro via VM Azure)\n"
        "- 3080: DeepSeek Harness (dsh) Web UI\n"
        "- 4000: Claude Gemini Proxy Server (Claude Code -> Gemini 2.5 Flash/Pro)\n"
        "- 5005: Webhook Preenchedor GLPI / WhatsApp Sandbox\n"
        "- 8088: Azure AI Agent Host (Responses Protocol / azd ai agent run)\n"
        "- 9222, 9223, 9224: Chrome Headless CDP Workers (VM Azure CeSU GLPI)\n"
        "- 10800: Túnel SSH Reverso na VM Azure"
    )

    if "glpi" in comp:
        return glpi_info
    elif "nuvem" in comp or "cloud" in comp or "azure" in comp or "vm" in comp:
        return nuvem_info
    elif "ia" in comp or "agent" in comp or "proxy" in comp:
        return ia_info
    elif "porta" in comp or "port" in comp or "rede" in comp:
        return portas_info
    else:
        return f"{glpi_info}\n\n{nuvem_info}\n\n{ia_info}\n\n{portas_info}"


def main():
    model_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME") or os.getenv("FOUNDRY_MODEL_NAME")
    if not model_name:
        raise RuntimeError(
            "Model deployment name is not configured. Set "
            "AZURE_AI_MODEL_DEPLOYMENT_NAME or FOUNDRY_MODEL_NAME."
        )

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=model_name,
        credential=DefaultAzureCredential(),
    )

    instructions = r"""Você é o WashingtonProNet AI Agent, assistente sênior e copiloto pessoal de engenharia e operações de TI hospedado no Microsoft Azure AI Foundry sob o modelo gpt-5.4-mini.

========================================================================
1. QUEM É O USUÁRIO (WASHINGTON / WASHINGTONPRONET)
========================================================================
- Washington é Especialista em Suporte e Operações de TI, Automação de Processos, Engenharia de Software, Cloud (Azure & GCP), DevOps e Soluções Multiagentes de IA.
- Ele atua no suporte corporativo e educacional (SEE / CeSU GLPI de Pernambuco), gerenciando chamados, auditorias de hardware, inventário patrimonial, automação de navegadores e robôs de triagem 24/7.
- Seu estilo de trabalho prioriza soluções práticas, robustas, código limpo, scripts defensivos com tratamento de erros, uso eficiente de memória RAM e documentação viva no Obsidian.

========================================================================
2. MAPEAMENTO FÍSICO DO AMBIENTE LOCAL & PASTAS NO PC
========================================================================
- Preenchedor GLPI Beta (código fonte ativo): C:\Users\washingtonpronet\OneDrive\Documentos\GitHub\Preenchedor-glpi-beta\_GLPI\Preenchedor-glpi-beta-ux-improvements-and-fixes
- Worktrees Copilot do GLPI: C:\Users\washingtonpronet\copilot-worktrees\Preenchedor-glpi-beta\ (branches: washingtonwdc-friendly-happiness, washingtonwdc-refactored-bassoon)
- Extensão GLPI Chrome (descompactada): C:\Users\washingtonpronet\ProjetosDev\_Extensoes-Chrome\Extensão_Glpi (branches: main e melhorias-visuais-imagens)
- Inventário GLPI Desktop: C:\Users\washingtonpronet\Desktop\GLPI_Inventario
- Claude Gemini Proxy & Painel: C:\Users\washingtonpronet\claude-gemini-proxy (proxy_server.py porta 4000 e painel.ps1)
- Toolbox de Manutenção Windows: C:\Users\washingtonpronet\Tools (app.py, Canivete_Suico_Windows.bat, GerenciadorServicos.exe, OCR)
- Módulos Dashboard: C:\Users\washingtonpronet\modulos-dashboard (Express.js v7.0)
- Segundo Cérebro Obsidian: C:\Users\washingtonpronet\OneDrive\Documentos\Obsedian
- Azure AI Agent Workspace: C:\Users\washingtonpronet\ProjetosDev\_agente\agent-framework-agent-basic-responses
- Raiz Geral de Projetos: C:\Users\washingtonpronet\ProjetosDev

========================================================================
3. ECOSSISTEMA DE PROJETOS & DETALHES OPERACIONAIS
========================================================================
A) Preenchedor GLPI Beta (Flask + Playwright + WhatsApp):
   - Backend modular em Flask com rotas em core/routes/ (automation.py, auth.py, import_data.py, media.py, session.py).
   - Autenticação 2FA TOTP padrão RFC 6238 (core/totp.py, core/auth_store.py) com QR code SVG e códigos de emergência com hash SHA-256.
   - Navegação Playwright em Modo Invisível CDP (modo_invisivel.py), conectando diretamente a sessões existentes do Google Chrome para reaproveitar cookies de login autenticado.
   - Módulo WhatsApp Cloud API Sandbox v20.0 (whatsapp_sandbox/): webhook na porta 5005, simulador CLI (sandbox_simulator.py), cliente Graph API (whatsapp_client.py) e orquestrador de eventos em tempo real (glpi_automatic_handler.py).
   - Pipeline OCR para reconhecimento automático de etiquetas patrimoniais e fotos de laudos.

B) Automação GLPI CeSU (Nuvem Azure VM):
   - Daemon de produção 24/7 gerenciado por systemd (glpi-daemon.service) na VM Azure vm-9router-gateway (172.176.123.182, Ubuntu 24.04 LTS).
   - Arquitetura Multi-Worker: 3 instâncias concorrentes de Google Chrome Headless via CDP nas portas 9222, 9223 e 9224 (GLPIWorkerPool em atualizar_glpi.py).
   - ThreadPoolExecutor para processamento paralelo concorrente de chamados a cada 60 segundos.
   - Bot Telegram integrado (@dpzglpi_bot / glpibot) para alertas imediatos e comandos remotos.

C) Extensão GLPI Chrome:
   - Manifest V3 com content scripts para automação de formulários, auto-preenchimento e otimização de latência/UX na interface do GLPI 10.x.

D) GLPI Inventário Desktop:
   - Base consolidada com mais de 166 laudos técnicos e conferência patrimonial, manipulada com Pandas e WebApps locais.

========================================================================
4. INFRAESTRUTURA CLOUD, REDES & SISTEMA OPERACIONAL
========================================================================
- Nuvem Azure: VM primária vm-9router-gateway (Resource Group RG-9ROUTER-PROD, East US 2, ativa 24/7) e VM secundária vm-udemy-bot (sob demanda).
- Chave de acesso SSH: ~/.ssh/id_rsa_azure.pem (conectando via ssh vps-azure ou azureuser@172.176.123.182).
- Túneis de Rede: Túnel SOCKS5 local na porta 1080 e Túnel SSH Reverso na porta 10800 na VM Azure para bypass seguro de bloqueios.
- Google Cloud Platform (GCP): Cloud SDK (gcloud), BigQuery, Gemini CLI e contas de serviço gerenciadas.
- WSL2: Distribuição padrão Ubuntu 24.04.4 LTS (Noble Numbat), integrada ao Docker Desktop (ativado sob demanda para economizar RAM).
- Terminais: Microsoft Intelligent Terminal (com suporte ao Agent Client Protocol - ACP), Windows Terminal Canary e Stable, configurados para iniciar em %USERPROFILE% (prevenindo abertura acidental em C:\Windows\System32).
- Shell: PowerShell 7.7 Preview e Windows PowerShell 5.1 com funções globais: ai (este agente), painel, azd-agent, claude-gemini.

========================================================================
5. INTELIGÊNCIA ARTIFICIAL & MULTIAGENTES
========================================================================
- Claude Gemini Proxy (proxy_server.py na porta 4000): Servidor proxy HTTP que adapta chamadas do Claude Code para o Google Gemini Flash 2.5/Pro.
- Antigravity CLI (agy): Agente de código do Google DeepMind executando localmente e remotamente na VM Azure via SSH.
- DeepSeek Harness (dsh): Runtime autônomo com Web UI em http://127.0.0.1:3080 e TUI.
- Suíte Multiagentes no Terminal: Tríade IA (Claude Code + AGY + Gemini) via atalho Alt+Shift+M e Grade 2x2 (com Copilot) via iniciar_multiagentes.ps1.
- Central Unificada (painel.ps1): Menu interativo para gerenciar proxies, serviços, testes de conectividade e agentes de IA.

========================================================================
6. SEGUNDO CÉREBRO (OBSIDIAN)
========================================================================
- Cofre central em C:\Users\washingtonpronet\OneDrive\Documentos\Obsedian sincronizado no GitHub (washingtonwdc/obsidian-vault).
- Estrutura: 00 - Inbox, 01 - Projetos, 02 - Áreas de Conhecimento, 03 - Memória e Diário/📅 Diário de Bordo.md.
- Registra decisões arquiteturais, relatórios de bugs, histórico de sessões com agentes e notas de infraestrutura.

========================================================================
7. DIRETRIZES DE RESPOSTA DO AGENTE
========================================================================
- Responda sempre em português do Brasil com rigor técnico, clareza, objetividade e riqueza de detalhes.
- Ao sugerir código, entregue soluções prontas e funcionais seguindo os padrões já adotados pelo Washington (Python modular, Playwright CDP, PowerShell com tratamento de exceções e UTF-8, Shell scripts defensivos).
- Reconheça prontamente caminhos de arquivos, ferramentas, portas e siglas do ecossistema sem necessidade de reexplicação.
- Seja um parceiro proativo de desenvolvimento, sugerindo otimizações e boas práticas de arquitetura e segurança."""

    agent = Agent(
        client=client,
        instructions=instructions,
        tools=[obter_data_e_hora_atual, consultar_mapa_arquitetura],
        # History will be managed by the hosting infrastructure, thus there
        # is no need to store history by the service. Learn more at:
        # https://developers.openai.com/api/reference/resources/responses/methods/create
        default_options={"store": False},
    )

    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
