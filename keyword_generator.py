#!/usr/bin/env python3
"""
Keyword Generator - Generate SEO keywords for a given topic using chat
"""

import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_keywords(topic, keyword_count=15, keyword_types=None):
    """
    Generate SEO keywords for a given topic using OpenAI chat
    
    Args:
        topic (str): The main topic to generate keywords for
        keyword_count (int): Number of keywords to generate (default: 15)
        keyword_types (list): Types of keywords to include (default: all types)
    
    Returns:
        dict: JSON object with keywords organized by type
    """
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Set up OpenAI API key for older version
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Default keyword types if none specified
    if keyword_types is None:
        keyword_types = [
            "primary_keywords",
            "long_tail_keywords", 
            "question_keywords",
            "local_keywords",
            "related_keywords"
        ]
    
    # Build the prompt for keyword generation
    prompt = build_keyword_prompt(topic, keyword_count, keyword_types)
    
    try:
        # Make the API call using older format
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert SEO specialist who generates high-quality, searchable keywords for content optimization."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract the response content
        content = response.choices[0].message.content.strip()
        
        # Try to parse the JSON response
        try:
            keywords_data = json.loads(content)
            return keywords_data
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                keywords_data = json.loads(json_match.group())
                return keywords_data
            else:
                raise ValueError("Failed to parse JSON response from OpenAI")
                
    except Exception as e:
        raise Exception(f"Error generating keywords: {str(e)}")

def build_keyword_prompt(topic, keyword_count, keyword_types):
    """
    Build the prompt for keyword generation
    """
    
    keyword_type_descriptions = {
        "primary_keywords": "main target keywords (1-3 words)",
        "long_tail_keywords": "longer, more specific phrases (4+ words)",
        "question_keywords": "keywords that start with what, how, why, when, where, etc.",
        "local_keywords": "keywords with location modifiers",
        "related_keywords": "semantically related terms and synonyms"
    }
    
    # Build the types section
    types_section = ""
    for keyword_type in keyword_types:
        if keyword_type in keyword_type_descriptions:
            types_section += f"- {keyword_type}: {keyword_type_descriptions[keyword_type]}\n"
    
    return f"""
Generate SEO keywords for the topic: "{topic}"

Requirements:
- Generate {keyword_count} keywords total
- Focus on high-search-volume, low-competition keywords
- Include a mix of different keyword types
- Keywords should be relevant and valuable for SEO

Keyword types to include:
{types_section}

Return the result in valid JSON format like this:

{{
  "topic": "{topic}",
  "total_keywords": {keyword_count},
  "keywords": {{
    "primary_keywords": ["keyword1", "keyword2", "keyword3"],
    "long_tail_keywords": ["long tail keyword 1", "long tail keyword 2"],
    "question_keywords": ["what is...", "how to...", "why does..."],
    "local_keywords": ["topic near me", "topic in [city]"],
    "related_keywords": ["synonym1", "related term1", "alternative1"]
  }},
  "seo_insights": {{
    "search_volume_estimate": "high/medium/low",
    "competition_level": "high/medium/low",
    "recommended_focus": "primary keywords to target first"
  }}
}}

Make sure all keywords are:
- Relevant to the topic
- Searchable and commonly used
- Optimized for SEO
- Include the main topic naturally
"""

def save_keywords_to_file(keywords_data, topic, output_dir=None):
    """
    Save generated keywords to JSON file
    
    Args:
        keywords_data (dict): The keywords data
        topic (str): The original topic
        output_dir (str): Directory to save the file (default: ~/SEO articles)
    """
    
    # Use SEO articles folder as default
    if output_dir is None:
        output_dir = os.path.expanduser('~/SEO articles')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename
    slug = topic.lower().replace(" ", "-").replace("/", "-")
    filename = f"keywords-{slug}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Save to file
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(keywords_data, f, indent=2, ensure_ascii=False)
    
    return filepath

def display_keywords(keywords_data):
    """
    Display keywords in a formatted way
    """
    print(f"\n🎯 Keywords for: {keywords_data.get('topic', 'Unknown Topic')}")
    print("=" * 50)
    
    keywords = keywords_data.get('keywords', {})
    
    for keyword_type, keyword_list in keywords.items():
        if keyword_list:
            print(f"\n📌 {keyword_type.replace('_', ' ').title()}:")
            for i, keyword in enumerate(keyword_list, 1):
                print(f"   {i}. {keyword}")
    
    # Display SEO insights
    insights = keywords_data.get('seo_insights', {})
    if insights:
        print(f"\n📊 SEO Insights:")
        print(f"   Search Volume: {insights.get('search_volume_estimate', 'Unknown')}")
        print(f"   Competition: {insights.get('competition_level', 'Unknown')}")
        print(f"   Recommended Focus: {insights.get('recommended_focus', 'All keywords')}")

if __name__ == "__main__":
    # Example usage
    topic = input("Enter your topic: ").strip()
    if topic:
        try:
            keywords = generate_keywords(topic)
            display_keywords(keywords)
            
            # Save to file
            filepath = save_keywords_to_file(keywords, topic)
            print(f"\n✅ Keywords saved to: {filepath}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    else:
        print("❌ Topic is required!") 