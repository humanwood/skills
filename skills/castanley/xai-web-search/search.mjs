// search.mjs
// xAI Web Search helper function

/**
 * Search the web using xAI's Grok API
 * @param {Object} options - Search options
 * @param {string} options.query - Search query (required)
 * @param {string} options.model - Model to use (default: grok-4-1-fast-reasoning)
 * @param {string[]} options.allowed_domains - Restrict to these domains (max 5)
 * @param {string[]} options.excluded_domains - Exclude these domains (max 5)
 * @param {boolean} options.enable_image_understanding - Enable image analysis
 * @returns {Promise<Object>} Search results with content and citations
 */
export async function search_web(options) {
  const {
    query,
    model = 'grok-4-1-fast-reasoning',
    allowed_domains = null,
    excluded_domains = null,
    enable_image_understanding = false
  } = options;

  // Validate API key
  if (!process.env.XAI_API_KEY) {
    throw new Error('XAI_API_KEY environment variable is required');
  }

  // Validate domain filters
  if (allowed_domains && allowed_domains.length > 5) {
    throw new Error('Maximum 5 allowed_domains');
  }
  if (excluded_domains && excluded_domains.length > 5) {
    throw new Error('Maximum 5 excluded_domains');
  }
  if (allowed_domains && excluded_domains) {
    throw new Error('Cannot use both allowed_domains and excluded_domains');
  }

  // Build tool - exactly like the curl example
  const tool = { type: "web_search" };
  
  // Add optional parameters directly to the tool object
  if (allowed_domains) tool.allowed_domains = allowed_domains;
  if (excluded_domains) tool.excluded_domains = excluded_domains;
  if (enable_image_understanding) tool.enable_image_understanding = true;

  // Make API request - exactly like the curl example
  const response = await fetch('https://api.x.ai/v1/responses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.XAI_API_KEY}`
    },
    body: JSON.stringify({
      model,
      input: [
        {
          role: 'user',
          content: query
        }
      ],
      tools: [tool]
    })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(`API Error: ${error.error?.message || response.statusText}`);
  }

  const data = await response.json();
  
  // Extract response from output array
  const output = data.output || [];
  const lastMessage = output[output.length - 1] || {};

  return {
    content: lastMessage.content || '',
    citations: data.citations || [],
    usage: data.usage || {},
    server_side_tool_usage: data.server_side_tool_usage || {},
    raw_response: data
  };
}

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const query = process.argv[2];
  
  if (!query) {
    console.error('Usage: node search.mjs "your search query"');
    process.exit(1);
  }

  try {
    const result = await search_web({ query });
    console.log(result.content);
    
    if (result.citations && result.citations.length > 0) {
      console.log('\nSources:');
      result.citations.forEach(cite => {
        console.log(`- ${cite.title || 'Untitled'} (${cite.url})`);
      });
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}
