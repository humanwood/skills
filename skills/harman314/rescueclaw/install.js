#!/usr/bin/env node
/**
 * Post-install hook for RescueClaw skill
 * Sets up local data directory and checks for the daemon binary.
 * Does NOT use curl | bash — binary is bundled or downloaded from GitHub Releases.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

console.log('🛟 RescueClaw Skill - Post-Install Setup\n');

// Use user-local path instead of /var/rescueclaw
const dataDir = path.join(os.homedir(), '.openclaw', 'rescueclaw');

// Ensure data directory exists
if (!fs.existsSync(dataDir)) {
  console.log(`📁 Creating data directory: ${dataDir}`);
  try {
    fs.mkdirSync(dataDir, { recursive: true, mode: 0o755 });
    console.log('   ✅ Directory created');
  } catch (err) {
    console.log(`   ⚠️  Could not create ${dataDir}: ${err.message}`);
    console.log(`   Run manually: mkdir -p ${dataDir}`);
  }
} else {
  console.log(`✅ Data directory ready: ${dataDir}`);
}

// Check if rescueclaw binary is installed
try {
  const version = execSync('rescueclaw --version', {
    encoding: 'utf-8',
    stdio: ['pipe', 'pipe', 'pipe']
  }).trim();
  console.log(`✅ RescueClaw daemon found: ${version}`);
} catch {
  console.log('⚠️  RescueClaw daemon not found in PATH');
  
  // Check if bundled binary exists for this platform
  const arch = os.arch();       // x64, arm64
  const platform = os.platform(); // linux, darwin
  const binName = `rescueclaw-${platform}-${arch}`;
  const bundledPath = path.join(__dirname, 'bin', binName);
  
  if (fs.existsSync(bundledPath)) {
    const installPath = path.join(os.homedir(), '.local', 'bin', 'rescueclaw');
    console.log(`📦 Found bundled binary for ${platform}/${arch}`);
    try {
      fs.mkdirSync(path.dirname(installPath), { recursive: true });
      fs.copyFileSync(bundledPath, installPath);
      fs.chmodSync(installPath, 0o755);
      console.log(`✅ Installed to ${installPath}`);
      console.log(`   Make sure ~/.local/bin is in your PATH`);
    } catch (err) {
      console.log(`   ⚠️  Could not install: ${err.message}`);
      console.log(`   Copy manually: cp ${bundledPath} ~/.local/bin/rescueclaw && chmod +x ~/.local/bin/rescueclaw`);
    }
  } else {
    console.log(`\n   To install, download the binary for your platform from:`);
    console.log(`   https://github.com/harman314/rescueclaw/releases`);
    console.log(`\n   Then place it in your PATH (e.g. ~/.local/bin/rescueclaw)`);
  }
}

console.log('\n🎯 Skill ready! Use rescueclaw-checkpoint.js for safe operations.');
