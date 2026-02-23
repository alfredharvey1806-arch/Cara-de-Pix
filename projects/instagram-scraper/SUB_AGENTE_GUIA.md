# 🤖 Sub-Agente: Automação de Análises Instagram → CRM

## O que Faz?

Automação **completa e reutilizável** que:

1. ✅ Lista todos os screenshots capturados em `~/Documents/Seguidores/`
2. ✅ Sincroniza com Supabase (checa se @username já existe)
3. ✅ Insere novos registros ou atualiza existentes
4. ✅ Gera log de todas as operações
5. ✅ Fica pronto para o upload no CRM

## Como Chamar o Sub-Agente

### Opção 1: Command Line
```bash
openclaw sessions_spawn \
  --task "Executar automação completa de screenshots → Supabase: listar todos os prints em ~/Documents/Seguidores/, sincronizar com Supabase checando se @username já existe, inserir novos registros, atualizar existentes, gerar log final" \
  --label "instagram-automation-sync" \
  --runTimeoutSeconds 600
```

### Opção 2: Via Chat (ao chamar Alfred)
```
"Rodar automação de Instagram: sincronizar screenshots com Supabase"
```

## Fluxo Passo a Passo

### PASSO 1: Listar Screenshots
```
📸 ~/Documents/Seguidores/
├── @ju_bettiol_20260222_155600.png
├── @_manuteles_20260222_155601.png
├── @beredela_20260222_155602.png
└── ...15 perfis no total
```

### PASSO 2: Sincronizar com Supabase
Para cada screenshot:
```
@username_TIMESTAMP.png
    ↓
[Extrai @username]
    ↓
[Checa se existe no Supabase]
    ↓
    ├─ Existe? → Verifica status
    │   ├─ "esperando" → Marca como "print feito"
    │   └─ "print feito" → Já foi processado ✅
    │
    └─ Não existe? → INSERT novo registro
        └─ status: "print feito"
```

### PASSO 3: Atualizar Supabase
```sql
UPDATE instagram_followers
SET status = 'print feito'
WHERE username = @username
```

### PASSO 4: Gerar Log
```
📄 /projects/instagram-scraper/analysis_log.md
```

## Banco de Dados (Supabase)

**Tabela:** `instagram_followers`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | bigint | Primary key |
| username | text | @username (unique) |
| status | text | `esperando` \| `print feito` |
| file_path | text | Caminho do screenshot |
| added_at | timestamp | Quando foi adicionado |
| print_at | timestamp | Quando o print foi tirado |
| created_at | timestamp | Auto (Supabase) |
| updated_at | timestamp | Auto (Supabase) |

## Status do Fluxo

- ✅ **Parte 1:** Screenshots capturados (15 perfis)
- ✅ **Parte 2:** Sub-agente pronto (automation_handler.py)
- 🔄 **Parte 3:** Sincronização Supabase (testando)
- ⏳ **Parte 4:** Upload no CRM (próximo passo)

## Próximas Fases (Não Automático Ainda)

Após o sub-agente sincronizar com Supabase:

1. **Abrir site:** https://pix-prospector-bot.lovable.app/
2. **Clicar "Nova Análise"**
3. **Arrastar screenshot** no campo
4. **Digitar @usuario**
5. **Clicar "analisar"**
6. **Marcar status como "análise_feita" no Supabase**

> Essa última parte será automatizada em breve no sub-agente

## Troubleshooting

### ❌ Erro: `instagram_followers_status_check`
**Causa:** Status inválido enviado ao Supabase
**Solução:** Usar apenas `"esperando"` ou `"print feito"`

### ❌ Erro: `Username já existe`
**Causa:** Tentou INSERT de username duplicado
**Solução:** O handler já checa isso, ignore

### ❌ Erro: `Pasta não encontrada`
**Solução:** Criar `~/Documents/Seguidores/` manualmente

## Exemplos de Uso

### Exemplo 1: Primeira Execução
```bash
# Chama sub-agente
sessions_spawn "Sincronizar screenshots com Supabase"

# Resultado esperado:
# ✅ 15 screenshots encontrados
# ✅ 15 registros sincronizados
# ✅ Log gerado
```

### Exemplo 2: Novos Screenshots Adicionados
```bash
# Chama sub-agente novamente
sessions_spawn "Sincronizar screenshots com Supabase"

# Resultado esperado:
# ✅ 27 screenshots encontrados (12 novos)
# ✅ 12 novos registros criados
# ✅ Log atualizado
```

## Integração Futura

Quando o CRM (Pix Prospector) for automatizado no sub-agente:

```
Sub-Agente Full Loop:
1. Lista screenshots
2. Sincroniza Supabase
3. Abre site CRM
4. Faz upload de cada print
5. Marca análise_feita no Supabase
6. Gera relatório final
```

## Contato / Melhorias

Se encontrar problemas ou quiser melhorias:
- Log completo em: `projects/instagram-scraper/analysis_log.md`
- Handler em: `projects/instagram-scraper/automation_handler.py`
- Documentação em: `projects/instagram-scraper/FLUXO_AUTOMACAO.md`
