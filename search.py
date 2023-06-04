import argparse
import os
import time
import requests
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from pytube import YouTube

def scrape_search_results(query):
    url = f"http://www.bing.com/search?q={query}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    results = soup.find_all("li", class_="b_algo")
    print(results)

def scrape_website(url, output_file):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    if output_file:
        with open(output_file, 'w') as f:
            f.write(str(soup))
        print(f'Successfully saved to file {output_file}')
    else:
        file_name = url.split('/')[-1] + '.html'
        with open(file_name, 'w') as f:
            f.write(str(soup))
        print(f'Successfully saved to file {file_name}')

def download_image(url, output_file):
    r = requests.get(url)

    if output_file:
        with open(output_file, 'wb') as f:
            f.write(r.content)
        print(f'Successfully saved to file {output_file}')
    else:
        file_name = url.split('/')[-1]
        with open(file_name, 'wb') as f:
            f.write(r.content)
        print(f'Successfully saved to file {file_name}')

def download_youtube_video(youtube_url):
	# Create a YouTube object from the video URL
	yt = YouTube(youtube_url)

	# Filter out the highest resolution video and download it
	stream = yt.streams.get_highest_resolution()
	stream.download()

def scrape_website_list(website_list_file, output_dir, delay=None):
    with open(website_list_file) as f:
        websites = f.read().splitlines()
    for website in websites:
        print(f'Scraping website {website}...')
        try:
            r = requests.get(website, timeout=10)
            soup = BeautifulSoup(r.content, "html.parser")
            if output_dir:
                file_name = website.split('/')[-1] + '.html'
                with open(f'{output_dir}/{file_name}', 'w') as f:
                    f.write(str(soup))
                print(f'Successfully saved to file {file_name}')
            else:
                file_name = website.split('/')[-1] + '.html'
                with open(file_name, 'w') as f:
                    f.write(str(soup))
                print(f'Successfully saved to file {file_name}')
            if delay:
                time.sleep(delay)
        except Timeout:
            print(f'Request to {website} timed out')
        except:
            print(f'Failed to scrape website {website}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape data from search results, website, or download image')
    parser.add_argument('--mode', type=str, default='search', help='Mode to run (default: search)')
    parser.add_argument('--query', type=str, default=None, help='Search query or URL depending on mode (default: None)')
    parser.add_argument('--output_file', type=str, default='', help='Name of file to save output')
    parser.add_argument('--website_list_file', type=str, default=None, help='Path to txt file containing list of websites to scrape')
    parser.add_argument('--output_dir', type=str, default=None, help='Name of directory to save website files in (default: current directory)')
    parser.add_argument('--delay', type=int, default=None, help='Delay in seconds between website scrapes to prevent overwhelming the website (default: None)')
    parser.add_argument('--youtube_url', type=str, default=None, help='URL of the YouTube video to download')
    parser.add_argument('--output_format', type=str, default=None, help='The output format of the YouTube video to download (e.g., mp4, mp3)')
    parser.add_argument('--resolution', type=int, default=720, help='The maximum resolution of the YouTube video to download')
    args = parser.parse_args()

    if args.query is None and args.website_list_file is None and args.youtube_url is None:
        # Do nothing if query, website list, and YouTube URL are not provided
        pass
    elif args.mode == 'search':
        scrape_search_results(args.query)
    elif args.mode == 'website':
        if not args.query:
            print('Error: Website URL not provided')
        else:
            scrape_website(args.query, args.output_file)
    elif args.mode == 'image':
        download_image(args.query, args.output_file)
    elif args.mode == 'website_list':
        if not args.website_list_file:
            print('Error: Website list file not provided')
        else:
            if args.delay and args.delay < 1:
                print('Error: Delay must be at least 1 second')
            else:
                scrape_website_list(args.website_list_file, args.output_dir, args.delay)
    elif args.mode == 'youtube':
        if not args.youtube_url:
            print('Error: YouTube URL not provided')
        else:
            download_youtube_video(args.youtube_url)
    else:
        print(f'Unknown mode {args.mode}')
