#!/usr/bin/env python3
"""
Agent Sleep Cycle Execution (Enhanced)
Integrates with agent-library for semantic compression.
"""
import os
import shutil
import datetime
import sys
import json
from pathlib import Path

# Setup paths
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "."))
MEMORY_DIR = WORKSPACE / "memory"
ARCHIVE_DIR = MEMORY_DIR / "archive"
KNOWLEDGE_DIR = WORKSPACE / "agent-library/knowledge"
LIBRARY_SRC = WORKSPACE / "agent-library/src"
MEMORY_FILE = WORKSPACE / "MEMORY.md"

# Add agent-library to path to reuse converter
if LIBRARY_SRC.exists():
    sys.path.append(str(LIBRARY_SRC))
    try:
        from converter import PDFConverter
        print("✅ Loaded agent-library converter")
    except ImportError:
        print("⚠️ Could not load agent-library converter. Fallback to simple mode.")
        PDFConverter = None
else:
    print("⚠️ agent-library not found. Fallback to simple mode.")
    PDFConverter = None

def consolidate_memory(day_file: Path):
    """
    Convert daily log into Agent-Native Knowledge (.toon)
    """
    if not PDFConverter:
        return

    print(f"🧠 Consolidating memory from {day_file.name}...")
    
    try:
        content = day_file.read_text(encoding='utf-8')
        
        # Initialize converter (we only need the chunking logic)
        converter = PDFConverter(use_llm=False)
        
        # Use chunk_content directly (bypass PDF parsing)
        chunks = converter.chunk_content(content, day_file.stem)
        
        if not chunks:
            print("  - No content to chunk.")
            return

        # Generate TOON content
        toon_content = converter.to_toon(
            chunks, 
            title=f"Daily Memory: {day_file.stem}", 
            author="Agent Self"
        )
        
        # Save to Knowledge Base
        KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
        output_path = KNOWLEDGE_DIR / f"{day_file.stem}.toon"
        output_path.write_text(toon_content, encoding='utf-8')
        
        print(f"  ✨ Created knowledge crystal: {output_path}")
        print(f"  - Extracted {len(chunks)} semantic chunks")
        
        # Update Long-term MEMORY.md with high-level summary
        update_long_term_memory(chunks, day_file.stem)
        
    except Exception as e:
        print(f"❌ Consolidation failed: {e}")

def update_long_term_memory(chunks, date_str):
    """
    Append key insights to MEMORY.md
    """
    
    # Simple heuristic: take the summary of the first and last chunks
    # In a real system, we would use an LLM to summarize all chunks
    if not chunks:
        return
        
    insights = []
    for c in chunks:
        # If chunk has interesting keywords, keep it
        if any(k in ['learned', 'decision', 'important', 'plan', 'strategy'] for k in c.keywords):
            insights.append(f"- {c.summary}")
            
    if not insights:
        # Fallback: just take the titles
        insights = [f"- {c.title}" for c in chunks[:5]]

    entry = f"\n\n### {date_str} Consolidation\n" + "\n".join(insights[:5]) # Limit to 5 items
    
    with open(MEMORY_FILE, "a") as f:
        f.write(entry)
    
    print(f"  📝 Updated long-term memory")

def deep_sleep():
    """
    Deep Sleep: Consolidate and Prune
    """
    print("🛌 Entering Deep Sleep...")
    
    # Ensure directories exist
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    
    processed_count = 0
    
    # Process yesterday's and older files
    for file in MEMORY_DIR.glob("202*-*-*.md"):
        # Skip today's file (still active)
        if file.stem == today:
            print(f"  - Skipping today's active memory: {file.name}")
            continue
            
        # 1. Consolidate (Convert to Knowledge)
        consolidate_memory(file)
        
        # 2. Archive (Move raw log)
        shutil.move(str(file), str(ARCHIVE_DIR / file.name))
        processed_count += 1
        
    print(f"📦 Processed and archived {processed_count} logs.")
    
    # 3. Clean temp files
    # (Safe cleanup: only delete known temp extensions in workspace root)
    for ext in ["*.tmp", "*.log"]:
        for temp in WORKSPACE.glob(ext):
            try:
                temp.unlink()
                print(f"  - Deleted temp file: {temp.name}")
            except:
                pass

if __name__ == "__main__":
    deep_sleep()
