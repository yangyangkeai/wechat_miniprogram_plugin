# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 yangyangkeai
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import ssl
import urllib.request
from html.parser import HTMLParser

class ContentExtractor(HTMLParser):
    """
    Parser to extract the inner HTML of the div with class 'content custom'.
    """
    def __init__(self):
        super().__init__()
        self.in_target_div = False
        self.target_depth = 0
        self.current_depth = 0
        self.html_pieces = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if not self.in_target_div:
            if tag == 'div':
                classes = attrs_dict.get('class', '').split()
                if 'content' in classes and 'custom' in classes:
                    self.in_target_div = True
                    self.target_depth = self.current_depth
            self.current_depth += 1
        else:
            self.current_depth += 1
            attrs_str = ""
            if attrs:
                attrs_str = " " + " ".join([f'{k}="{v}"' if v is not None else f'{k}' for k, v in attrs])
            self.html_pieces.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag):
        self.current_depth -= 1
        if self.in_target_div:
            if tag == 'div' and self.current_depth == self.target_depth:
                self.in_target_div = False
            else:
                self.html_pieces.append(f"</{tag}>")

    def handle_data(self, data):
        if self.in_target_div:
            self.html_pieces.append(data)

    def handle_startendtag(self, tag, attrs):
        if self.in_target_div:
            attrs_str = ""
            if attrs:
                attrs_str = " " + " ".join([f'{k}="{v}"' if v is not None else f'{k}' for k, v in attrs])
            self.html_pieces.append(f"<{tag}{attrs_str} />")

    def handle_entityref(self, name):
        if self.in_target_div:
            self.html_pieces.append(f"&{name};")

    def handle_charref(self, name):
        if self.in_target_div:
            self.html_pieces.append(f"&#{name};")

    def handle_comment(self, data):
        if self.in_target_div:
            self.html_pieces.append(f"<!--{data}-->")

def generate_metadata(href, text):
    """
    Fetch the component's detailed documentation page and extract the content
    inside <div class="content custom">, saving it as {text}.html.
    """
    url = "https://developers.weixin.qq.com/miniprogram/dev/component/" + href
    print(f"Fetching and extracting: {url} -> {text}.html")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, context=context) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return

    extractor = ContentExtractor()
    extractor.feed(html)
    extracted_html = "".join(extractor.html_pieces).strip()

    output_dir = os.path.dirname(__file__)
    file_path = os.path.join(output_dir, f"output/{text}.html")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(extracted_html)
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")

class WeChatComponentParser(HTMLParser):
    """
    Parser to extract component links from WeChat mini-program documentation page.
    It targets tables with class 'have-children-table' and rows with class 'have-children-tr'.
    Within each target row, it finds the <a> tag in the second column (second <td>).
    """
    def __init__(self):
        super().__init__()
        self.in_target_table = False
        self.in_target_row = False
        self.col_index = -1
        self.in_td = False
        self.in_target_a = False
        self.current_href = None
        self.current_text = []
        self.results = []

        self.table_depth = 0
        self.tr_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Identify start of target table
        if tag == 'table':
            self.table_depth += 1
            classes = attrs_dict.get('class', '').split()
            if 'have-children-table' in classes:
                self.in_target_table = True

        # Identify start of target row inside the target table
        elif tag == 'tr' and self.in_target_table:
            self.tr_depth += 1
            classes = attrs_dict.get('class', '').split()
            if 'have-children-tr' in classes:
                self.in_target_row = True
                self.col_index = -1

        # Track <td> columns inside the target row
        elif tag == 'td' and self.in_target_row:
            self.in_td = True
            self.col_index += 1

        # Target <a> tag inside the second column (index 1) of the target row
        elif tag == 'a' and self.in_target_row and self.col_index == 1:
            self.in_target_a = True
            self.current_href = attrs_dict.get('href')
            self.current_text = []

    def handle_endtag(self, tag):
        if tag == 'table':
            if self.table_depth > 0:
                self.table_depth -= 1
                if self.table_depth == 0:
                    self.in_target_table = False

        elif tag == 'tr':
            if self.tr_depth > 0:
                self.tr_depth -= 1
                if self.tr_depth == 0:
                    self.in_target_row = False
                    self.col_index = -1

        elif tag == 'td':
            self.in_td = False

        elif tag == 'a' and self.in_target_a:
            self.in_target_a = False
            text_content = "".join(self.current_text).strip()
            self.results.append((self.current_href, text_content))
            self.current_href = None
            self.current_text = []

    def handle_data(self, data):
        if self.in_target_a:
            self.current_text.append(data)

def scrape_components():
    url = 'https://developers.weixin.qq.com/miniprogram/dev/component/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    context = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req, context=context) as response:
        html = response.read().decode('utf-8')

    parser = WeChatComponentParser()
    parser.feed(html)

    for href, text in parser.results:
        generate_metadata(href, text)

if __name__ == '__main__':
    scrape_components()
