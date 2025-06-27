from writer import generate_article
from keyword_generator import generate_keywords, display_keywords
import json
import os

def get_user_input():
    """Get user input for article generation parameters"""
    print("🚀 SEO Article Generator")
    print("=" * 40)
    
    # Get topic
    topic = input("Enter your topic: ").strip()
    if not topic:
        print("❌ Topic is required!")
        return None
    
    # Get tone with validation
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
    
    # Get word count with validation
    try:
        word_count = int(input("Enter target word count (e.g., 800, 1200, 1500): ").strip())
        if word_count < 300 or word_count > 5000:
            print("❌ Word count should be between 300 and 5000 words.")
            return None
    except ValueError:
        print("❌ Please enter a valid number for word count.")
        return None
    
    # Get article type with validation
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
    
    return {
        "topic": topic,
        "tone": tone,
        "word_count": word_count,
        "article_type": article_type
    }

def main():
    # Get user inputs
    inputs = get_user_input()
    if not inputs:
        print("❌ Invalid inputs. Please try again.")
        return
    
    print(f"\n🎯 Topic: {inputs['topic']}")
    print(f"📝 Tone: {inputs['tone']}")
    print(f"📊 Word count: {inputs['word_count']}")
    print(f"📄 Article type: {inputs['article_type']}")
    
    # Step 1: Generate keywords
    print("\n🔍 Generating keywords...")
    try:
        keywords_data = generate_keywords(inputs['topic'], 15)
        
        if keywords_data:
            # Display keywords in terminal
            display_keywords(keywords_data)
            
            # Get primary keywords for article generation
            primary_keywords = keywords_data.get('keywords', {}).get('primary_keywords', [])
            if primary_keywords:
                # Use the first primary keyword for article generation
                article_keyword = primary_keywords[0]
                print(f"\n📝 Using keyword for article: '{article_keyword}'")
            else:
                # Fallback to original topic
                article_keyword = inputs['topic']
                print(f"\n📝 Using original topic for article: '{article_keyword}'")
            
            # Step 2: Generate article
            print(f"\n⏳ Generating article...")
            data = generate_article(
                article_keyword, 
                inputs['tone'], 
                inputs['word_count'], 
                inputs['article_type']
            )

            if data:
                # Set output directory to ~/SEO articles
                output_dir = os.path.expanduser('~/SEO articles')
                os.makedirs(output_dir, exist_ok=True)
                
                slug = inputs['topic'].lower().replace(" ", "-").replace("/", "-")
                json_path = os.path.join(output_dir, f"article-{slug}.json")
                md_path = os.path.join(output_dir, f"article-{slug}.md")
                keywords_path = os.path.join(output_dir, f"keywords-{slug}.json")

                # Save article
                with open(json_path, "w", encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                with open(md_path, "w", encoding='utf-8') as f:
                    f.write(f"# {data['article_title']}\n\n")
                    for section in data['article_sections']:
                        f.write(f"## {section['heading']}\n{section['content']}\n\n")

                # Save keywords
                with open(keywords_path, "w", encoding='utf-8') as f:
                    json.dump(keywords_data, f, indent=2, ensure_ascii=False)

                print(f"\n✅ Files saved to:")
                print(f"   📄 Article JSON: {json_path}")
                print(f"   📝 Article Markdown: {md_path}")
                print(f"   🔍 Keywords JSON: {keywords_path}")
            else:
                print("❌ Failed to generate article.")
        else:
            print("❌ Failed to generate keywords. Please check your OpenAI API key and try again.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your OpenAI API key and internet connection.")

if __name__ == "__main__":
    main()
