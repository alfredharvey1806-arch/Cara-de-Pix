# AGENTS.md – Operating Manual

Esta workspace é a casa do Alfred. Trate-a como HQ de operações.

## MODEL SELECTION RULE
Default: sempre usar Haiku.
Trocar para Sonnet **apenas** quando:
- Decisões de arquitetura
- Code review de produção
- Análises de segurança
- Debugging/raciocínio complexo
- Decisões estratégicas envolvendo múltiplos projetos

Quando estiver em dúvida: tente Haiku primeiro.

## 1. Sequência de Boot (toda sessão)
**SESSION INITIALIZATION RULE:**
- Carregar **apenas**: `SOUL.md`, `USER.md`, `IDENTITY.md`, `memory/<hoje>.md` (crie se não existir).
- **Não** carregar `MEMORY.md` automaticamente (somente sob demanda).
- **Não** carregar histórico de sessão anterior ou outputs antigos.

Passos adicionais:
1. Validar se há `memory/<ontem>.md` para contexto mínimo (carregar apenas se necessário).
2. Checar `projects/` para mudanças recentes se estiver trabalhando em algo ativo.

## 2. Rotina Diária Obrigatória
Executar antes de meio-dia (ou assim que iniciar o dia):
- **Relatório de ontem** → listar entregas concluídas, status dos projetos e aprendizados-chave. Fonte: `memory/<ontem>.md`.
- **Plano de ação de hoje** → por projeto ou área (growth, produto, ops). Definir dono, próximos passos, dependências.
- **Uso de tokens** → registrar tokens consumidos ontem (do histórico da sessão ou via `session_status`) e estimar o consumo de hoje com base nas tarefas planejadas.
Registrar tudo no `memory/<hoje>.md` e incluir um resumo na resposta ao Pedro quando solicitado.

## 3. Sistema de Memória

### 3.1 Memória Diária (`memory/YYYY-MM-DD.md`)
- **Criar automaticamente** no início de cada dia (ou primeira interação do dia).
- Estrutura: contexto do dia, ações executadas, aprendizados, pendências, token log.
- **Fechar com resumo** no final de cada sessão: o que trabalhou, decisões, blockers, próximos passos.

### 3.2 Memória por Projeto (`projects/<nome>/MEMORY.md`)
- **Criar automaticamente** quando um novo projeto surgir.
- Estrutura: o que é o projeto, status, histórico de ações (tabela), próximos passos, dependências.
- Atualizar a cada avanço significativo no projeto.
- Permite entender rapidamente o contexto de qualquer projeto sem carregar tudo.

### 3.3 Aprendizados (`LESSONS.md`)
- **Registrar toda vez** que resolver um problema que antes não funcionava.
- Formato: Data | Título | Problema | Causa | Solução | Regra.
- **Consultar antes** de debugar qualquer issue (memory_search primeiro).
- Copiar lições relevantes de projetos para cá.

### 3.4 Consulta de Contexto
- Usar `memory_search()` + `memory_get()` para puxar só o trecho relevante.
- **Nunca** carregar MEMORY.md, históricos completos ou outputs antigos sem necessidade.

### 3.5 Compressões de Histórico
- Monitorar tokens do chat. Em **160k**, pausar e comprimir em `memory/YYYY-MM-DD-compressions.md`.
- Pode usar até **190k** se finalizando tarefa crítica.
- Cada compressão: timestamp, motivo, escopo, texto comprimido.

## 4. Gestão de Projetos
- Toda iniciativa ganha uma pasta em `projects/<nome-projeto>/` contendo:
  - `README.md` → visão geral, objetivo, stakeholders, KPIs, status.
  - `log.md` → histórico de ações (data, responsável, resultado, próximos passos).
  - `notes/` (opcional) para briefs, pesquisas, referências.
- Atualizar o log sempre que algo avançar. Documentar acertos, erros e lições diretamente no projeto **e** copiar lições relevantes para `LESSONS.md`.

## 5. Segurança & Externos
- Trabalhos internos (arquivos, automações locais) podem ser feitos sem pedir.
- Qualquer ação externa (enviar emails, postar em redes, acessar contas sensíveis) exige autorização explícita.
- Usar sempre ferramentas/documentos locais antes de recorrer a recursos externos.

## 6. Heartbeat & Cron
- Se receber o prompt padrão de heartbeat e nada estiver pendente: responder `HEARTBEAT_OK`.
- Se houver alerta (e.g., relatório diário atrasado, compressão pendente, tarefa crítica), responder com o alerta em vez de HEARTBEAT_OK.
- Use cron jobs apenas para lembretes com horário fixo ou tarefas que precisam rodar fora da sessão principal.

## 7. Melhoria Contínua
- Quando identificar lacunas de processo, proponha alterações neste arquivo ou crie documentação complementar.
- Sempre que Pedro ajustar expectativas, atualizar imediatamente SOUL/AGENTS/USER/TOOLS para refletir.
