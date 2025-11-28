import sys
from config import initialize_client, API_KEY
from link_analyzer import display_relevant_links
from brochure_generator import create_brochure, save_brochure


def main():
    if not API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables")
        print("Please set GEMINI_API_KEY in your .env file or environment")
        sys.exit(1)
    
    try:
        initialize_client()
        
        print("\n" + "="*60)
        print("Company Brochure Generator")
        print("="*60 + "\n")
        
        print("1. Generate brochure")
        print("2. Analyze links only")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "3":
            print("Exiting...")
            return
        
        url = input("Enter website URL: ").strip()
        
        if not url:
            print("Error: URL is required")
            sys.exit(1)
        
        if choice == "2":
            display_relevant_links(url)
            return
        
        if choice == "1":
            company_name = input("Enter company name: ").strip()
            
            if not company_name:
                print("Error: Company name is required")
                sys.exit(1)
            
            stream_choice = input("Stream output? (y/n): ").strip().lower()
            stream = stream_choice == "y"
            
            brochure = create_brochure(
                company_name=company_name,
                url=url,
                stream=stream
            )
            
            if not stream:
                print("\n" + "="*60)
                print("GENERATED BROCHURE")
                print("="*60 + "\n")
                print(brochure)
                print("\n" + "="*60 + "\n")
            
            save_choice = input("Save brochure to file? (y/n): ").strip().lower()
            if save_choice == "y":
                save_brochure(brochure, company_name)
        else:
            print("Invalid choice")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
