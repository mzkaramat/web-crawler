from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pyquery import PyQuery as pq

class rsscarchSpider(CrawlSpider):
    name = "rsscarch" #Spider name
    allowed_domains = ["rsscarch.com"] # Which (sub-)domains shall be scraped?
    start_urls = ["http://www.rsscarch.com/"] # Start with this one
    
	#only allowing menu-item-object-project class, which is linked with projects
    rules = [Rule(LinkExtractor(restrict_css='.menu-item-object-project'), callback='parse_item')]


    def parse_item(self, response):
        """Parses each item from the scrapy
        """
		
        pyquery_obj = pq(response.body)
		
		#Getting respective fields of the project
        title = self.get_title(pyquery_obj)
        location = self.get_location(pyquery_obj)
        description = self.get_description(pyquery_obj)
		
		#encoding in utf-8
        description = description.encode('utf-8').strip()

        project =  {
            'title':title,
            'location':location,
            'description':description
        }
        print(project['description'])
		
        return project
		
		
    def get_title(self, pyquery_obj):
        """Returns the title of project.
        """
        return pyquery_obj('.post-title').text()
		
		
    def get_location(self, pyquery_obj):
        """Returns the location of project.
        """
        location = ''
		#Handling exception for bad formatted html
        try:
            str_strong = '</strong>'
            out=pyquery_obj('#portfolio-header p').html().split('<br/>')[1]
            location = out[out.index(str_strong)+len(str_strong):]
        except:
            location = ''
        return location
	
	
    def get_description(self, pyquery_obj):
        """Returns the description of project.
        """
        return pyquery_obj('.post-entry').text()