# seo_tools.py
"""
Core SEO tools: keyword generation, article generation, file saving, and prompt building.
"""

import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

# --- Prompt Building ---
def build_prompt(keyword, tone, word_count, article_type, keywords_list=None):
    keywords_section = ""
    if keywords_list:
        keywords_str = ", ".join(f'"{kw}"' for kw in keywords_list)
        keywords_section = f"""
- Use ALL of the following keywords naturally throughout the article: {keywords_str}
"""
    return f"""
You are an expert SEO content writer. Create a comprehensive, SEO-optimized {article_type} article targeting the keyword: "{keyword}".

Requirements:
- Target word count: {word_count} words
- Tone: {tone}
- Include the target keyword naturally throughout the content
{keywords_section}- Create engaging, informative content that provides real value
- Include relevant subheadings for better structure
- Add a FAQ section with common questions about the topic

Return the result in valid JSON format like this:

{{
  "meta_title": "SEO-optimized title (50-60 characters)",
  "meta_description": "Compelling description (150-160 characters)",
  "article_title": "Engaging main title",
  "target_keyword": "{keyword}",
  "word_count": {word_count},
  "article_sections": [
    {{
      "heading": "H2 heading",
      "content": "Well-written content with natural keyword usage..."
    }}
  ],
  "faq": [
    {{
      "question": "Common question about the topic",
      "answer": "Clear, helpful answer"
    }}
  ],
  "seo_tips": [
    "SEO optimization tip 1",
    "SEO optimization tip 2"
  ]
}}

Make sure the content is original, engaging, and provides genuine value to readers while being optimized for search engines.
"""

# --- Keyword Generation ---
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def generate_keywords(topic, keyword_count=15, keyword_types=None):
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
    prompt = build_keyword_prompt(topic, keyword_count, keyword_types)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert SEO specialist who generates high-quality, searchable keywords for content optimization."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        content = response.choices[0].message.content
        if content:
            content = content.strip()
        else:
            raise ValueError("Empty response from OpenAI")
        try:
            keywords_data = json.loads(content)
            return keywords_data
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                keywords_data = json.loads(json_match.group())
                return keywords_data
            else:
                raise ValueError("Failed to parse JSON response from OpenAI")
    except Exception as e:
        raise Exception(f"Error generating keywords: {str(e)}")

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

# --- Article Generation ---
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

def generate_article_with_functions(keyword, tone="informal", word_count=1000, article_type="guide", model=None, temperature=None, keywords_list=None):
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    model = model or DEFAULT_MODEL
    temperature = temperature or DEFAULT_TEMPERATURE
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
    keywords_section = ""
    if keywords_list:
        keywords_str = ", ".join(f'"{kw}"' for kw in keywords_list)
        keywords_section = f"""
- Use ALL of the following keywords naturally throughout the article: {keywords_str}
"""
    prompt = f"""
You are an expert SEO content writer. Create a comprehensive, SEO-optimized {article_type} article targeting the keyword: "{keyword}".

Requirements:
- Target word count: {word_count} words
- Tone: {tone}
- Include the target keyword naturally throughout the content
{keywords_section}- Create engaging, informative content that provides real value
- Include relevant subheadings for better structure
- Add a FAQ section with common questions about the topic

Make sure the content is original, engaging, and provides genuine value to readers while being optimized for search engines.
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "generate_seo_article"}},
            temperature=temperature,
            max_tokens=4000
        )
        tool_call = response.choices[0].message.tool_calls[0]
        if tool_call and tool_call.function.name == "generate_seo_article":
            data = json.loads(tool_call.function.arguments)
            required_fields = ['article_title', 'article_sections']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                print(f"⚠️ Warning: Missing required fields: {missing_fields}")
                return None
            return data
        else:
            print("⚠️ No function call response received")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

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