from bs4 import BeautifulSoup


class Parser:

    def parse_all_data(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')

        adv_data = {
            'Title': self.parse_title(soup),
            'Description': self.parse_description(soup),
            'Company name': self.parse_company_name(soup),
            'Company description': self.parse_description(soup),
            'Remaining days': self.parse_days_remaining(soup),
        }

        adv_data.update(self.parse_tags(soup))
        return adv_data

    @staticmethod
    def parse_title(soup):
        data = soup.find('div', {'class': 'c-jobView__titleText'})
        if data is not None:
            data = data.string
        return data

    @staticmethod
    def parse_description(soup):
        data = ""
        tag = soup.find('div', {'class': 's-jobDesc'})
        if tag is not None:
            for string in tag.stripped_strings:
                data += string
        return data

    @staticmethod
    def parse_company_name(soup):
        data = ""
        tag = soup.find('h2', {'class': 'c-companyHeader__name'})
        if tag is not None:
            for string in tag.stripped_strings:
                data += string
        return data

    @staticmethod
    def parse_company_desc(soup):
        data = ""
        tag = soup.select_one(
            '#singleJob > div > div:nth-child(1) > div.col-md-8.col-sm-12.js-fixedWidgetSide > section > '
            'div:nth-child(6)')
        if tag is not None:
            for string in tag.stripped_strings:
                data += string
        return data

    @staticmethod
    def parse_days_remaining(soup):
        data = ""
        tag = soup.find('p', {'class': 'u-textCenter'})
        if tag is not None:
            for string in tag.stripped_strings:
                data += string
        return data

    @staticmethod
    def parse_tags(soup):
        # returns a dict of tags(length is unknown)
        data = dict()

        key_tags = [h4.text for h4 in soup.find_all('h4', {'class': 'c-infoBox__itemTitle'})]
        value_tags = soup.find_all('div', {'class': 'tags'})

        for key, value in zip(key_tags, value_tags):
            contents = list(value.stripped_strings)
            data[key] = contents[0].replace("\n", "") if len(contents) == 1 else [content for content in contents]

        return data
