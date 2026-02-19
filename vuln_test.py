import click
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_html_of(url):
    resp = requests.get(url)

    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)

    return resp.text

def count_occurrences_in(word_list, min_length):
    word_count = {}
    for word in word_list:
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)
            word_count[word] = current_count + 1
    return word_count

from urllib.parse import urljoin, urlparse

def scrape_page(url, base_url):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    words = re.findall(r'\w+', soup.get_text())
    links = []
    for a in soup.find_all('a', href=True):
        full_url = urljoin(url, a['href'])
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.append(full_url)      
    return words, list(set(links))

def get_top_words_from(all_words, min_length):
    occurrences = count_occurrences_in(all_words, min_length)
    return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)

def get_mutations_for(word):
    base_variations = [
        word, 
        word.lower(), 
        word.upper(), 
        word.capitalize(), 
        word.swapcase()
    ]
    final_results = []
    year = "2026"
    for base in base_variations:
        final_results.append(base)
        final_results.append(f"{base}{year}")
        final_results.append(f"{base}{year}!")
        final_results.append(f"{base}{year}!!")
        final_results.append(f"{base}!")
        final_results.append(f"{base}!!")
        final_results.append(f"{base}123")   
    return list(set(final_results))



@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).')
@click.option('--output','-o', type=click.File('w'), help='Convert the result into a txt file')
@click.option('--show_all','-s', is_flag=True, help='Writes all the words of the webpage')
@click.option('--mutate', '-m', is_flag=True, help='Enable password mutations for each word.')
@click.option('--depth', '-d', default=0, help='Crawl depth.')

def main(url, length, output, show_all, mutate, depth):
    urls_to_visit = [(url, 0)] 
    visited = set()
    master_word_list = []
    while urls_to_visit:
        current_url, current_depth = urls_to_visit.pop(0)
        if current_url in visited or current_depth > depth:
            continue
        visited.add(current_url)

        try:
            new_words, new_links = scrape_page(current_url, url)
            master_word_list.extend(new_words)

            if current_depth < depth:
                for link in new_links:
                    if link not in visited:
                        urls_to_visit.append((link, current_depth + 1))
        except Exception:
            continue

    top_words = get_top_words_from(master_word_list, length)

    if show_all:
        limite = len(top_words)
    else:
        limite = min(10, len(top_words))

    for i in range(limite):
        raw_word = top_words[i][0]

        if mutate:
            results = get_mutations_for(raw_word)
        else:
            results = [raw_word]

        for r in results:
            if output:
                output.write(f"{r}\n")
            else:
                print(r)
    
if __name__ == '__main__':
    #pylint:disable=no-value-for-parameter
    main()