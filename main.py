from writer import generate_article
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
        "keyword": topic,
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
    
    print(f"\n🎯 Generating article with:")
    print(f"   Keyword: {inputs['keyword']}")
    print(f"   Tone: {inputs['tone']}")
    print(f"   Word count: {inputs['word_count']}")
    print(f"   Article type: {inputs['article_type']}")
    print("\n⏳ Generating article...")
    
    # Generate article
    data = generate_article(
        inputs['keyword'], 
        inputs['tone'], 
        inputs['word_count'], 
        inputs['article_type']
    )

    if data:
        # Create outputs directory if it doesn't exist
        os.makedirs("outputs", exist_ok=True)
        
        slug = inputs['keyword'].lower().replace(" ", "-")
        json_path = f"outputs/article-{slug}.json"
        md_path = f"outputs/article-{slug}.md"

        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)

        with open(md_path, "w") as f:
            f.write(f"# {data['article_title']}\n\n")
            for section in data['article_sections']:
                f.write(f"## {section['heading']}\n{section['content']}\n\n")

        print(f"\n✅ Article saved to:")
        print(f"   📄 {json_path}")
        print(f"   📝 {md_path}")
    else:
        print("❌ Failed to generate article.")

if __name__ == "__main__":
    main()
