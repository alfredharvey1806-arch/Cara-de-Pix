# 🔗 Integração do Sistema Instagram com Alfred

## Padrão Reconhecido
```
analise @username
```

## Fluxo Automático (PRONTO PARA ATIVAR)

Quando você enviar a mensagem, Alfred:

### 1️⃣ **Recebe o padrão**
```
usuario: "analise @pedrosallun"
alfred: reconhece pattern + extrai "pedrosallun"
```

### 2️⃣ **Abre o navegador**
```
browser.start() → Instagram.com
```

### 3️⃣ **Faz login**
```
email: alfredharvey1806@gmail.com
password: Sucesso$$2026$$
```

### 4️⃣ **Clica na lupa de pesquisa**
```
browser.click(searchIcon) → abre caixa de busca
```

### 5️⃣ **Digita o @username**
```
browser.type("pedrosallun")
```

### 6️⃣ **Clica no perfil**
```
browser.click(profileLink) → abre perfil
```

### 7️⃣ **Tira screenshot**
```
browser.screenshot("@pedrosallun_20260215_112706.png")
```

### 8️⃣ **Salva em Seguidores/**
```
/home/harvey1806/Documents/Seguidores/@pedrosallun_20260215_112706.png
```

### 9️⃣ **Log em index.md**
```
- `@pedrosallun` | 20260215_112706 | @pedrosallun_20260215_112706.png
```

### 🔟 **Responde para você**
```
✅ Captura salva: @pedrosallun_20260215_112706.png
```

---

## Status
🔴 **BLOQUEADOR**: Ambiente sem display (sandbox Linux)
- Selenium + Firefox crasham sem X11
- Playwright Firefox tb depende de display
- Chrome não está instalado

## Solução Recomendada
**Integração com OpenClaw browser control nativo**:
- Use `browser action` com `profile="chrome"` (relay) ou `profile="openclaw"`
- Você clica no toolbar de OpenClaw pra ativar
- Alfred controla os passos via browser tool

## Próximos Passos
1. **Você testa manualmente**: abra Instagram no seu navegador, pesquise @pedrosallun
2. **Depois configuramos**: como Alfred vai enviar comandos pro browser que você tem aberto
3. **Ou**: você permite que Alfred use um browser separado (headless com display)

Qual caminho quer?
