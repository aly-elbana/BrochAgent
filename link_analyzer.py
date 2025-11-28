import json
from utils.scraper import fetch_website_links
from config import initialize_client, MODEL
from prompts import LINK_SYSTEM_PROMPT


def get_links_user_prompt(url):
    links = fetch_website_links(url)

    user_prompt = f"""
Extract **all marketing-valuable links** from the website:

URL: {url}

You are given raw links below — your job is to identify every link that can be useful in marketing,
branding, brochures, business presentations, product communication, investor material, hiring,
or public-facing messaging.

Raw links discovered from site:

{"\n".join(links)}

Return output **strictly in JSON** only — NO commentary, NO explanation, NO Markdown.
"""

    return user_prompt


def select_relevant_links(url):
    gemini = initialize_client()
    
    response = gemini.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": LINK_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": get_links_user_prompt(url)
            }
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)


def display_relevant_links(url):
    print(f"\n{'='*60}")
    print(f"Analyzing links for: {url}")
    print(f"{'='*60}\n")
    
    try:
        relevant_links = select_relevant_links(url)
        
        if "links" in relevant_links and relevant_links["links"]:
            print(f"Found {len(relevant_links['links'])} relevant links:\n")
            
            for i, link in enumerate(relevant_links["links"], 1):
                print(f"{i}. {link.get('specific_type', 'Unknown')}")
                print(f"   URL: {link.get('url', 'N/A')}")
                print(f"   Type: {link.get('type', 'N/A')}")
                print(f"   Importance: {link.get('importance_score', 'N/A')}/100")
                print(f"   Why useful: {link.get('why_useful', 'N/A')}")
                print()
        else:
            print("No relevant links found.")
            
    except Exception as e:
        print(f"Error analyzing links: {str(e)}")
