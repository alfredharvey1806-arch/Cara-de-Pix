/**
 * Handler para automação Instagram
 * Padrão: "analise @username"
 * 
 * Quando receber essa mensagem, Alfred ativa:
 * 1. Abre browser
 * 2. Loga em Instagram
 * 3. Clica na lupa
 * 4. Pesquisa @username
 * 5. Tira screenshot
 * 6. Salva em Seguidores/
 * 7. Log em index.md
 */

const fs = require('fs');
const path = require('path');

class InstagramHandler {
  constructor() {
    this.outputDir = '/home/harvey1806/Documents/Seguidores';
    this.email = 'alfredharvey1806@gmail.com';
    this.password = 'Sucesso$$2026$$';
  }

  extractUsername(text) {
    const match = text.match(/@(\w+)/i);
    return match ? match[1] : null;
  }

  async captureProfile(username, browserControl) {
    const timestamp = new Date().toISOString().replace(/[:-]/g, '').split('.')[0];
    const filename = `@${username}_${timestamp}.png`;
    const filepath = path.join(this.outputDir, filename);

    console.log(`\n${'='.repeat(70)}`);
    console.log(`🔄 CAPTURA: @${username}`);
    console.log(`${'='.repeat(70)}`);
    console.log(`📧 Email: ${this.email}`);
    console.log(`📱 Modo: Mobile (375x812)`);
    console.log(`💾 Destino: ${filepath}`);
    console.log(`⏰ Timestamp: ${timestamp}`);
    console.log(`${'='.repeat(70)}\n`);

    // Criar diretório
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }

    // AQUI entra a integração com o browser control do OpenClaw
    // Fluxo:
    // 1. browserControl.navigate('https://www.instagram.com');
    // 2. browserControl.login(this.email, this.password);
    // 3. browserControl.clickSearchIcon();
    // 4. browserControl.typeSearch(username);
    // 5. browserControl.clickProfile(username);
    // 6. browserControl.screenshot(filepath);

    console.log(`✅ [PLACEHOLDER] Captura pronta para: @${username}`);
    console.log(`   Será salva em: ${filepath}`);

    return {
      success: true,
      username,
      filename,
      filepath,
      message: `✅ Captura pronta (aguardando integração com browser)`
    };
  }

  handleMessage(messageText, browserControl) {
    const username = this.extractUsername(messageText);
    
    if (!username) {
      return null; // Padrão não reconhecido
    }

    return this.captureProfile(username, browserControl);
  }
}

module.exports = InstagramHandler;
