# 📋 Passo a Passo: Upload no CRM (Pix Prospector)

## Fluxo Testado Manualmente

### ✅ Passo 1: Login
```
URL: https://pix-prospector-bot.lovable.app/auth
Email: alfredharvey1806@gmail.com
Senha: Sucesso$$2026$$
→ Clica em "Entrar"
→ Acessa o CRM
```

### ✅ Passo 2: Nova Análise
```
Localiza: Botão "Nova Análise" no topo
→ Clica no botão
→ Abre formulário "/analisar"
```

### ✅ Passo 3: Formulário de Análise

**Campo 1: Screenshot do Perfil** (obrigatório)
- Label: "Screenshot do Perfil *"
- Input: Choose File button
- Aceita: PNG, JPG até 10MB
- Ação: Clicar para abrir file dialog ou arrastar arquivo
- **Path do arquivo:** `~/Documents/Seguidores/@username_YYYYMMDD_HHMMSS.png`

**Campo 2: Bio e Informações** (opcional)
- Label: "Bio e Informações do Perfil (opcional)"
- Placeholder: "Cole aqui a bio, nome, categoria, número de seguidores, link externo, etc."
- Ação: Preenchimento opcional
- **Dados disponíveis:** Pode vir de metadados do screenshot

**Campo 3: @ do Usuário** (obrigatório)
- Label: "@usuario ou usuario"
- Input: textbox
- Placeholder: "@usuario ou usuario"
- **Valor a digitar:** `@username` (extraído do filename)

**Campo 4: Botão Analisar**
- Status: Desabilitado até screenshot ser carregado
- Ação: Clicar para enviar análise

### ⏳ Passo 4: Validação
- ⚠️ Alerta: "Screenshot obrigatório para análise"
- Vai desaparecer assim que upload for bem-sucedido
- Botão "Analisar" fica habilitado

### 🎯 Passo 5: Análise
- Após clicar em "Analisar":
  - Sistema processa screenshot
  - GPT analisa perfil
  - Score de Pix é gerado (0-100)
  - Sequência de 7 dias criada
  - Lead é adicionado ao CRM

### ✅ Passo 6: Atualização Supabase
```sql
UPDATE instagram_followers
SET status = 'print feito'
WHERE username = @username;
```

---

## Mapeamento de IDs (refs) do Lovable

| Elemento | Ref | Tipo |
|----------|-----|------|
| Nova Análise (header) | e62 | Button |
| Choose File (screenshot) | e150 | File Input |
| Bio textbox | e161 | Textarea |
| @usuario field | e169 | Textbox |
| Botão Analisar | (dinâmico) | Button |
| Back button | e95 | Button |

---

## Estado do Teste

- ✅ Login bem-sucedido
- ✅ Navegação para formulário ok
- ⏳ Upload de arquivo (precisa refinamento)
- ⏳ Preenchimento de campos (pronto pra implementar)
- ⏳ Click em "Analisar" (pronto)
- ⏳ Atualização Supabase (pronto)

---

## Próximas Ações

1. **Refinar upload:** Testar com diferentes métodos de upload
2. **Automatizar campos:** Extrair username e bio do screenshot
3. **Implementar no sub-agente:** Criar automation loop completo
4. **Testar batch:** Rodar com todos os 15 perfis
5. **Integração final:** Sync screenshots → CRM → Supabase

