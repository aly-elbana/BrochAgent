from utils.scraper import fetch_website_contents
from link_analyzer import select_relevant_links
from config import initialize_client, MODEL
from prompts import BROCHURE_SYSTEM_PROMPT


def fetch_page_and_all_relevant_links(url):
    print(f"Fetching content from: {url}")
    contents = fetch_website_contents(url)

    print("Analyzing relevant links...")
    relevant_links = select_relevant_links(url)

    result = f"## Landing page contents\n\n{contents}\n\n## Relevant links\n"

    if "links" in relevant_links and relevant_links["links"]:
        print(f"Fetching content from {len(relevant_links['links'])} relevant pages...")
        for i, link in enumerate(relevant_links["links"], 1):
            print(f"  [{i}/{len(relevant_links['links'])}] Fetching: {link.get('url', 'N/A')}")
            result += f"* [{link.get('specific_type', 'Unknown')}]({link.get('url', 'N/A')})\n"
            try:
                link_content = fetch_website_contents(link.get('url', ''))
                result += f"{link_content}\n\n"
            except Exception as e:
                print(f"    Warning: Could not fetch {link.get('url', 'N/A')}: {str(e)}")
                result += f"[Content could not be fetched: {str(e)}]\n\n"

    return result


def get_brochure_user_prompt(company_name, url):
    base_prompt = f"""
You are creating a professional brochure for the company: {company_name}.
Use the following contents from its landing page and other relevant pages
to summarize the company for prospective customers, investors, and recruits.
Respond in Markdown without code blocks.

Focus on these sections if the information is available:
1. Company Overview: Who they are, what they do, and their market presence.
2. Products & Services: Core offerings and unique selling points.
3. Company Culture: Values, mission, work environment, and team dynamics.
4. Customers & Partners: Key clients, target audience, and strategic partners.
5. Careers & Opportunities: Available roles, career growth, and employee benefits.
6. Contact & Online Presence: Website, social media, and other relevant links.
"""

    website_contents = fetch_page_and_all_relevant_links(url)

    user_prompt = base_prompt + "\n\n" + website_contents

    user_prompt = user_prompt[:30_000]

    return user_prompt


def create_brochure(company_name, url, stream=False):
    gemini = initialize_client()
    
    print(f"\n{'='*60}")
    print(f"Generating brochure for: {company_name}")
    print(f"Website: {url}")
    print(f"{'='*60}\n")
    
    user_prompt = get_brochure_user_prompt(company_name, url)
    
    if stream:
        print("Generating brochure (streaming)...\n")
        response_text = ""
        
        stream_obj = gemini.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": BROCHURE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            stream=True
        )
        
        for chunk in stream_obj:
            delta_content = chunk.choices[0].delta.content or ""
            response_text += delta_content
            print(delta_content, end="", flush=True)
        
        print("\n")
        return response_text
    else:
        print("Generating brochure...")
        response = gemini.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": BROCHURE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        print("Brochure generated successfully!\n")
        return response.choices[0].message.content


def save_brochure(brochure_content, company_name, output_dir="output"):
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    
    safe_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')
    
    filename = os.path.join(output_dir, f"{safe_name}_brochure.md")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(brochure_content)
    
    print(f"Brochure saved to: {filename}")
    return filename
