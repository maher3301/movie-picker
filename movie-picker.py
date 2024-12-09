import random
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple


IMDB_TOP_URL = 'https://www.imdb.com/chart/top'


def fetch_imdb_data(url: str) -> Tuple[List[str], List[str], List[str], List[float]]:
    # Add a user-agent header to mimic a browser
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return [], [], [], []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Debugging: Print a portion of the page content to ensure we fetched correctly
    # Uncomment the following line for debugging
    # print(response.text[:500])

    movietags = soup.select('td.titleColumn')
    inner_movietags = soup.select('td.titleColumn a')
    ratingtags = soup.select('td.ratingColumn strong')

    # Ensure all parts were parsed
    if not movietags or not inner_movietags or not ratingtags:
        print("Failed to parse IMDb data. Check the structure or anti-scraping measures.")
        return [], [], [], []

    def get_year(movie_tag):
        return movie_tag.find('span', class_='secondaryInfo').text.strip('()')

    years = [get_year(tag) for tag in movietags]
    titles = [tag.text for tag in inner_movietags]
    actors_list = [tag['title'] for tag in inner_movietags]
    ratings = [float(tag.text) for tag in ratingtags]

    return titles, years, actors_list, ratings


def main():
    print("Fetching data from IMDb...")
    titles, years, actors_list, ratings = fetch_imdb_data(IMDB_TOP_URL)

    if not titles:
        print("Could not fetch movie data. Please try again later.")
        return

    n_movies = len(titles)

    while True:
        idx = random.randrange(0, n_movies)
        print(f"{titles[idx]} ({years[idx]}), Rating: {ratings[idx]:.1f}, Starring: {actors_list[idx]}")

        user_input = input("Do you want another movie (y/[n])? ").strip().lower()
        if user_input != 'y':
            print("Enjoy your movie!")
            break


if __name__ == '__main__':
    main()
