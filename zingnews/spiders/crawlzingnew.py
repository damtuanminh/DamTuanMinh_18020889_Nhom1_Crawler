import scrapy


class spiderZingnews(scrapy.Spider):
    name = 'Zingnews'
    start_urls = ['https://zingnews.vn/benh-nhan-787-mac-covid-19-da-di-cho-choi-bai-voi-nhieu-nguoi-post1117044.html']
    links_list = []

    #xử lí trang web và trích xuất thông tin
    def parse(self, response):
        f = open('/Users/minhdam/PycharmProjects/zing/zingnews/zingnews/spiders/Output/' + response.css('div.page-wrapper article::attr(article-id)').extract_first() + '.txt', 'w+')

        f.write('LIÊN KẾT: ' + response.css('link::attr(href)').extract_first() + '\n')
        category = response.css('header.the-article-header p.the-article-category a.parent_cate::text').get()
        f.write('CHUYÊN MỤC: ' + category + '\n')

        title = response.css('h1.the-article-title::text').get()
        f.write('TIÊU ĐỀ: ' + title + '\n')

        time = response.css('li.the-article-publish::text').get()
        f.write('THỜI GIAN: ' + time + '\n')

        f.write('TAGS: ')
        for tag in response.css('p.the-article-tags a::text'):
            p_tag = tag.get()
            f.write(p_tag + ', ')

        summary = response.css('section.main p.the-article-summary::text').get()
        f.write('\n' + 'TÓM TẮT: ' + summary + '\n')

        f.write('NỘI DUNG: ' + '\n')
        for i in response.css('div.the-article-body p::text'):
            p_body = i.get()
            f.write(p_body.strip() + '\n')

        '''yield {
            'Chuyenmuc': response.css('header.the-article-header p.the-article-category a.parent_cate::text').get(),
            'Tieude': response.css('h1.the-article-title::text').get(),
            'Thoigian': response.css('li.the-article-publish::text').get(),
            'Tomtat': response.css('section.main p.the-article-summary::text').get(),
            'Tags': response.css('p.the-article-tags span::text').extract(),
            'Noidung': response.css('div.the-article-body p::text').extract()
        }'''

        next_links = self.get_next_links(response)
        for link in next_links:
            if link and (link not in self.links_list) and (len(self.links_list) <= 5000):
                self.links_list.append(link)
                yield scrapy.Request('https://zingnews.vn/' + link, callback=self.parse)

    def get_next_links(self, response):
        #Trả về danh sách các link trong response
        next_links = response.css('p.article-title a::attr(href)').extract()
        return next_links
