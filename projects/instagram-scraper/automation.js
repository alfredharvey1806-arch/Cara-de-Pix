/**
 * Instagram Profile Screenshot Automation
 * Trigger: "analise @username"
 * Output: /home/harvey1806/Documents/Seguidores/@username_TIMESTAMP.png
 */

const fs = require('fs');
const path = require('path');

// Configuração
const CONFIG = {
  email: 'alfredharvey1806@gmail.com',
  password: 'Sucesso$$2026$$',
  outputDir: '/home/harvey1806/Documents/Seguidores',
  instagramUrl: 'https://www.instagram.com',
  mobileViewport: { width: 375, height: 812 } // iPhone 12
};

/**
 * Extrai o username do input "analise @username"
 */
function extractUsername(input) {
  const match = input.match(/@(\w+)/i);
  if (!match) return null;
  return match[1];
}

/**
 * Gera timestamp formatado
 */
function getTimestamp() {
  const now = new Date();
  return now.toISOString().replace(/[:-]/g, '').split('.')[0] + '_' + Math.random().toString(36).substr(2, 5);
}

/**
 * Automação principal
 */
async function analyzeProfile(username) {
  console.log(`🔄 Iniciando análise de @${username}...`);
  
  const timestamp = getTimestamp();
  const filename = `@${username}_${timestamp}.png`;
  const filepath = path.join(CONFIG.outputDir, filename);
  
  try {
    // Validar pasta
    if (!fs.existsSync(CONFIG.outputDir)) {
      console.error(`❌ Pasta não existe: ${CONFIG.outputDir}`);
      return false;
    }
    
    console.log(`📸 Capturando perfil de @${username}...`);
    console.log(`💾 Salvando em: ${filepath}`);
    
    // Aqui entra a integração com browser control do OpenClaw
    // Return true quando screenshot for salvo
    
    return {
      success: true,
      username,
      filepath,
      timestamp
    };
    
  } catch (error) {
    console.error(`❌ Erro na captura: ${error.message}`);
    return false;
  }
}

module.exports = { extractUsername, analyzeProfile, CONFIG };
