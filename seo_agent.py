#!/usr/bin/env python3
"""
SEO Agent - Interactive CLI tool for generating SEO-optimized articles and keywords
"""

import click
import os
import json
from writer import generate_article
from keyword_generator import generate_keywords, save_keywords_to_file, display_keywords, get_flat_keywords_list
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@click.group()
def cli():
    """SEO Agent - Generate SEO-optimized articles and keywords"""
    pass

@cli.command()
@click.option('--keyword', '-k', prompt='Enter your target topic', help='The main topic to target')
@click.option('--tone', '-t', default='informal', type=click.Choice(['formal', 'informal', 'conversational', 'professional']), help='Tone of the article')
@click.option('--word-count', '-w', default=1200, type=int, help='Target word count for the article')
@click.option('--article-type', '-a', default='guide', type=click.Choice(['guide', 'review', 'how-to', 'list', 'comparison']), help='Type of article to generate')
def article(keyword, tone, word_count, article_type):
    """Generate SEO-optimized articles using OpenAI"""
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        click.echo("❌ Error: OPENAI_API_KEY not found in environment variables.")
        click.echo("Please create a .env file with your OpenAI API key:")
        click.echo("OPENAI_API_KEY=your_api_key_here")
        return
    
    # Set output directory to ~/SEO articles
    output_dir = os.path.expanduser('~/SEO articles')
    os.makedirs(output_dir, exist_ok=True)
    
    click.echo(f"\n🚀 Generating SEO article...")
    click.echo(f"Topic: {keyword}")
    click.echo(f"Tone: {tone}")
    click.echo(f"Word count: {word_count}")
    click.echo(f"Article type: {article_type}")
    click.echo("-" * 50)
    
    try:
        # Generate flat keywords list for the topic
        flat_keywords_obj = get_flat_keywords_list(keyword, 15)
        flat_keywords = flat_keywords_obj["keywords"]
        
        # Generate the article using the keywords
        data = generate_article(keyword, tone, word_count, article_type, keywords_list=flat_keywords)
        
        if data:
            # Create filenames
            slug = keyword.lower().replace(" ", "-").replace("/", "-")
            json_path = os.path.join(output_dir, f"article-{slug}.json")
            md_path = os.path.join(output_dir, f"article-{slug}.md")
            
            # Save JSON data with UTF-8 encoding
            with open(json_path, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Save Markdown file with UTF-8 encoding
            with open(md_path, "w", encoding='utf-8') as f:
                f.write(f"# {data.get('article_title', 'Article Title')}\n\n")
                
                # Add meta information
                if 'meta_title' in data:
                    f.write(f"**Meta Title:** {data['meta_title']}\n\n")
                if 'meta_description' in data:
                    f.write(f"**Meta Description:** {data['meta_description']}\n\n")
                
                # Add article sections
                for section in data.get('article_sections', []):
                    f.write(f"## {section['heading']}\n{section['content']}\n\n")
                
                # Add FAQ section
                if 'faq' in data and data['faq']:
                    f.write("## Frequently Asked Questions\n\n")
                    for faq in data['faq']:
                        f.write(f"**Q: {faq['question']}**\n")
                        f.write(f"A: {faq['answer']}\n\n")
                
                # Add SEO tips
                if 'seo_tips' in data and data['seo_tips']:
                    f.write("## SEO Optimization Tips\n\n")
                    for tip in data['seo_tips']:
                        f.write(f"- {tip}\n")
                    f.write("\n")
            
            click.echo(f"\n✅ Article generated successfully!")
            click.echo(f"📄 JSON: {json_path}")
            click.echo(f"📝 Markdown: {md_path}")
            
            # Show article stats
            actual_word_count = len(data.get('article_title', '').split()) + sum(
                len(section.get('content', '').split()) for section in data.get('article_sections', [])
            )
            click.echo(f"📊 Word count: ~{actual_word_count} words")
            
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
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        click.echo("❌ Error: OPENAI_API_KEY not found in environment variables.")
        click.echo("Please create a .env file with your OpenAI API key:")
        click.echo("OPENAI_API_KEY=your_api_key_here")
        return
    
    # Set output directory to ~/SEO articles
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
        # Convert types tuple to list, or use None for all types
        keyword_types = list(types) if types else None
        
        # Generate keywords
        keywords_data = generate_keywords(topic, count, keyword_types)
        
        if keywords_data:
            # Display keywords
            display_keywords(keywords_data)
            
            # Save to file
            filepath = save_keywords_to_file(keywords_data, topic, output_dir)
            click.echo(f"\n✅ Keywords saved to: {filepath}")
            
            # Show summary
            total_keywords = sum(len(keyword_list) for keyword_list in keywords_data.get('keywords', {}).values())
            click.echo(f"📊 Total keywords generated: {total_keywords}")
            
        else:
            click.echo("❌ Failed to generate keywords. Please check your OpenAI API key and try again.")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        click.echo("Please check your OpenAI API key and internet connection.")

def main():
    """Main entry point for backward compatibility"""
    cli()

if __name__ == '__main__':
    main()
