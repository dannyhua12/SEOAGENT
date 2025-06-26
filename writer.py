import openai
import os
import json
import re
from dotenv import load_dotenv
from prompts import build_prompt

load_dotenv()

# Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

def clean_json_response(text_output):
    """Clean and extract JSON from OpenAI response"""
    # Try to find JSON in the response
    json_match = re.search(r'\{.*\}', text_output, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # If no JSON found or parsing failed, try parsing the entire response
    try:
        return json.loads(text_output)
    except json.JSONDecodeError:
        return None

def generate_article(keyword, tone="informal", word_count=1000, article_type="guide", model=None, temperature=None):
    """
    Generate an SEO-optimized article using OpenAI
    
    Args:
        keyword (str): Target keyword for the article
        tone (str): Writing tone (formal, informal, conversational, professional)
        word_count (int): Target word count
        article_type (str): Type of article (guide, review, how-to, list, comparison)
        model (str): OpenAI model to use (default: gpt-4)
        temperature (float): Creativity level (0.0-1.0)
    
    Returns:
        dict: Article data in JSON format or None if generation failed
    """
    
    if not openai.api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    
    # Use defaults if not provided
    model = model or DEFAULT_MODEL
    temperature = temperature or DEFAULT_TEMPERATURE
    
    prompt = build_prompt(keyword, tone, word_count, article_type)
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=4000  # Increased for longer articles
        )
        
        text_output = response['choices'][0]['message']['content']
        
        # Try to parse JSON response
        data = clean_json_response(text_output)
        
        if data:
            # Validate required fields
            required_fields = ['article_title', 'article_sections']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"⚠️ Warning: Missing required fields: {missing_fields}")
                print("Raw response:")
                print(text_output)
                return None
            
            return data
        else:
            print("⚠️ Failed to parse JSON response. Raw output:")
            print(text_output)
            return None
            
    except openai.error.AuthenticationError:
        print("❌ Authentication error: Please check your OpenAI API key.")
        return None
    except openai.error.RateLimitError:
        print("❌ Rate limit exceeded: Please wait a moment and try again.")
        return None
    except openai.error.APIError as e:
        print(f"❌ OpenAI API error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
