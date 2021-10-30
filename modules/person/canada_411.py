import requests
import string
import bs4

from iris.module import Module
from iris.util import PrintUtil, HTMLUtil
from iris.logger import Logger
from urllib3.exceptions import InsecureRequestWarning

class IRISModule(Module):

    description = 'Lookup Canadian citizens\' personal information by name/address/phone number'
    author = 'cs'
    date = '28-07-2021'

    def execute(self, name__address__phone_number: str):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        people = [x for x in self.__411_lookup(name__address__phone_number) if not all(list(map((lambda x : x is None), x)))]

        if len(people) == 0:
            raise Exception('No results found')

        people_sorted = []

        for person in people:
            name, address, phone = person

            for i, (name1, address1, phones) in enumerate(people_sorted.copy()):
                if name == name1 and address == address1:
                    if not phone in phones:
                        people_sorted[i][2].append(phone)
                    break
            else:
                people_sorted.append((name, address, [phone]))

        for name, address, phones in people_sorted:
            Logger.info(name + ':')

            PrintUtil.pp({
                'Address': address,
                'Phone' if len(phones) == 1 else 'Phone numbers': phones[0] if len(phones) == 1 else phones
            })
            Logger.nl()

        return True

    def __411_lookup(self, keywords):
        MAX_RESULTS = 25

        def __is_address(keywords):
            """ Check if keywords is an address by checking if it both contains characters and numbers """
            return any((i in keywords for i in string.digits)) and any(([c in keywords for c in string.ascii_letters]))

        is_address = __is_address(keywords)

        res = requests.get(
            url='https://www.canada411.ca/search/',
            params={
                'stype': 'si',
                'what': keywords if is_address is False else None,
                'where': keywords if is_address is True else None
            },
            verify=False
        )

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        error = soup.find('div', {'class': 'ypalert ypalert--error'})

        if error is not None:
            raise Exception('An error occurred: %s' % error.find('p').text)

        for i in range(MAX_RESULTS):
            target = soup.find('div', {'id': f'Contact{i + 1}'})

            if target is None:
                break

            name = HTMLUtil.get_element_string(target, ('h2', {'id': f'ContactName{i + 1}'}), 'a')
            address = HTMLUtil.get_element_string(target, ('span', {'id': f'ContactAddress{i + 1}'}))
            phone = HTMLUtil.get_element_string(target, ('span', {'id': f'ContactPhone{i + 1}'}))

            yield name, address, phone

        return None, None, None
