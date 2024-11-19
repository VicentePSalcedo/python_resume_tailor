from bs4 import BeautifulSoup
import cloudscraper

scraper = cloudscraper.create_scraper()

def get_job_description_from_indeed(url) -> str:
    response = scraper.get(url)

    if response.status_code!=200:
        print(f"The reuest failed with an error {response.status_code}")
        return "No job Description Found"
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        job_description = soup.find('div', id="jobDescription")
        print("Finished scraping job description")
        return job_description.text

def get_full_site_text(url) -> str:
    response = scraper.get(url)
