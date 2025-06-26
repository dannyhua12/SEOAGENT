def build_prompt(keyword, tone, word_count, article_type):
    return f"""
You are an expert SEO content writer. Create a comprehensive, SEO-optimized {article_type} article targeting the keyword: "{keyword}".

Requirements:
- Target word count: {word_count} words
- Tone: {tone}
- Include the target keyword naturally throughout the content
- Create engaging, informative content that provides real value
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
