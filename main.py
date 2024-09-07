import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

# Define the Spider
class ArticleSpider(scrapy.Spider):
    name = "article_spider"
    
    # Add your 120 URLs here in the start_urls list
    start_urls = [
        'https://en.wikipedia.org/wiki/India',
        'https://en.wikipedia.org/wiki/India_Today',
        # Add the remaining URLs
    ]

    def parse(self, response):
        title = response.xpath('//h1/text()').get()  # Extract the H1
        paragraphs = response.xpath('//p//text()').getall()  # Extract all paragraph text
        images = response.xpath('//img/@src').getall()  # Extract image paths

        # Combine all paragraph text and image paths into a single string
        content = "\n".join(paragraphs)
        image_paths = "\n".join(images)

        # Store the extracted data
        yield {
            'title': title,
            'url': response.url,
            'content': content + "\n\nImages:\n" + image_paths
        }

# Run the spider and save data to a CSV
def run_spider():
    # List to store scraped data
    scraped_data = []

    # Custom pipeline to collect the data in the list
    class ArticlePipeline:
        def process_item(self, item, spider):
            scraped_data.append(item)
            return item

    # Set up the Scrapy process
    process = CrawlerProcess({
        'ITEM_PIPELINES': {
            '__main__.ArticlePipeline': 1,
        }
    })

    # Start the scraping process
    process.crawl(ArticleSpider)
    process.start()

    # After scraping, save the data to a CSV
    df = pd.DataFrame(scraped_data, columns=['title', 'url', 'content'])
    df.to_csv('scraped_articles.csv', index=False)

# Main execution
if __name__ == "__main__":
    run_spider()
