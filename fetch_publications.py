import json
import time
from scholarly import scholarly

def fetch_publications():
    # Dr. Mridha's Google Scholar ID extracted from the URL
    author_id = 's_8YDgkAAAAJ'
    print(f"Fetching Google Scholar data for author ID: {author_id}...")

    try:
        author = scholarly.search_author_id(author_id)
        # Fill the author profile with their publications list
        author = scholarly.fill(author, sections=['publications'])
        
        pubs_data = []
        
        for pub in author.get('publications', []):
            try:
                # We fill each publication to get the journal and full author list
                # Note: Scholarly handles rate-limiting internally, but we add a tiny sleep just to be safe
                scholarly.fill(pub)
                bib = pub.get('bib', {})
                
                title = bib.get('title', 'Unknown Title')
                authors = bib.get('author', 'Mridha, D.')
                
                # Different entries might store the journal/conference name differently
                journal = bib.get('citation', '') or bib.get('journal', '') or bib.get('publisher', '')
                year = str(bib.get('pub_year', ''))
                citations = str(pub.get('num_citations', '0'))
                link = pub.get('pub_url', '#')
                
                pubs_data.append({
                    "title": title,
                    "authors": authors,
                    "journal": journal,
                    "year": year,
                    "citations": citations,
                    "link": link
                })
                print(f"Successfully fetched: {title}")
                time.sleep(0.5) # Slight delay to respect Google Scholar's servers
                
            except Exception as e:
                print(f"Failed to fetch details for a publication: {e}")
                continue

        # Sort publications by year, newest first
        pubs_data.sort(key=lambda x: x['year'], reverse=True)
        
        # Write out to the JSON file that the website expects
        with open('publications.json', 'w', encoding='utf-8') as f:
            json.dump(pubs_data, f, indent=4)
            
        print(f"Successfully saved {len(pubs_data)} publications to publications.json")

    except Exception as e:
        print(f"Critical error fetching author data: {e}")
        exit(1)

if __name__ == '__main__':
    fetch_publications()
