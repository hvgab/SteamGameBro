import requests
import os
from pprint import pprint, pformat
import logging
from django.conf import settings
from xml.etree import ElementTree
import xmltodict

logger = logging.getLogger(__name__)

class SteamGroup(object):
    """classd doc"""

    def __init__(self, groupid):
        self.groupid = groupid

    def __repr__(self):
        return f'<SteamGroup({self.groupid})>'

    def get_members_list(self):
        logger.debug('start get members list')
        
        url = f'https://steamcommunity.com/gid/{self.groupid}/memberslistxml'
        payload = {'xml': 1}
        r = requests.get(url, params=payload)

        pprint(f'{r.url=}')

        tree = ElementTree.fromstring(r.content)
        rd = xmltodict.parse(r.content)
        # pprint(rd)

        members = rd['memberList']['members']['steamID64']
        # pprint(members)

        return members

    def get_group_info(self):
        url = f'https://steamcommunity.com/gid/{self.groupid}/memberslistxml'
        payload = {'xml': 1}
        r = requests.get(url, params=payload)
        pprint(f'{r.url=}')
        tree = ElementTree.fromstring(r.content)
        rd = xmltodict.parse(r.content)

        members = rd['memberList']

        pprint(f"{rd['memberList']['groupDetails']['groupName']=}")
        pprint(f"{rd['memberList']['groupDetails']['groupURL']=}")
        pprint(f"{rd['memberList']['groupDetails']['headline']=}")
        pprint(f"{rd['memberList']['groupDetails']['summary']=}")
        pprint(f"{rd['memberList']['groupDetails']['avatarIcon']=}")
        pprint(f"{rd['memberList']['groupDetails']['avatarMedium']=}")
        pprint(f"{rd['memberList']['groupDetails']['avatarFull']=}")
        pprint(f"{rd['memberList']['groupDetails']['memberCount']=}")

        return rd


if __name__ == "__main__":

    g = SteamGroup('103582791429672498')
    logger.debug(f'{g=}')
    
    # members_list = g.get_members_list()
    # logger.debug(pformat(members_list))

    info = g.get_group_info()
