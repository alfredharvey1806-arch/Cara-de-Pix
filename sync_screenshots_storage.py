#!/usr/bin/env python3
"""Sync Instagram screenshots to Supabase Storage and update DB paths."""

import os
import requests
from datetime import datetime
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
BUCKET_NAME = os.environ.get("SUPABASE_BUCKET_NAME", "instagram-screenshots")
SCREENSHOTS_DIR = os.path.expanduser(os.environ.get("SCREENSHOTS_DIR", "~/Documents/Seguidores"))

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise SystemExit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")

class ScreenshotStorageSync:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    # ---------------- Bucket helpers ----------------
    def ensure_bucket(self):
        buckets = self.client.storage.list_buckets()
        if any(getattr(b, "name", None) == BUCKET_NAME for b in buckets):
            print(f"🪣 Bucket '{BUCKET_NAME}' já existe")
            return
        print(f"🪣 Criando bucket '{BUCKET_NAME}' (publico)")
        resp = requests.post(
            f"{SUPABASE_URL}/storage/v1/bucket",
            headers={
                "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
                "apikey": SUPABASE_SERVICE_KEY,
                "Content-Type": "application/json"
            },
            json={"name": BUCKET_NAME, "public": True}
        )
        if resp.status_code not in (200, 201):
            raise RuntimeError(f"Falha ao criar bucket: {resp.status_code} {resp.text}")
        else:
            print("   ✅ Bucket criado")
    
    # ---------------- File helpers ----------------
    def list_screenshots(self):
        if not os.path.exists(SCREENSHOTS_DIR):
            return []
        return sorted([
            os.path.join(SCREENSHOTS_DIR, f)
            for f in os.listdir(SCREENSHOTS_DIR)
            if f.lower().endswith(".png")
        ])
    
    def extract_username(self, filename: str) -> str | None:
        base = os.path.basename(filename)
        if not base.startswith("@"):
            return None
        sanitized = base.lstrip("@")
        parts = sanitized.rsplit("_", 2)
        if len(parts) >= 3:
            username = "_".join(parts[:-2])
        else:
            username = parts[0]
        username = username.strip()
        return username or None
    
    # ---------------- Upload + DB sync ----------------
    def upload_file(self, filepath: str) -> str | None:
        storage_path = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            data = f.read()
        try:
            self.client.storage.from_(BUCKET_NAME).upload(
                storage_path,
                data,
                {
                    "content-type": "image/png"
                }
            )
            print(f"   ✅ Upload: {storage_path}")
            return storage_path
        except Exception as e:
            if "exists" in str(e).lower():
                print(f"   ⚠️ Já existe: {storage_path}")
                return storage_path
            print(f"   ❌ Erro upload {storage_path}: {e}")
            return None
    
    def update_db_path(self, username: str, storage_path: str):
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{storage_path}"
        payload = {
            "file_path": public_url,
            "updated_at": datetime.now().isoformat()
        }
        response = self.client.table("instagram_followers").update(payload) \
            .eq("username", username).execute()
        if response.data:
            print(f"   🗄️ DB update @{username} -> {storage_path}")
            return True
        insert = self.client.table("instagram_followers").insert({
            "username": username,
            "status": "print feito",
            "file_path": public_url,
            "added_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }).execute()
        if insert.data:
            print(f"   ➕ DB insert @{username}")
            return True
        print(f"   ❌ Falha ao atualizar/inserir @{username}")
        return False
    
    def run(self):
        print("=" * 60)
        print("🚀 Sync de screenshots para Supabase Storage")
        print("=" * 60)
        
        self.ensure_bucket()
        files = self.list_screenshots()
        if not files:
            print("⚠️ Nenhum arquivo encontrado em ~/Documents/Seguidores")
            return
        
        print(f"📸 {len(files)} arquivos encontrados")
        for filepath in files:
            username = self.extract_username(filepath)
            if not username:
                print(f"   ⚠️ Ignorando {filepath} (sem username)")
                continue
            storage_path = self.upload_file(filepath)
            if storage_path:
                self.update_db_path(username, storage_path)
        
        print("\n✅ Sync concluído")

if __name__ == "__main__":
    sync = ScreenshotStorageSync()
    sync.run()
