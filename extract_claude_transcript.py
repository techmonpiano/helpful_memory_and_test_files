#!/usr/bin/env python3
"""
Generic Claude Code JSONL Transcript Extractor

Converts Claude Code session JSONL files into readable markdown transcripts.
Properly attributes tool results to Claude's entries instead of showing them as fake user entries.

Usage:
    python3 extract_claude_transcript.py <input_jsonl_file> [output_md_file]
    
If output file is not specified, auto-generates based on session ID and date.
"""

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path

def extract_session_info(file_path, entries):
    """Extract session metadata from file path and entries"""
    # Extract session ID from filename
    filename = Path(file_path).stem
    session_id = filename if re.match(r'^[0-9a-f-]+$', filename) else 'unknown'
    
    # Extract date range from timestamps
    timestamps = []
    for entry in entries[:10] + entries[-10:]:  # Check first and last 10 entries
        if 'timestamp' in entry:
            try:
                dt = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
                timestamps.append(dt)
            except:
                continue
    
    if timestamps:
        start_date = min(timestamps).strftime('%B %d, %Y')
        if len(set(t.date() for t in timestamps)) > 1:
            end_date = max(timestamps).strftime('%B %d, %Y')
            date_str = f'{start_date} - {end_date}'
        else:
            date_str = start_date
    else:
        date_str = 'Unknown'
    
    return session_id, date_str

def extract_conversation(file_path, output_file=None):
    """Extract conversation from Claude Code JSONL file to markdown"""
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return False
    
    # Auto-generate output filename if not provided
    if output_file is None:
        base_name = Path(file_path).stem
        output_file = f'{base_name}_transcript.md'
        print(f"📝 Auto-generating output filename: {output_file}")
    
    try:
        entries = []
        
        # First pass: read all entries and identify patterns
        print(f"📖 Reading JSONL file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    data = json.loads(line.strip())
                    if data.get('type') != 'summary':
                        entries.append(data)
                except json.JSONDecodeError:
                    continue
                except Exception:
                    continue
        
        if not entries:
            print("❌ Error: No valid conversation entries found in file")
            return False
        
        print(f"✅ Found {len(entries)} conversation entries")
        
        # Extract session metadata
        session_id, date_str = extract_session_info(file_path, entries)
        
        # Write transcript
        with open(output_file, 'w', encoding='utf-8') as out:
            out.write('# Claude Code Conversation Transcript\n')
            out.write(f'**Date:** {date_str}\n')
            out.write(f'**Session ID:** {session_id}\n')
            out.write(f'**Source File:** {Path(file_path).name}\n')
            out.write('---\n\n')
            
            # Second pass: process entries with context
            i = 0
            user_count = 0
            claude_count = 0
            
            while i < len(entries):
                entry = entries[i]
                
                # Process Assistant messages
                if entry.get('type') == 'assistant' and 'message' in entry:
                    message = entry['message']
                    timestamp = entry.get('timestamp', '')
                    claude_count += 1
                    
                    if timestamp:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        time_str = dt.strftime('%H:%M:%S')
                        out.write(f'## 🤖 **Claude** [{time_str}]\n\n')
                    else:
                        out.write(f'## 🤖 **Claude**\n\n')
                    
                    # Write Claude's content
                    if 'content' in message:
                        for item in message['content']:
                            if item.get('type') == 'text':
                                out.write(f"{item['text']}\n\n")
                            elif item.get('type') == 'tool_use':
                                out.write(f"**🔧 Tool Used:** {item['name']}\n\n")
                                if 'input' in item:
                                    if 'command' in item['input']:
                                        out.write(f"**Command:** `{item['input']['command']}`\n\n")
                                    if 'description' in item['input']:
                                        out.write(f"**Description:** {item['input']['description']}\n\n")
                                    # Include any other relevant input parameters
                                    for key, value in item['input'].items():
                                        if key not in ['command', 'description']:
                                            out.write(f"**{key.title()}:** {value}\n\n")
                    
                    # Check if the next entry is a tool result (same or very close timestamp)
                    if i + 1 < len(entries):
                        next_entry = entries[i + 1]
                        if (next_entry.get('type') == 'user' and 
                            'message' in next_entry and 
                            'content' in next_entry['message']):
                            
                            next_content = next_entry['message']['content']
                            # Check if this is a tool result
                            if isinstance(next_content, list):
                                for item in next_content:
                                    if isinstance(item, dict) and item.get('type') == 'tool_result':
                                        # This is a tool result - append it to Claude's entry
                                        if 'content' in item and item['content']:
                                            result_content = str(item['content'])
                                            out.write(f"**📊 Tool Result:**\n```\n")
                                            if len(result_content) > 3000:
                                                out.write(result_content[:3000])
                                                out.write('\n... (output truncated for readability)')
                                            else:
                                                out.write(result_content)
                                            out.write('\n```\n\n')
                                        # Skip the next entry since we've processed it
                                        i += 1
                                        break
                
                # Process User messages (only actual user text, not tool results)
                elif entry.get('type') == 'user' and 'message' in entry:
                    content = entry['message']['content']
                    timestamp = entry.get('timestamp', '')
                    actual_user_message = ""
                    
                    # Only process if it's actual user text (not a tool result)
                    if isinstance(content, str) and content.strip():
                        actual_user_message = content.strip()
                    elif isinstance(content, list):
                        # Check if this contains actual user input vs just tool results
                        has_user_text = False
                        for item in content:
                            if isinstance(item, dict):
                                # Skip tool results - they should be attached to Claude's entries
                                if item.get('type') == 'tool_result':
                                    continue
                                else:
                                    # Other content types might be actual user input
                                    item_str = str(item).strip()
                                    if item_str and len(item_str) > 10:
                                        actual_user_message += f'{item_str}\n'
                                        has_user_text = True
                            else:
                                # Plain text in array
                                item_str = str(item).strip()
                                if item_str and len(item_str) > 5:
                                    actual_user_message += f'{item_str}\n'
                                    has_user_text = True
                    
                    # Only write User entry if there's actual user input
                    if actual_user_message.strip():
                        user_count += 1
                        if timestamp:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            time_str = dt.strftime('%H:%M:%S')
                            out.write(f'## 👤 **User** [{time_str}]\n\n')
                        else:
                            out.write(f'## 👤 **User**\n\n')
                        out.write(f'{actual_user_message}\n\n')
                
                i += 1
            
            print(f"✅ Transcript created: {user_count} user messages, {claude_count} Claude responses")
            
        return True
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_claude_transcript.py <input_jsonl_file> [output_md_file]")
        print("\nExample:")
        print("  python3 extract_claude_transcript.py session.jsonl")
        print("  python3 extract_claude_transcript.py session.jsonl transcript.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if extract_conversation(input_file, output_file):
        print(f"🎉 Successfully extracted transcript to: {output_file or Path(input_file).stem + '_transcript.md'}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()