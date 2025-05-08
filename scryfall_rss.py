#!/usr/bin/env python3
import requests
import feedgenerator
import datetime
import time
import urllib.parse
import argparse
import os
import sys

def create_scryfall_rss(query, output_file='scryfall_feed.xml', feed_title=None, feed_description=None):
    """
    Create an RSS feed from Scryfall search results
    
    Args:
        query: The Scryfall search query
        output_file: Path to save the RSS feed XML
        feed_title: Title for the RSS feed
        feed_description: Description for the RSS feed
    """
    # URL encode the query
    encoded_query = urllib.parse.quote(query)
    
    # Set up the API URL
    api_url = f"https://api.scryfall.com/cards/search?q={encoded_query}&order=released"
    
    # Set up headers as required by Scryfall API
    headers = {
        'User-Agent': 'ScryFallRSSGenerator/1.0',
        'Accept': 'application/json'
    }
    
    try:
        # Make the API request
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        
        if not data.get('data'):
            print(f"No cards found for query: {query}")
            return False
        
        # Set default feed title and description if not provided
        if not feed_title:
            feed_title = f"Scryfall Search: {query}"
        if not feed_description:
            feed_description = f"RSS feed for Scryfall search: {query}"
        
        # Create the feed
        feed = feedgenerator.Rss201rev2Feed(
            title=feed_title,
            link=f"https://scryfall.com/search?q={encoded_query}",
            description=feed_description,
            language="en"
        )
        
        # Add each card as an item in the feed
        for index, card in enumerate(data['data']):
            # Create a unique ID for the card
            card_id = card.get('id', '')
            
            # Get the card's release date
            release_date_str = card.get('released_at', '')
            try:
                release_date = datetime.datetime.strptime(release_date_str, '%Y-%m-%d')
                # Add a small time offset based on the card's position in the results
                # This ensures cards with the same release date maintain their order
                # Since the API returns newest items first, we add a time offset that
                # preserves this ordering (first items get the most recent timestamps)
                release_date = release_date + datetime.timedelta(seconds=-index)
            except ValueError:
                release_date = datetime.datetime.now()
            
            # Initialize description
            description = ""
            
            # Check the card layout type and handle accordingly
            layout = card.get('layout', '')
            
            # For double-faced cards (transform, modal_dfc, etc.), get images from each face
            if card.get('card_faces') and len(card.get('card_faces', [])) > 0 and layout not in ['adventure', 'split', 'flip', 'meld']:
                # For double-faced cards, get images from each face
                for i, face in enumerate(card.get('card_faces', [])):
                    face_image_url = face.get('image_uris', {}).get('normal', '')
                    if face_image_url:
                        face_name = face.get('name', f'Face {i+1}')
                        description += f"<p><img src='{face_image_url}' alt='{face_name}'></p>"
            else:
                # For single-faced cards and split cards (adventure, split, flip, meld), get the image from the main card
                image_url = card.get('image_uris', {}).get('normal', '')
                if image_url:
                    description = f"<p><img src='{image_url}' alt='{card.get('name', '')}'></p>"
            
            # Add the card to the feed
            feed.add_item(
                title=card.get('name', 'Unknown Card'),
                link=card.get('scryfall_uri', f"https://scryfall.com/card/{card_id}"),
                description=description,
                pubdate=release_date,
                unique_id=card_id
            )
        
        # Write the feed to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            feed.write(f, 'utf-8')
        
        print(f"RSS feed created successfully: {output_file}")
        print(f"Feed contains {len(data['data'])} cards")
        
        # If there are more pages, mention it
        if data.get('has_more', False):
            total_cards = data.get('total_cards', 0)
            print(f"Note: This feed only contains the first page of results. Total cards matching query: {total_cards}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return False
    except Exception as e:
        print(f"Error creating RSS feed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Create an RSS feed from Scryfall search results')
    parser.add_argument('query', nargs='?', help='Scryfall search query')
    parser.add_argument('--output', '-o', default='scryfall_feed.xml', help='Output file path (default: scryfall_feed.xml)')
    parser.add_argument('--title', '-t', help='RSS feed title')
    parser.add_argument('--description', '-d', help='RSS feed description')
    parser.add_argument('--url', '-u', help='Full Scryfall search URL (alternative to query)')
    
    args = parser.parse_args()
    
    # Extract query from URL if provided
    if args.url and not args.query:
        try:
            parsed_url = urllib.parse.urlparse(args.url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            if 'q' in query_params:
                args.query = query_params['q'][0]
            else:
                print("Error: Could not extract query parameter from URL")
                sys.exit(1)
        except Exception as e:
            print(f"Error parsing URL: {e}")
            sys.exit(1)
    
    if not args.query:
        parser.print_help()
        print("\nExample usage:")
        print("  python scryfall_rss.py 't:angel c=w'")
        print("  python scryfall_rss.py --url 'https://scryfall.com/search?q=t%3Aangel+c%3Dw'")
        sys.exit(1)
    
    create_scryfall_rss(args.query, args.output, args.title, args.description)

if __name__ == "__main__":
    main()