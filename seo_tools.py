# seo_tools.py
"""
Core SEO tools: keyword generation, article generation, file saving, and prompt building.
"""

import os
import json
import openai
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()

# --- Article Generation ---



def generate_article_with_tools(keyword, tone="informal", article_type="guide", model=None, keywords_list=None):
    """
    Generate an SEO article using OpenAI Responses API with function calling.
    This is a more reliable approach than the build_prompt method.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    
    # Use gpt-4.1 as default for Responses API
    model = model or "gpt-4.1"
    
    # Define the tool schema for Responses API
    tools = [{
        "type": "function",
        "name": "generate_seo_article",
        "description": "Generate a comprehensive SEO-optimized article with all required components",
        "parameters": {
            "type": "object",
            "properties": {
                "meta_title": {"type": "string", "description": "SEO-optimized title (50-60 characters)"},
                "meta_description": {"type": "string", "description": "Compelling description (150-160 characters)"},
                "article_title": {"type": "string", "description": "Engaging main title"},
                "target_keyword": {"type": "string", "description": "The target keyword for this article"},
                "word_count": {"type": "integer", "description": "Target word count for the article"},
                "article_sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "heading": {"type": "string", "description": "H2 heading for the section"},
                            "content": {"type": "string", "description": "Well-written content with natural keyword usage"}
                        },
                        "required": ["heading", "content"],
                        "additionalProperties": False
                    },
                    "description": "Article sections with headings and content"
                },
                "faq": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string", "description": "Common question about the topic"},
                            "answer": {"type": "string", "description": "Clear, helpful answer"}
                        },
                        "required": ["question", "answer"],
                        "additionalProperties": False
                    },
                    "description": "Frequently asked questions and answers"
                },
                "seo_tips": {
                    "type": "array",
                    "items": {"type": "string", "description": "SEO optimization tip"},
                    "description": "List of SEO optimization tips"
                }
            },
            "required": ["meta_title", "meta_description", "article_title", "target_keyword", "word_count", "article_sections", "faq", "seo_tips"],
            "additionalProperties": False
        },
        "strict": True
    }]
    
    # Build the prompt without JSON examples
    keywords_section = ""
    if keywords_list:
        keywords_str = ", ".join(f'"{kw}"' for kw in keywords_list)
        keywords_section = f"""
- Use ALL of the following keywords naturally throughout the article: {keywords_str}
"""
    
    prompt = f"""
Generate a comprehensive SEO-optimized article about "{keyword}".

Article Requirements:
- Tone: {tone}
- Article type: {article_type}
{keywords_section}

The article must include:
1. SEO-optimized meta title (50-60 characters)
2. Compelling meta description (150-160 characters)
3. Engaging article title
4. Well-structured content with H2 headings
5. Natural keyword usage throughout
6. FAQ section with relevant questions
7. SEO optimization tips

Make sure the content is:
- Comprehensive and detailed
- Well-researched and accurate
- Engaging and readable
- Optimized for search engines
"""

    try:
        # Use Responses API
        response = client.responses.create(
            model=model,
            input=[{"role": "user", "content": prompt}],
            tools=tools  # type: ignore
        )
        
        # Handle function calls from Responses API
        if response.output and len(response.output) > 0:
            tool_call = response.output[0]
            if tool_call.type == "function_call" and tool_call.name == "generate_seo_article":
                data = json.loads(tool_call.arguments)
                required_fields = ['article_title', 'article_sections']
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"⚠️ Warning: Missing required fields: {missing_fields}")
                    return None
                
                # Return the generated article data
                
                return data
            else:
                print("⚠️ No function call response received")
                return None
        else:
            print("⚠️ No tool calls in response")
            return None
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    
    return None

# --- Keyword Generation ---
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_keywords_with_tools(topic, keyword_count=15, keyword_types=None):
    """
    Generate keywords using OpenAI Responses API with function calling.
    This is a more reliable approach than the original generate_keywords method.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    if keyword_types is None:
        keyword_types = [
            "primary_keywords",
            "long_tail_keywords", 
            "question_keywords",
            "local_keywords",
            "related_keywords"
        ]
    
    # Define the tool schema for Responses API
    tools = [{
        "type": "function",
        "name": "generate_seo_keywords",
        "description": "Generate SEO keywords for content optimization",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The main topic for keyword generation"},
                "total_keywords": {"type": "integer", "description": "Total number of keywords generated"},
                "keywords": {
                    "type": "object",
                    "properties": {
                        "primary_keywords": {"type": "array", "items": {"type": "string"}},
                        "long_tail_keywords": {"type": "array", "items": {"type": "string"}},
                        "question_keywords": {"type": "array", "items": {"type": "string"}},
                        "local_keywords": {"type": "array", "items": {"type": "string"}},
                        "related_keywords": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["primary_keywords", "long_tail_keywords", "question_keywords", "local_keywords", "related_keywords"],
                    "description": "Keywords organized by type",
                    "additionalProperties": False
                },
                "seo_insights": {
                    "type": "object",
                    "properties": {
                        "search_volume_estimate": {"type": "string", "description": "Estimated search volume (high/medium/low)"},
                        "competition_level": {"type": "string", "description": "Competition level (high/medium/low)"},
                        "recommended_focus": {"type": "string", "description": "Recommended keywords to focus on"}
                    },
                    "required": ["search_volume_estimate", "competition_level", "recommended_focus"],
                    "description": "SEO insights and recommendations",
                    "additionalProperties": False
                }
            },
            "required": ["topic", "total_keywords", "keywords", "seo_insights"],
            "additionalProperties": False
        },
        "strict": True
    }]
    
    # Build the prompt without JSON examples
    keyword_type_descriptions = {
        "primary_keywords": "main target keywords (1-3 words)",
        "long_tail_keywords": "longer, more specific phrases (4+ words)",
        "question_keywords": "keywords that start with what, how, why, when, where, etc.",
        "local_keywords": "keywords with location modifiers",
        "related_keywords": "semantically related terms and synonyms"
    }
    
    types_section = ""
    for keyword_type in keyword_types:
        if keyword_type in keyword_type_descriptions:
            types_section += f"- {keyword_type}: {keyword_type_descriptions[keyword_type]}\n"
    
    prompt = f"""
Generate SEO keywords for the topic: "{topic}"

Requirements:
- Generate {keyword_count} keywords total
- Focus on high-search-volume, low-competition keywords
- Include a mix of different keyword types
- Keywords should be relevant and valuable for SEO

Keyword types to include:
{types_section}

Make sure all keywords are:
- Relevant to the topic
- Searchable and commonly used
- Optimized for SEO
- Include the main topic naturally
"""
    
    try:
        # Use Responses API
        response = client.responses.create(
            model="gpt-4.1",
            input=[{"role": "user", "content": prompt}],
            tools=tools  # type: ignore
        )
        
        # Handle function calls from Responses API
        if response.output and len(response.output) > 0:
            tool_call = response.output[0]
            if tool_call.type == "function_call" and tool_call.name == "generate_seo_keywords":
                keywords_data = json.loads(tool_call.arguments)
                return keywords_data
            else:
                print("⚠️ No function call response received")
                return None
        else:
            print("⚠️ No tool calls in response")
            return None
            
    except Exception as e:
        raise Exception(f"Error generating keywords: {str(e)}")

