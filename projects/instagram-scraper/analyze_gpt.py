#!/usr/bin/env python3
"""Run brutal Cara de Pix analysis via OpenAI Vision and log result back to Supabase."""

import os
import re
from datetime import datetime
from typing import Dict, Optional, Tuple

from openai import OpenAI
from supabase import create_client, Client

PROMPT = """PROMPT - ANALISADOR BRUTAL DE "CARA DE PIX" (INSTAGRAM)
Função: Você é um analista de social selling high ticket, especializado em identificar capacidade real de compra (CRA) com base apenas em sinais visuais, comportamentais e posicionamento de perfis do Instagram.
Sua missão é ser frio, direto, pragmático e brutalmente honesto.
Você receberá apenas um print de um perfil do Instagram (foto, bio, nome, destaques visíveis, tipo de conteúdo, seguidores/seguindo, estética geral). Você NÃO deve ser educado. Você NÃO deve ser motivacional. Você NÃO deve suavizar o diagnóstico. Seu papel é responder à pergunta: "Essa pessoa tem ou não cara de PIX para produto high ticket?"

📌 REGRAS DE ANÁLISE
Avalie o perfil usando sinais indiretos de poder de compra, como:
- Posicionamento profissional (cargo, negócio, clareza de atuação)
- Linguagem da bio (adulto funcional vs aspiracional)
- Tipo de conteúdo (autoridade, trabalho, bastidores reais vs entretenimento vazio)
- Estética geral (organização, intenção, maturidade)
- Indícios de renda ativa (empresa, clientes, projetos, rotina)
- Rede social implícita (quem segue, quem parece seguir)
- Comportamento típico de comprador vs espectador
Ignore completamente:
- Beleza
- Simpatia
- Carisma
- "Potencial"
- Histórias emocionais
Aqui não existe "quase". Ou compra, ou não compra.

🧠 FORMATO OBRIGATÓRIO DA RESPOSTA
1️⃣ VEREDITO FINAL (obrigatório)
Escolha apenas UM: 🟢 TEM CARA DE PIX | 🔴 NÃO TEM CARA DE PIX

2️⃣ SCORE DE CRA (0 a 10)
Dê uma nota objetiva de capacidade de compra. Ex: CRA: 7.5 / 10

3️⃣ JUSTIFICATIVA BRUTAL (3 a 5 bullets, sem suavizar)
Exemplos de tom:
- Bio vaga, sem posição clara → não passa confiança
- Conteúdo não indica geração de renda
- Perfil mais aspiracional do que consolidado

4️⃣ CLASSIFICAÇÃO COMERCIAL (escolha UMA)
- Vale DM personalizada
- Só nutrição por conteúdo
- Ignorar completamente

5️⃣ ALERTA FINAL (1 frase)
Frase seca sobre o maior risco de abordar essa pessoa.

6️⃣ MENSAGEM INICIAL (SOCIAL SELLING AMIGÁVEL)
Regras para a primeira mensagem (abordagem suave, conversacional):
- Comece com um ELOGIO GENUÍNO ou OBSERVAÇÃO ESPECÍFICA do conteúdo/perfil (não genérico).
- Faça uma PERGUNTA que demonstre interesse real no que a pessoa faz (curiosidade, não pitch).
- Compartilhe um PONTO DE CONEXÃO ou interesse comum, sem vender nada ainda.
- Tom: colega conversando, não vendedor abordando.
- Máximo 2-3 frases, natural, sem emojis ou gírias forçadas.

EXEMPLO BOM: "Vi que você trabalha com agências em EUA — como você estrutura esse modelo? Estou explorando algo parecido."
EXEMPLO RUIM: "Vi seu resultado ajudando agências, tenho oportunidade que combina com você" (muito vendedor)

Seu objetivo é INICIAR UMA CONVERSA, não fazer pitch. A pessoa deve querer responder porque sente curiosidade/sintonia, não pressão.

🚫 PROIBIÇÕES
- Não use "talvez", "depende", "pode ser"
- Não aconselhe desenvolvimento pessoal
- Não sugira "aquecer mais"
- Não abra com "tenho uma oportunidade para você"
- Não comece com "vi que você faz..." sem uma pergunta ou ponto de conexão
- Nada de "que legal!" ou emojis

🧨 LEMBRETE FINAL
Seu trabalho não é julgar caráter. Seu trabalho é responder apenas: "Esse perfil parece alguém que passa PIX sem drama?" Se não, diga NÃO.
Para a mensagem: você é um colega curioso tentando iniciar conversa legítima, não um vendedor."""

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

