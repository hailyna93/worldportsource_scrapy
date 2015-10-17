import scrapy

from coutries.items import CountryItem
from coutries.items import CountryInfor

class CountrySpider(scrapy.Spider):
	name = "country"
	allowed_domains = ["worldportsource.com"]
	start_urls = ["http://www.worldportsource.com/countries.php"]

	def parse(self, response):
		for href in response.css("tr td[valign = 'top'] a"):
			url = href.xpath('@href').extract()[0]
			url = response.urljoin(url)
			yield scrapy.Request(url, callback=self.parse_country)

	def parse_country(self, response):
		for href in response.css("tr td[valign = 'top'] a"):
			url = href.xpath('@href').extract()[0]
			name = href.xpath('text()').extract()[0]
			if(url.find('review')>=0):
				name = name +" *"
				url = url.replace("review/", "")

			url = response.urljoin(url)
			request = scrapy.Request(url, callback=self.parse_contry_infor)
			request.meta["name"] = name
			yield request

	def parse_contry_infor(self,response):
		info = CountryInfor()
		info["name"] = response.meta["name"]
		info['Latitude'] = response.css("table.form tr:nth-of-type(11) td:nth-of-type(2)::text").extract()
		info['Longitude'] = response.css("table.form tr:nth-of-type(12) td:nth-of-type(2)::text").extract()
		info['Port_Type'] = response.css("table.form tr:nth-of-type(14) td:nth-of-type(2)::text").extract()
		info['Port_Size'] = response.css("table.form tr:nth-of-type(15) td:nth-of-type(2)::text").extract()
		info['UN_LOCODE'] = response.css("table.form tr:nth-of-type(13) td:nth-of-type(2)::text").extract()
		info['Source_url'] = response.url
		yield info