const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Mock implementation of callSkill (would be replaced by actual OpenClaw SDK)
async function callSkill(skillName, action, params) {
  console.log(`Mock callSkill: ${skillName}.${action}`, params);
  // This is a placeholder - in real implementation, this would call the actual skill
  if (skillName === 'tavily-search' && action === 'search') {
    // Simulate Tavily response
    return {
      items: [
        { title: `Tavily result for "${params.q}"`, url: 'http://example.com', score: 0.9 },
        { title: `Another Tavily result for "${params.q}"`, url: 'http://example2.com', score: 0.8 }
      ]
    };
  }
  if (skillName === 'web-search-plus' && action === 'search') {
    // Simulate Web Search Plus response
    return {
      items: [
        { title: `Web Search Plus result for "${params.q}"`, url: 'http://example3.com', score: 0.7 },
        { title: `Another Web Search Plus result for "${params.q}"`, url: 'http://example4.com', score: 0.6 }
      ]
    };
  }
  return { items: [] };
}

// Simple local file search (placeholder - would use SQLite FTS in real impl)
function searchLocalFiles(query, maxResults) {
  // Placeholder for local file search
  // In a real implementation, this would query a SQLite database with FTS
  // For now, just return some mock results based on file names in the workspace
  const results = [];
  const workspaceDir = process.env.HOME ? path.join(process.env.HOME, '.openclaw', 'workspace') : './';
  try {
    const files = fs.readdirSync(workspaceDir);
    for (const file of files) {
      if (file.toLowerCase().includes(query.toLowerCase())) {
        results.push({
          path: path.join(workspaceDir, file),
          snippet: `Found query "${query}" in filename: ${file}`,
          score: 0.5 // Placeholder score
        });
      }
    }
  } catch (e) {
    console.warn('Could not search local files:', e.message);
  }
  return results.slice(0, maxResults);
}

// Parse arguments manually
const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    const key = args[i].substring(2);
    const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true;
    params[key] = value;
  }
}

const { query, sources, max_results } = params;
let sourceList = ['tavily', 'web-search-plus', 'local']; // Default
if (sources) {
  try {
    sourceList = JSON.parse(sources);
  } catch (e) {
    console.error('Invalid JSON for sources, using defaults');
  }
}
const maxResults = parseInt(max_results) || 5;

async function doTool() {
  if (!query) {
    console.error('Error: --query is required');
    process.exit(1);
  }

  const results = [];

  if (sourceList.includes('tavily')) {
    try {
      const r = await callSkill('tavily-search', 'search', { q: query, limit: maxResults });
      results.push(...r.items.map(i => ({ source: 'tavily', title: i.title, url: i.url, score: i.score })));
    } catch (e) {
      console.warn('Tavily search failed:', e.message);
    }
  }

  if (sourceList.includes('web-search-plus')) {
    try {
      const r = await callSkill('web-search-plus', 'search', { q: query, limit: maxResults });
      results.push(...r.items.map(i => ({ source: 'web-search-plus', title: i.title, url: i.url, score: i.score })));
    } catch (e) {
      console.warn('Web Search Plus failed:', e.message);
    }
  }

  if (sourceList.includes('local')) {
    const local = searchLocalFiles(query, maxResults);
    results.push(...local.map(l => ({ source: 'local', title: l.path, snippet: l.snippet, score: l.score })));
  }

  // simple rank by score then return top N
  results.sort((a, b) => (b.score || 0) - (a.score || 0));
  const topResults = results.slice(0, maxResults);

  console.log(JSON.stringify(topResults, null, 2));
}

doTool();