if not (SUPABASE_URL and SUPABASE_SERVICE_KEY and OPENAI_API_KEY):
    raise SystemExit("Missing env vars: SUPABASE_URL, SUPABASE_SERVICE_KEY, OPENAI_API_KEY")

client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
BUCKET = "instagram-screenshots"
PUBLIC_ROOT = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}"


def fetch_pending(limit: int = 3):
    query = (
        client.table("instagram_followers")
        .select("id, username, file_path, analysis_status")
        .order("updated_at", desc=True)
        .limit(limit)
    )
    data = query.execute().data or []
    pending = [row for row in data if row.get("analysis_status") in (None, "pending", "error")]
    return pending


def call_openai(image_url: str) -> str:
    response = openai_client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Você é um avaliador brutal de capacidade de compra. Siga estritamente o formato solicitado."
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": PROMPT},
                    {"type": "input_image", "image_url": image_url}
                ]
            }
        ]
    )
    return response.output[0].content[0].text


def parse_output(text: str) -> Dict[str, Optional[str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    verdict = next((l for l in lines if "TEM CARA" in l or "NÃO TEM" in l or "NAO TEM" in l), None)
    score_line = next((l for l in lines if "CRA:" in l.upper()), None)
    if not score_line:
        score_line = next((l for l in lines if "CRA" in l.upper()), None)
    score_val = None
    if score_line:
        match = re.search(r"(\d+(?:[\.,]\d+)?)", score_line)
        if match:
            score_val = float(match.group(1).replace(",", "."))
    classification = next((l for l in lines if "Vale DM" in l or "nutrição" in l or "Ignorar" in l), None)

    # justification bullets between "JUSTIFICATIVA" and next numbered section
    justification: list[str] = []
    collecting = False
    for line in lines:
        if "JUSTIFICATIVA" in line.upper():
            collecting = True
            continue
        if collecting and line.startswith("4️⃣"):
            break
        if collecting and line.startswith(("-", "•", "*")):
            justification.append(line.lstrip("-*• "))
    alert = next((l for l in lines if "ALERTA" in l.upper()), None)

    dm_hook = None
    for idx, line in enumerate(lines):
        if "MENSAGEM" in line.upper():
            if idx + 1 < len(lines):
                dm_hook = lines[idx + 1]
            break

    return {
        "verdict": verdict,
        "score": score_val,
        "classification": classification,
        "justification": "\n".join(justification) if justification else None,
        "alert": alert,
        "dm_hook": dm_hook,
        "raw": text.strip()
    }


def update_row(row_id: int, username: str, parsed: Dict[str, Optional[str]]):
    payload = {
        "analysis_status": "done",
        "gpt_model": MODEL,
        "gpt_analyzed_at": datetime.utcnow().isoformat() + "Z",
        "gpt_raw": parsed["raw"]
    }
    if parsed.get("score") is not None:
        payload["gpt_score"] = parsed["score"]
    if parsed.get("verdict"):
        payload["gpt_verdict"] = parsed["verdict"]
    if parsed.get("classification"):
        payload["gpt_classification"] = parsed["classification"]
    if parsed.get("justification"):
        payload["gpt_summary"] = parsed["justification"]
    if parsed.get("alert"):
        payload["gpt_alert"] = parsed["alert"]
    if parsed.get("dm_hook"):
        payload["gpt_dm_hook"] = parsed["dm_hook"]

    client.table("instagram_followers").update(payload).eq("id", row_id).execute()
    print(f"✅ @{username} analisado")


def mark_error(row_id: int, username: str, error_msg: str):
    client.table("instagram_followers").update({
        "analysis_status": "error",
        "gpt_alert": error_msg[:250]
    }).eq("id", row_id).execute()
    print(f"❌ @{username}: {error_msg}")


def run(limit: int = 3):
    pending = fetch_pending(limit)
    if not pending:
        print("Nenhum perfil pendente")
        return

    for row in pending:
        username = row["username"]
        row_id = row["id"]
        file_path = row.get("file_path")
        if not file_path:
            mark_error(row_id, username, "Sem file_path")
            continue
        image_url = file_path if file_path.startswith("http") else f"{PUBLIC_ROOT}/{file_path.lstrip('/')}"
        try:
            text = call_openai(image_url)
            parsed = parse_output(text)
            update_row(row_id, username, parsed)
        except Exception as exc:
            mark_error(row_id, username, str(exc))


if __name__ == "__main__":
    run(limit=int(os.environ.get("GPT_BATCH", "3")))
