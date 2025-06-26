# SEO Agent

An intelligent SEO content generation tool powered by OpenAI that creates high-quality, SEO-optimized articles based on your target keywords.

## Features

- 🎯 **Keyword-focused content** - Optimized for your target keywords
- 📝 **Multiple article types** - Guides, reviews, how-to articles, lists, and comparisons
- 🎨 **Flexible tone options** - Formal, informal, conversational, or professional
- 📊 **SEO optimization** - Meta titles, descriptions, and structured content
- 📁 **Multiple output formats** - JSON and Markdown files
- 🔧 **Easy CLI interface** - Simple command-line tool for quick article generation

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

# Specify all options
python seo_agent.py --keyword "best protein powder" --tone informal --word-count 1500 --article-type guide

# Short options
python seo_agent.py -k "digital marketing tips" -t professional -w 2000 -a how-to

# Custom output directory
python seo_agent.py -k "seo strategies" -o my_articles
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

### Article Structure

Each generated article includes:

- **Meta title** - SEO-optimized title (50-60 characters)
- **Meta description** - Compelling description (150-160 characters)
- **Article title** - Engaging main headline
- **Article sections** - Well-structured content with H2 headings
- **FAQ section** - Common questions and answers
- **SEO tips** - Optimization recommendations

## Examples

### Generate a Guide Article

```bash
python seo_agent.py -k "how to start a blog" -t conversational -w 1500 -a guide
```

### Generate a Product Review

```bash
python seo_agent.py -k "best wireless headphones 2024" -t professional -w 2000 -a review
```

### Generate a How-To Article

```bash
python seo_agent.py -k "how to make sourdough bread" -t informal -w 1800 -a how-to
```

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