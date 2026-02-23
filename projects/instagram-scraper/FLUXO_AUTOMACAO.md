# 🤖 Fluxo de Automação: Screenshots → Supabase → CRM

## Objetivo
Criar um sub-agente reutilizável que automatiza o processo completo de captura, sincronização e análise de novos seguidores do Instagram.

## Arquitetura do Fluxo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. CAPTURA DE SCREENSHOTS                                   │
│    - Browser conectado ao Instagram                         │
│    - Busca por @username                                    │
│    - Tira print em viewport mobile (375x667)               │
│    - Salva em ~/Documents/Seguidores/                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. SINCRONIZAÇÃO SUPABASE                                   │
│    - Conecta ao Supabase                                    │
│    - Checa se @username já existe na tabela                │
│    - Se não existir: INSERT com status "print_pendente"    │
│    - Se existir: Verifica status atual                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. UPLOAD NO CRM (PIX PROSPECTOR)                          │
│    - Navega para https://pix-prospector-bot.lovable.app/   │
│    - Clica em "Nova Análise"                               │
│    - Arrasta screenshot no campo "arraste um screenshot"   │
│    - Digita @ no campo "@usuario"                          │
│    - Clica em "analisar"                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. ATUALIZAÇÃO FINAL NO SUPABASE                            │
│    - Marca status como "analise_feita"                      │
│    - Registra timestamp da análise                          │
│    - Sincroniza com o CRM                                   │
└─────────────────────────────────────────────────────────────┘
```

## Banco de Dados (Supabase)

**Tabela:** `instagram_followers`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | bigint | Primary key |
| username | text | @username (unique) |
| status | text | `novo` \| `print_tirado` \| `analise_feita` \| `respondeu` |
| file_path | text | Caminho do screenshot |
| added_at | timestamp | Quando foi adicionado |
| print_at | timestamp | Quando o print foi tirado |
| analysis_at | timestamp | Quando foi analisado no CRM |
| created_at | timestamp | Auto |
| updated_at | timestamp | Auto |

## Sub-Agente: Como Chamar

```bash
# Chamar o sub-agente
sessions_spawn --task "Executar fluxo completo de análise de novos seguidores" \
              --label "instagram-crm-automation" \
              --runTimeoutSeconds 900
```

## Passo a Passo do Sub-Agente

### 1️⃣ **Listar screenshots na pasta**
```python
import os
screenshots = [f for f in os.listdir("~/Documents/Seguidores") if f.endswith(".png")]
```

### 2️⃣ **Para cada screenshot:**

a. **Extrair @username do nome do arquivo**
```python
# Formato: @username_YYYYMMDD_HHMMSS.png
username = filename.split("_")[0].replace("@", "")
```

b. **Checar no Supabase se já existe**
```python
response = supabase.table("instagram_followers") \
    .select("status") \
    .eq("username", username) \
    .execute()
```

c. **Se não existe: INSERT**
```python
supabase.table("instagram_followers").insert({
    "username": username,
    "status": "novo",
    "file_path": screenshot_path,
    "added_at": datetime.now().isoformat()
}).execute()
```

d. **Se status != "analise_feita": Fazer análise no CRM**
   - Acessar `https://pix-prospector-bot.lovable.app/`
   - Clicar em "Nova Análise"
   - Arrastar arquivo no drop zone
   - Digitar @ no campo "@usuario"
   - Clicar "analisar"

e. **Após análise: Atualizar Supabase**
```python
supabase.table("instagram_followers").update({
    "status": "analise_feita",
    "analysis_at": datetime.now().isoformat()
}).eq("username", username).execute()
```

### 3️⃣ **Documentação e Log**
- Salvar resultado em `projects/instagram-scraper/analysis_log.md`
- Registrar quantos foram novos, atualizados, já feitos

## Credenciais (Já Configuradas)

**Supabase:**
- URL: `https://sfqsghgogwtxwzthscvw.supabase.co`
- Service Key: (armazenado com segurança)

**Instagram:**
- Login: `alfredharvey1806@gmail.com`
- (Usar browser Chrome já logado)

**CRM (Pix Prospector):**
- Login: `alfredharvey1806@gmail.com`
- Senha: `Sucesso$$2026$$`
- (Usar browser Chrome já logado)

## Status de Implementação

- [x] Screenshots capturados (15 perfis)
- [x] Supabase conectado e testado
- [x] CRM acessível
- [ ] Sub-agente automático criado
- [ ] Integração completa testada
- [ ] Documentação finalizada

## Próximos Passos

1. Criar handler Python que o sub-agente vai executar
2. Testar com 2-3 perfis primeiro
3. Escalar para todo o lote de 15
4. Parametrizar pra ser reutilizável (chamar sempre que houver novo seguidor)
