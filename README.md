# SEO Agent

An intelligent SEO content generation tool powered by OpenAI that creates high-quality, SEO-optimized articles and generates targeted keywords based on your topics.

## Features

- 🎯 **Keyword-focused content** - Optimized for your target keywords
- 🔍 **Keyword generation** - Generate SEO keywords for any topic using chat
- 📝 **Multiple article types** - Guides, reviews, how-to articles, lists, and comparisons
- 🎨 **Flexible tone options** - Formal, informal, conversational, or professional
- 📊 **SEO optimization** - Meta titles, descriptions, and structured content
- 📁 **Multiple output formats** - JSON and Markdown files
- 🔧 **Easy CLI interface** - Simple command-line tool for quick article and keyword generation
- 🤖 **Smart model selection** - Automatically choose the right model for your article length
- 📏 **Accurate word counting** - Count all content including FAQ and SEO tips
- ⚡ **Single-attempt generation** - Powerful prompts ensure correct word count on first try

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up OpenAI API Key

Create a `.env` file in the project root:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model configuration
OPENAI_MODEL=gpt-4
TEMPERATURE=0.7
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

### 3. Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## Usage

### Interactive CLI Tool (Recommended)

```bash
python seo_agent.py
```

This will prompt you for:
- **Topic**: Your target SEO keyword
- **Tone**: Writing style (formal, informal, conversational, professional)
- **Word count**: Target article length
- **Article type**: Guide, review, how-to, list, or comparison

### Generate SEO Keywords

Use the keyword generation feature to get targeted SEO keywords for any topic:

```bash
# Generate keywords for a topic
python seo_agent.py keywords --topic "digital marketing"

# Specify number of keywords
python seo_agent.py keywords --topic "weight loss" --count 20

# Generate specific types of keywords
python seo_agent.py keywords --topic "coffee brewing" --types primary_keywords --types long_tail_keywords

# Short options
python seo_agent.py keywords -t "yoga for beginners" -c 25 -y question_keywords -y local_keywords
```

### Standalone Keyword Generator

For keyword generation only:

```bash
python generate_keywords.py
```

This provides an interactive interface for keyword generation without the full CLI framework.

### Alternative: Main Script

You can also use the main script:

```bash
python main.py
```

This provides the same functionality as `seo_agent.py` and allows you to add your own custom prompts along the way.

### Command Line Options

```bash
# Basic usage with prompts
python seo_agent.py

# Generate article with all options
python seo_agent.py article --keyword "best protein powder" --tone informal --word-count 1500 --article-type guide

# Generate keywords with all options
python seo_agent.py keywords --topic "digital marketing" --count 20 --types primary_keywords --types long_tail_keywords

# Short options for article
python seo_agent.py article -k "digital marketing tips" -t professional -w 2000 -a how-to

# Short options for keywords
python seo_agent.py keywords -t "seo strategies" -c 15 -y question_keywords
```

### Programmatic Usage

```python
from writer import generate_article

# Generate an article
data = generate_article(
    keyword="best protein powder for beginners",
    tone="informal",
    word_count=1200,
    article_type="guide"
)

if data:
    print(f"Article title: {data['article_title']}")
    print(f"Meta description: {data['meta_description']}")
```

## Output

The tool generates two files for each article:

1. **JSON file** (`article-{keyword}.json`) - Structured data with all article components
2. **Markdown file** (`article-{keyword}.md`) - Formatted article ready for publishing

### Keyword Generation Output

For keyword generation, the tool creates:

1. **JSON file** (`keywords-{topic}.json`) - Structured data with all generated keywords

### Article Structure

Each generated article includes:

- **Meta title** - SEO-optimized title (50-60 characters)
- **Meta description** - Compelling description (150-160 characters)
- **Article title** - Engaging main headline
- **Article sections** - Well-structured content with H2 headings
- **FAQ section** - Common questions and answers
- **SEO tips** - Optimization recommendations

### Keyword Structure

Each generated keyword set includes:

- **Primary keywords** - Main target keywords (1-3 words)
- **Long-tail keywords** - Longer, specific phrases (4+ words)
- **Question keywords** - What, how, why questions
- **Local keywords** - Location-based keywords
- **Related keywords** - Synonyms and related terms
- **SEO insights** - Search volume estimates and competition levels

## Examples

### Generate a Guide Article

```bash
python seo_agent.py article -k "how to start a blog" -t conversational -w 1500 -a guide
```

### Generate Keywords for a Topic

```bash
python seo_agent.py keywords -t "vegan recipes" -c 20
```

### Generate Specific Keyword Types

```bash
python seo_agent.py keywords -t "home workout" -y primary_keywords -y question_keywords -y local_keywords
```

### Generate a Product Review

```bash
python seo_agent.py article -k "best wireless headphones 2024" -t professional -w 2000 -a review
```

### Generate a How-To Article

```bash
python seo_agent.py article -k "how to make sourdough bread" -t informal -w 1800 -a how-to
```

## Model Selection and Token Limits

The system supports multiple OpenAI models with different context limits. Choose the right model for your article length:

### Available Models

| Model | Context Limit | Best For | Cost |
|-------|---------------|----------|------|
| `gpt-4` | 8,192 tokens | Articles up to ~1,500 words | Standard |
| `gpt-4-turbo` | 128,000 tokens | Articles up to ~25,000 words | Higher |
| `gpt-3.5-turbo-16k` | 16,384 tokens | Articles up to ~3,000 words | Lower |

### Model Selection Examples

```bash
# Short article (default GPT-4)
python seo_interface.py article -k "coffee brewing" -w 1200

# Medium article (cost-effective)
python seo_interface.py article -k "digital marketing" -w 2000 -m gpt-3.5-turbo-16k

# Long article (high context limit)
python seo_interface.py article -k "comprehensive guide" -w 5000 -m gpt-4-turbo
```

For more details, see [TOKEN_LIMITS_GUIDE.md](TOKEN_LIMITS_GUIDE.md).

## Configuration

### Environment Variables

You can customize the behavior using these environment variables in your `.env` file:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - Model to use (default: gpt-4)
- `TEMPERATURE` - Creativity level 0.0-1.0 (default: 0.7)

### Article Types

- **guide** - Comprehensive guides and tutorials
- **review** - Product and service reviews
- **how-to** - Step-by-step instructions
- **list** - Listicles and top X articles
- **comparison** - Comparison articles

### Tones

- **formal** - Professional and authoritative
- **informal** - Casual and friendly
- **conversational** - Chatty and engaging
- **professional** - Business-focused

### Keyword Types

- **primary_keywords** - Main target keywords (1-3 words)
- **long_tail_keywords** - Longer, specific phrases (4+ words)
- **question_keywords** - What, how, why questions
- **local_keywords** - Location-based keywords
- **related_keywords** - Synonyms and related terms

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not found"**
   - Make sure you have a `.env` file with your API key
   - Check that the key is correct and active

2. **"Rate limit exceeded"**
   - Wait a moment and try again
   - Consider upgrading your OpenAI plan

3. **"Authentication error"**
   - Verify your API key is correct
   - Check your OpenAI account status

4. **JSON parsing errors**
   - The tool will show the raw response for debugging
   - Try regenerating with different parameters

### Getting Help

If you encounter issues:

1. Check your OpenAI API key is valid
2. Ensure you have sufficient API credits
3. Try with a simpler keyword first
4. Check the generated error messages

## License

This project is open source and available under the MIT License. 