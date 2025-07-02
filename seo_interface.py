# seo_interface.py
"""
User interfaces for SEO tools: CLI (Click) and interactive terminal mode.
"""

import os
import click
from seo_tools import (
    generate_keywords_with_tools, display_keywords, get_flat_keywords_list, save_keywords_to_file,
    generate_article_with_tools, save_article_and_keywords
)
import json



def get_user_input():
    print("🚀 SEO Article Generator")
    print("=" * 40)
    topic = input("Enter your topic: ").strip()
    if not topic:
        print("❌ Topic is required!")
        return None
    print("\n📝 Available tones:")
    print("- formal: Professional and authoritative")
    print("- informal: Casual and friendly")
    print("- conversational: Chatty and engaging")
    print("- professional: Business-like and polished")
    tone = input("Enter tone (formal/informal/conversational/professional): ").strip().lower()
    valid_tones = ["formal", "informal", "conversational", "professional"]
    if tone not in valid_tones:
        print(f"❌ Invalid tone. Please choose from: {', '.join(valid_tones)}")
        return None

    print("\n📄 Available article types:")
    print("- guide: How-to guide or tutorial")
    print("- review: Product or service review")
    print("- how-to: Step-by-step instructions")
    print("- list: Listicle or numbered content")
    print("- comparison: Compare different options")
    article_type = input("Enter article type (guide/review/how-to/list/comparison): ").strip().lower()
    valid_types = ["guide", "review", "how-to", "list", "comparison"]
    if article_type not in valid_types:
        print(f"❌ Invalid article type. Please choose from: {', '.join(valid_types)}")
        return None
    
    # Use gpt-4.1 as default for Responses API
    selected_model = 'gpt-4.1'
    
    return {
        "topic": topic,
        "tone": tone,
        "article_type": article_type,
        "model": selected_model
    }

# --- Interactive Terminal Mode ---
def interactive_main():
    inputs = get_user_input()
    if not inputs:
        print("❌ Invalid inputs. Please try again.")
        return
    print(f"\n🎯 Topic: {inputs['topic']}")
    print(f"📝 Tone: {inputs['tone']}")
    print(f"📄 Article type: {inputs['article_type']}")
    print(f"🤖 Model: {inputs['model']}")
    
    # Show model info
    print(f"🤖 Model: {inputs['model']}")
    
    print("\n🔍 Generating keywords...")
    try:
        keywords_data = generate_keywords_with_tools(inputs['topic'], 15)
        if keywords_data:
            display_keywords(keywords_data)
            primary_keywords = keywords_data.get('keywords', {}).get('primary_keywords', [])
            if primary_keywords:
                article_keyword = primary_keywords[0]
                print(f"\n📝 Using keyword for article: '{article_keyword}'")
            else:
                article_keyword = inputs['topic']
                print(f"\n📝 Using original topic for article: '{article_keyword}'")
            print(f"\n⏳ Generating article...")
            data = generate_article_with_tools(
                article_keyword,
                inputs['tone'],
                inputs['article_type'],
                model=inputs['model']
            )
            if data:
                json_path, md_path, keywords_path = save_article_and_keywords(data, keywords_data, inputs['topic'])
                print(f"\n✅ Files saved to:")
                print(f"   📄 Article JSON: {json_path}")
                print(f"   📝 Article Markdown: {md_path}")
                print(f"   🔍 Keywords JSON: {keywords_path}")
                
                print(f"✅ Article generated successfully!")
            else:
                print("❌ Failed to generate article.")
        else:
            print("❌ Failed to generate keywords. Please check your OpenAI API key and try again.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your OpenAI API key and internet connection.")

# --- CLI Mode (Click) ---
@click.group()
def cli():
    """SEO Agent - Generate SEO-optimized articles and keywords"""
    pass

@cli.command()
@click.option('--keyword', '-k', prompt='Enter your target topic', help='The main topic to target')
@click.option('--tone', '-t', default='informal', type=click.Choice(['formal', 'informal', 'conversational', 'professional']), help='Tone of the article')

