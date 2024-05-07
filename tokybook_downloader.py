import re
import json5
import requests
from pathlib import Path


def get_chapter_content(chapter_data):
    BASE_URLS = ['https://files01.tokybook.com/audio/',  'https://files02.tokybook.com/audio/']

    for base_url in BASE_URLS:
        response = requests.get(base_url+chapter_data['chapter_link_dropbox'])
        if response.status_code == 200:
            return response.content
        
    print('[FAILED] Failed to download chapter', chapter_data['name'])
    print(response.text)
    return None

def download_chapter(chapters_queue:list):

    chapter_info = chapters_queue.pop()
    print(chapter_info)
    chapter_file = Path('./MP3/'+chapter_info['name']+'.mp3')
    chapter_file.touch(exist_ok=True)

    chapter_content = get_chapter_content(chapter_info)
    if chapter_content == None:
        return
    
    chapter_file.write_bytes(chapter_content)

def extract_chapters_data(web_page_response:str) -> list:
    data = re.search(r"tracks\s*=\s*(\[[^\]]+\])\s*", web_page_response)
    parsed_data_str = data.group(1)
    parsed_data = json5.loads(parsed_data_str)
    
    # It is necessary to remove the first chapter entry, since it is not an actual chapter but rather 
    # an audion from tokybook's website
    parsed_data.pop(0)
    return parsed_data

def get_tokybook_data(tokybook_url:str):
    response = requests.get(tokybook_url)
    return response.text


if __name__ == '__main__':
    toky_response = get_tokybook_data('https://tokybook.com/fellowship-rings-audiobook-01-02')
    chapters_datas = extract_chapters_data(toky_response)
    download_chapter(chapters_datas)