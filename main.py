from writer import generate_article
from keyword_generator import generate_keywords, display_keywords
from input_handler import get_user_input
from file_saver import save_article_and_keywords
import json
import os

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
                # Save article and keywords using the new module
                json_path, md_path, keywords_path = save_article_and_keywords(data, keywords_data, inputs['topic'])
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
