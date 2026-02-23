# Instagram Scraper – Memória do Projeto

## O que é
Agente hybrid para análise de seguidores Instagram. Scraping + integração Google Sheets/Drive.

## Status: Em Setup
- Script `agente_hybrid.py` criado
- Setup script `setup_hybrid.sh` corrigido (bug de sintaxe bash)
- Cron job configurado para rodar a cada 5 min
- **Pendente:** credenciais Google Cloud (service account)

## Histórico
| Data | Ação | Resultado |
|------|------|-----------|
| 2026-02-21 | Fix syntax error em setup_hybrid.sh | ✅ Corrigido parênteses → chaves |
| 2026-02-21 | Setup script criado | ✅ Pronto para rodar |

## Próximos Passos
1. Criar Service Account no Google Cloud
2. Baixar JSON e salvar em `projects/instagram-scraper/service_account.json`
3. Compartilhar folders com email da service account
4. Validar execução: `bash agente-followers.sh`

## Dependências
- Python 3 + venv
- google-auth-oauthlib, google-api-python-client, selenium
- Ollama (futuro, para análise local)