@click.option('--article-type', '-a', default='guide', type=click.Choice(['guide', 'review', 'how-to', 'list', 'comparison']), help='Type of article to generate')
@click.option('--model', '-m', default='gpt-4', type=click.Choice(['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo-16k']), help='OpenAI model to use')
def article(keyword, tone, article_type, model):
    """Generate SEO-optimized articles using OpenAI"""
    if not os.getenv("OPENAI_API_KEY"):
        click.echo("❌ Error: OPENAI_API_KEY not found in environment variables.")
        click.echo("Please create a .env file with your OpenAI API key:")
        click.echo("OPENAI_API_KEY=your_api_key_here")
        return
    output_dir = os.path.expanduser('~/SEO articles')
    os.makedirs(output_dir, exist_ok=True)
    click.echo(f"\n🚀 Generating SEO article...")
    click.echo(f"Topic: {keyword}")
    click.echo(f"Tone: {tone}")
    click.echo(f"Article type: {article_type}")
    click.echo(f"Model: {model}")
    
    # Show model info
    click.echo(f"Model: {model}")
    
    click.echo("-" * 50)
    try:
        flat_keywords_obj = get_flat_keywords_list(keyword, 15)
        flat_keywords = flat_keywords_obj["keywords"]
        data = generate_article_with_tools(keyword, tone, article_type, keywords_list=flat_keywords, model=model)
        if data:
            slug = keyword.lower().replace(" ", "-").replace("/", "-")
            json_path = os.path.join(output_dir, f"article-{slug}.json")
            md_path = os.path.join(output_dir, f"article-{slug}.md")
            with open(json_path, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            with open(md_path, "w", encoding='utf-8') as f:
                f.write(f"# {data.get('article_title', 'Article Title')}\n\n")
                if 'meta_title' in data:
                    f.write(f"**Meta Title:** {data['meta_title']}\n\n")
                if 'meta_description' in data:
                    f.write(f"**Meta Description:** {data['meta_description']}\n\n")
                for section in data.get('article_sections', []):
                    f.write(f"## {section['heading']}\n{section['content']}\n\n")
                if 'faq' in data and data['faq']:
                    f.write("## Frequently Asked Questions\n\n")
                    for faq in data['faq']:
                        f.write(f"**Q: {faq['question']}**\n")
                        f.write(f"A: {faq['answer']}\n\n")
                if 'seo_tips' in data and data['seo_tips']:
                    f.write("## SEO Optimization Tips\n\n")
                    for tip in data['seo_tips']:
                        f.write(f"- {tip}\n")
                    f.write("\n")
            click.echo(f"\n✅ Article generated successfully!")
            click.echo(f"📄 JSON: {json_path}")
            click.echo(f"📝 Markdown: {md_path}")
            
            click.echo(f"✅ Article generated successfully!")
        else:
            click.echo("❌ Failed to generate article. Please check your OpenAI API key and try again.")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        click.echo("Please check your OpenAI API key and internet connection.")

@cli.command()
@click.option('--topic', '-t', prompt='Enter your topic', help='The topic to generate keywords for')
@click.option('--count', '-c', default=15, type=int, help='Number of keywords to generate')
@click.option('--types', '-y', multiple=True, 
              type=click.Choice(['primary_keywords', 'long_tail_keywords', 'question_keywords', 'local_keywords', 'related_keywords']),
              help='Types of keywords to generate (can specify multiple)')
def keywords(topic, count, types):
    """Generate SEO keywords for a given topic using chat"""
    if not os.getenv("OPENAI_API_KEY"):
        click.echo("❌ Error: OPENAI_API_KEY not found in environment variables.")
        click.echo("Please create a .env file with your OpenAI API key:")
        click.echo("OPENAI_API_KEY=your_api_key_here")
        return
    output_dir = os.path.expanduser('~/SEO articles')
    os.makedirs(output_dir, exist_ok=True)
    click.echo(f"\n🔍 Generating SEO keywords...")
    click.echo(f"Topic: {topic}")
    click.echo(f"Keyword count: {count}")
    if types:
        click.echo(f"Keyword types: {', '.join(types)}")
    else:
        click.echo("Keyword types: All types")
    click.echo("-" * 50)
    try:
        keyword_types = list(types) if types else None
        keywords_data = generate_keywords_with_tools(topic, count, keyword_types)
        if keywords_data:
            display_keywords(keywords_data)
            filepath = save_keywords_to_file(keywords_data, topic, output_dir)
            click.echo(f"\n✅ Keywords saved to: {filepath}")
            total_keywords = sum(len(keyword_list) for keyword_list in keywords_data.get('keywords', {}).values())
            click.echo(f"📊 Total keywords generated: {total_keywords}")
        else:
            click.echo("❌ Failed to generate keywords. Please check your OpenAI API key and try again.")
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        click.echo("Please check your OpenAI API key and internet connection.")

def main():
    interactive_main()

if __name__ == "__main__":
    main() 