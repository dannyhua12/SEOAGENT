#!/usr/bin/env python3
"""
Simple Keyword Generator - Generate SEO keywords for a given topic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from keyword_generator import generate_keywords, save_keywords_to_file, display_keywords

def main():
    print("🔍 SEO Keyword Generator")
    print("=" * 40)
    
    # Get topic from user
    topic = input("Enter your topic: ").strip()
    if not topic:
        print("❌ Topic is required!")
        return
    
    # Get keyword count
    try:
        count = input("Enter number of keywords to generate (default: 15): ").strip()
        count = int(count) if count else 15
        if count < 1 or count > 50:
            print("❌ Keyword count should be between 1 and 50.")
            return
    except ValueError:
        print("❌ Please enter a valid number for keyword count.")
        return
    
    # Get keyword types
    print("\n📝 Available keyword types:")
    print("- primary_keywords: Main target keywords (1-3 words)")
    print("- long_tail_keywords: Longer, specific phrases (4+ words)")
    print("- question_keywords: What, how, why questions")
    print("- local_keywords: Location-based keywords")
    print("- related_keywords: Synonyms and related terms")
    
    types_input = input("Enter keyword types (comma-separated, or press Enter for all): ").strip()
    
    keyword_types = None
    if types_input:
        valid_types = ['primary_keywords', 'long_tail_keywords', 'question_keywords', 'local_keywords', 'related_keywords']
        selected_types = [t.strip() for t in types_input.split(',')]
        keyword_types = [t for t in selected_types if t in valid_types]
        
        if not keyword_types:
            print("❌ No valid keyword types selected. Using all types.")
            keyword_types = None
    
    print(f"\n🎯 Generating {count} keywords for: {topic}")
    if keyword_types:
        print(f"📌 Keyword types: {', '.join(keyword_types)}")
    else:
        print("📌 Keyword types: All types")
    
    try:
        # Generate keywords
        keywords_data = generate_keywords(topic, count, keyword_types)
        
        if keywords_data:
            # Display keywords
            display_keywords(keywords_data)
            
            # Save to file
            filepath = save_keywords_to_file(keywords_data, topic)
            print(f"\n✅ Keywords saved to: {filepath}")
            
            # Show summary
            total_keywords = sum(len(keyword_list) for keyword_list in keywords_data.get('keywords', {}).values())
            print(f"📊 Total keywords generated: {total_keywords}")
            
        else:
            print("❌ Failed to generate keywords. Please check your OpenAI API key and try again.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your OpenAI API key and internet connection.")

if __name__ == "__main__":
    main() 