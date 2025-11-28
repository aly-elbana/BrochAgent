# Company Brochure Generator

A Python application that analyzes company websites and generates professional brochures using AI. The tool extracts relevant marketing links, fetches website content, and creates comprehensive company brochures using Google's Gemini AI.

## Features

- **Link Analysis**: Automatically identifies and extracts marketing-valuable links from company websites
- **Content Extraction**: Fetches and processes content from landing pages and relevant linked pages
- **Brochure Generation**: Creates professional, well-structured brochures using AI
- **Streaming Output**: Optional real-time streaming of brochure generation
- **File Export**: Save generated brochures as Markdown files

## Requirements

- Python 3.11+
- Google Gemini API key
- Required packages (see dependencies in `pyproject.toml`)

## Installation

1. Install dependencies:

```bash
uv sync
```

2. Create a `.env` file in the project root and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the application:

```bash
python main.py
```

The application will present a menu with the following options:

1. **Generate brochure** - Creates a full brochure for a company
2. **Analyze links only** - Only analyzes and displays relevant links
3. **Exit** - Quit the application

### Example Workflow

1. Select option `1` to generate a brochure
2. Enter the website URL (e.g., `https://www.google.com`)
3. Enter the company name (e.g., `Google`)
4. Choose whether to stream output (y/n)
5. Optionally save the brochure to a file

## Project Structure

```
Project/
├── main.py                 # Main entry point
├── config.py              # Configuration and API client setup
├── prompts.py             # AI system prompts
├── link_analyzer.py       # Link extraction and analysis
├── brochure_generator.py  # Brochure generation logic
├── utils/
│   └── scraper.py        # Website scraping utilities
└── notebooks/
    └── code_prep.ipynb   # Development notebook
```

## How It Works

1. **Link Discovery**: The scraper extracts all links from the target website
2. **Link Analysis**: AI analyzes links and identifies marketing-relevant ones
3. **Content Fetching**: Fetches content from the main page and relevant linked pages
4. **Brochure Generation**: AI generates a comprehensive brochure based on the collected content
5. **Output**: Displays the brochure and optionally saves it to a file

## Output

Generated brochures include:

- Company Overview
- Products & Services
- Company Culture
- Customers & Partners
- Careers & Opportunities
- Contact & Online Presence

Brochures are saved in the `output/` directory as Markdown files.

## Notes

- The application uses Google's Gemini 2.5 Flash model
- Content is limited to 30,000 characters to avoid token limits
- Some websites may block automated scraping
