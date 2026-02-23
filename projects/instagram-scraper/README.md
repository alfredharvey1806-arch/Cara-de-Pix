# Instagram Profile Screenshot System

## Objetivo
Automatizar captura de screenshots de perfis do Instagram em modo mobile e salvar organizados em `/home/harvey1806/Documents/Seguidores/`.

## Como Usar
Você envia para Alfred:
```
@username
```

Alfred fará:
1. Login em `alfredharvey1806@gmail.com`
2. Navega para o perfil
3. Ativa modo mobile via viewport
4. Tira screenshot de alta qualidade
5. Salva em `Seguidores/` com timestamp

## Estrutura de Saída
```
Seguidores/
├── @username_20260215_112030.png
├── @username_20260215_112045.png
└── index.md (log das capturas)
```

## Status
🟢 Pasta criada  
🟡 Automação em desenvolvimento  
⚠️ Próximo: Integrar com browser control + definir trigger via webhook/cron

## Próximos Passos
1. Teste login Instagram no Firefox
2. Definir como você quer enviar o @username (chat direto? arquivo? comando?)
3. Calibrar viewport mobile ideal
4. Criar automation trigger
