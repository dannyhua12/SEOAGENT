import os
import json

def save_article_and_keywords(data, keywords_data, topic):
    """Save article and keywords to files in ~/SEO articles directory."""
    output_dir = os.path.expanduser('~/SEO articles')
    os.makedirs(output_dir, exist_ok=True)
    
    slug = topic.lower().replace(" ", "-").replace("/", "-")
    json_path = os.path.join(output_dir, f"article-{slug}.json")
    md_path = os.path.join(output_dir, f"article-{slug}.md")
    keywords_path = os.path.join(output_dir, f"keywords-{slug}.json")

    # Save article JSON
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save article Markdown
    with open(md_path, "w", encoding='utf-8') as f:
        f.write(f"# {data['article_title']}\n\n")
        for section in data['article_sections']:
            f.write(f"## {section['heading']}\n{section['content']}\n\n")

    # Save keywords JSON
    with open(keywords_path, "w", encoding='utf-8') as f:
        json.dump(keywords_data, f, indent=2, ensure_ascii=False)

    return json_path, md_path, keywords_path 