# Handler de Automação Instagram

## Padrão Reconhecido
```
analise @username
```

## Flow Automático
Quando Pedro enviar a mensagem acima, Alfred:

1. **Detecta** o padrão `analise @\w+`
2. **Extrai** o username
3. **Abre Firefox** com Playwright/browser control
4. **Login** automático (email + password)
5. **Navega** para instagram.com/@username
6. **Ativa viewport mobile** (375x812px)
7. **Screenshot** de alta qualidade
8. **Salva** em `/home/harvey1806/Documents/Seguidores/@username_TIMESTAMP.png`
9. **Log** em `Seguidores/index.md`
10. **Responde** ao Pedro: `✅ Captura salva: @username_TIMESTAMP.png`

## Integrações Necessárias
- [x] Pasta criada
- [x] Scripts prontos
- [ ] Browser automation ativa
- [ ] Interceptor de mensagens ativo
- [ ] Teste com @exemplo

## Próximo Passo
Ativar o handler e fazer teste com @exemplo
