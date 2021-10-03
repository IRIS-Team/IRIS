import cfscrape, re
from iris.module import Module
from iris.util import PrintUtil
from iris.logger import logger

class IRISModule(Module):
    description = 'Get playstation username IP.'
    author = 'robert'
    date = '3-10-2021'

    def execute(self, playstation_username: str):
        scraper = cfscrape.create_scraper()

        req = scraper.get(f'https://playstationresolver.xyz/profile/{playstation_username}')

        found_usernames = re.findall(r'(?:\d{1,3}\.)+(?:\d{1,3})', req.text)
        
        if len(found_usernames) < 1:
            Logger.info('No results found.')
            return


        for x in found_usernames:
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', x):
                PrintUtil.pp({'Possible IP': x,})
