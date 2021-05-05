from bs4 import BeautifulSoup


class Parser:

    def parse_all_data(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')

        return {**self.parse_tags(soup), **self.parse_description(soup), **self.parse_company_desc(soup),
                **self.parse_days_remaining(soup)}

    @staticmethod
    def parse_tags(soup):
        data = dict()

        key_tags = [h4.text for h4 in soup.find_all('h4', {'class': 'c-infoBox__itemTitle'})]
        value_tags = soup.find_all('div', {'class': 'tags'})

        for key, value in zip(key_tags, value_tags):
            contents = list(value.stripped_strings)
            data[key] = contents[0].replace("\n", "") if len(contents) == 1 else [content for content in contents]

        return data

    @staticmethod
    def parse_description(soup):
        data = ""
        for string in soup.find('div', {'class': 'o-box__text s-jobDesc'}).stripped_strings:
            data += string
        key = "موقعیت شغلی"
        return {key: data}

    @staticmethod
    def parse_company_desc(soup):
        data = ""
        for string in soup.select_one(
                '#singleJob > div > div:nth-child(1) > div.col-md-8.col-sm-12.js-fixedWidgetSide > section > '
                'div:nth-child(6)').stripped_strings:
            data += string
        key = "معرفی شرکت"
        return {key: data}

    @staticmethod
    def parse_days_remaining(soup):
        data = soup.select_one('#apply-form > section > div.c-boxWidget__content > p').string.replace("\n", "")
        key = "فرصت ارسال رزومه"
        return {key: data}
