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
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

def get_model_context_limit(model_name):
    """Get the context length limit for a given model."""
    model_limits = {
        "gpt-4": 8192,
        "gpt-4-32k": 32768,
        "gpt-4-turbo": 128000,
        "gpt-4-turbo-preview": 128000,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384,
    }
    return model_limits.get(model_name, 8192)  # Default to 8192 if unknown

def calculate_safe_max_tokens(model_name, base_tokens=4000, attempt=0):
    """Calculate a safe max_tokens value that won't exceed context limits."""
    context_limit = get_model_context_limit(model_name)
    
    # Reserve some tokens for the prompt and response overhead
    reserved_tokens = 2000  # Conservative estimate for prompt + overhead
    available_tokens = context_limit - reserved_tokens
    
    # Calculate tokens for this attempt
    attempt_tokens = min(base_tokens + (attempt * 500), available_tokens)
    
    return max(1000, attempt_tokens)  # Ensure minimum of 1000 tokens

def generate_article_with_tools(keyword, tone="informal", word_count=1000, article_type="guide", model=None, temperature=None, keywords_list=None):
    """
    Generate an SEO article using OpenAI tools instead of JSON examples in the prompt.
    This is a more reliable approach than the build_prompt method.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    
    model = model or DEFAULT_MODEL
    temperature = temperature or DEFAULT_TEMPERATURE
    
    # Define the tool schema with proper typing
    tools = [
        {
            "type": "function",
            "function": {
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
                                "required": ["heading", "content"]
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
                                "required": ["question", "answer"]
                            },
                            "description": "Frequently asked questions and answers"
                        },
                        "seo_tips": {
                            "type": "array",
                            "items": {"type": "string", "description": "SEO optimization tip"},
                            "description": "List of SEO optimization tips"
                        }
                    },
                    "required": ["meta_title", "meta_description", "article_title", "target_keyword", "word_count", "article_sections", "faq", "seo_tips"]
                }
            }
        }
    ]
    
    # Build the prompt without JSON examples
    keywords_section = ""
    if keywords_list:
        keywords_str = ", ".join(f'"{kw}"' for kw in keywords_list)
        keywords_section = f"""
- Use ALL of the following keywords naturally throughout the article: {keywords_str}
"""
    
    prompt = f"""
You are an expert SEO content writer. Create a comprehensive, SEO-optimized {article_type} article targeting the keyword: "{keyword}".

CRITICAL REQUIREMENTS:
- Target word count: EXACTLY {word_count} words (±10% tolerance)
- Tone: {tone}
- Include the target keyword naturally throughout the content
{keywords_section}- Create engaging, informative content that provides real value
- Include relevant subheadings for better structure
- Add a FAQ section with common questions about the topic

WORD COUNT BREAKDOWN (MANDATORY):
- Article sections (main content): {int(word_count * 0.7)}-{int(word_count * 0.8)} words
- FAQ section: {int(word_count * 0.15)}-{int(word_count * 0.2)} words  
- SEO tips: {int(word_count * 0.05)}-{int(word_count * 0.1)} words
- Total target: {word_count} words

CONTENT STRUCTURE GUIDELINES:
- Create 4-6 detailed article sections with substantial content
- Each section should be {int(word_count * 0.15)}-{int(word_count * 0.25)} words
- Include 3-5 comprehensive FAQ questions with detailed answers
- Each FAQ answer should be 50-100 words
- Include 3-5 actionable SEO tips

CRITICAL INSTRUCTION: You MUST generate exactly {word_count} words. This is not optional. Write comprehensive, detailed content that thoroughly covers the topic. Do not be brief or superficial. Expand every section with examples, explanations, and detailed information. If you generate fewer than {int(word_count * 0.9)} words, the article will be rejected.

Make sure the content is original, engaging, and provides genuine value to readers while being optimized for search engines.
"""
    
    try:
        messages = [
            {
                "role": "system", 
                "content": f"You are a verbose, comprehensive content writer. Always write detailed, thorough content. Your target is {word_count} words. Never write short or superficial content. Expand every topic with examples, explanations, and detailed information."
            },
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore
            tools=tools,  # type: ignore
            tool_choice={"type": "function", "function": {"name": "generate_seo_article"}},
            temperature=temperature,
            max_tokens=calculate_safe_max_tokens(model, 4000)
        )
        
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            if tool_call and tool_call.function.name == "generate_seo_article":
                data = json.loads(tool_call.function.arguments)
                required_fields = ['article_title', 'article_sections']
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"⚠️ Warning: Missing required fields: {missing_fields}")
                    return None
                
                # Validate word count
                total_content = ""
                if data.get('article_title'):
                    total_content += data['article_title'] + " "
                for section in data.get('article_sections', []):
                    if section.get('heading'):
                        total_content += section['heading'] + " "
                    if section.get('content'):
                        total_content += section['content'] + " "
                for faq in data.get('faq', []):
                    if faq.get('question'):
                        total_content += faq['question'] + " "
                    if faq.get('answer'):
                        total_content += faq['answer'] + " "
                for tip in data.get('seo_tips', []):
                    total_content += tip + " "
                
                actual_word_count = len(total_content.split())
                target_min = int(word_count * 0.8)
                target_max = int(word_count * 1.2)
                
                if actual_word_count < target_min:
                    print(f"❌ Error: Generated article is too short ({actual_word_count} words vs target {word_count} words)")
                    print(f"   The article must be at least {target_min} words. Please try again with a different approach.")
                    return None
                elif actual_word_count > target_max:
                    print(f"⚠️ Warning: Generated article is too long ({actual_word_count} words vs target {word_count} words)")
                    print(f"   The article is {actual_word_count - word_count} words over target, but will be accepted.")
                
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
    Generate keywords using OpenAI tools instead of JSON examples in the prompt.
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
    
    # Define the tool schema with proper typing
    tools = [
        {
            "type": "function",
            "function": {
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
                            "description": "Keywords organized by type"
                        },
                        "seo_insights": {
                            "type": "object",
                            "properties": {
                                "search_volume_estimate": {"type": "string", "description": "Estimated search volume (high/medium/low)"},
                                "competition_level": {"type": "string", "description": "Competition level (high/medium/low)"},
                                "recommended_focus": {"type": "string", "description": "Recommended keywords to focus on"}
                            },
                            "description": "SEO insights and recommendations"
                        }
                    },
                    "required": ["topic", "total_keywords", "keywords", "seo_insights"]
                }
            }
        }
    ]
    
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert SEO specialist who generates high-quality, searchable keywords for content optimization."},
                {"role": "user", "content": prompt}
            ],
            tools=tools,  # type: ignore
            tool_choice={"type": "function", "function": {"name": "generate_seo_keywords"}},
            temperature=0.7,
            max_tokens=1000
        )
        
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            if tool_call and tool_call.function.name == "generate_seo_keywords":
                keywords_data = json.loads(tool_call.function.arguments)
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
    Backward compatibility function that uses the new tool-based approach.
    This replaces the old function that used JSON examples in prompts.
    """
    return generate_article_with_tools(keyword, tone, word_count, article_type, model, temperature, keywords_list)

def generate_keywords(topic, keyword_count=15, keyword_types=None):
    """
    Backward compatibility function that uses the new tool-based approach.
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