# --- Backward Compatibility Functions ---
def generate_article_with_functions(keyword, tone="informal", word_count=1000, article_type="guide", model=None, temperature=None, keywords_list=None):
    """
    Backward compatibility function that uses the new Responses API approach.
    This replaces the old function that used JSON examples in prompts.
    """
    return generate_article_with_tools(keyword, tone, article_type, model, keywords_list)

def generate_keywords(topic, keyword_count=15, keyword_types=None):
    """
    Backward compatibility function that uses the new Responses API approach.
    This replaces the old function that used JSON examples in prompts.
    """
    return generate_keywords_with_tools(topic, keyword_count, keyword_types)

def build_keyword_prompt(topic, keyword_count, keyword_types):
    keyword_type_descriptions = {
        "primary_keywords": "main target keywords (1-3 words)",
        "long_tail_keywords": "longer, more specific phrases (4+ words)",
        "question_keywords": "keywords that start with what, how, why, when, where, etc.",
        "local_keywords": "keywords with location modifiers",
        "related_keywords": "semantically related terms and synonyms"
    }
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

def display_keywords(keywords_data):
    print(f"\n🎯 Keywords for: {keywords_data.get('topic', 'Unknown Topic')}")
    print("=" * 50)
    keywords = keywords_data.get('keywords', {})
    for keyword_type, keyword_list in keywords.items():
        if keyword_list:
            print(f"\n📌 {keyword_type.replace('_', ' ').title()}:")
            for i, keyword in enumerate(keyword_list, 1):
                print(f"   {i}. {keyword}")
    insights = keywords_data.get('seo_insights', {})
    if insights:
        print(f"\n📊 SEO Insights:")
        print(f"   Search Volume: {insights.get('search_volume_estimate', 'Unknown')}")
        print(f"   Competition: {insights.get('competition_level', 'Unknown')}")
        print(f"   Recommended Focus: {insights.get('recommended_focus', 'All keywords')}")

def get_flat_keywords_list(topic, keyword_count=15, keyword_types=None):
    data = generate_keywords(topic, keyword_count, keyword_types)
    if data is None:
        return {"topic": topic, "keywords": []}
    flat = []
    for kw_list in data.get('keywords', {}).values():
        flat.extend(kw_list)
    return {"topic": topic, "keywords": flat}

def save_keywords_to_file(keywords_data, topic, output_dir=None):
    if output_dir is None:
        output_dir = os.path.expanduser('~/SEO articles')
    os.makedirs(output_dir, exist_ok=True)
    slug = topic.lower().replace(" ", "-").replace("/", "-")
    filename = f"keywords-{slug}.json"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(keywords_data, f, indent=2, ensure_ascii=False)
    return filepath

def save_article_and_keywords(data, keywords_data, topic):
    output_dir = os.path.expanduser('~/SEO articles')
    os.makedirs(output_dir, exist_ok=True)
    slug = topic.lower().replace(" ", "-").replace("/", "-")
    json_path = os.path.join(output_dir, f"article-{slug}.json")
    md_path = os.path.join(output_dir, f"article-{slug}.md")
    keywords_path = os.path.join(output_dir, f"keywords-{slug}.json")
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(md_path, "w", encoding='utf-8') as f:
        f.write(f"# {data['article_title']}\n\n")
        for section in data['article_sections']:
            f.write(f"## {section['heading']}\n{section['content']}\n\n")
    with open(keywords_path, "w", encoding='utf-8') as f:
        json.dump(keywords_data, f, indent=2, ensure_ascii=False)
    return json_path, md_path, keywords_path 