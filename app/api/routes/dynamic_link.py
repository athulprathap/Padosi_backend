from fastapi import HTTPException
import requests


class DynamicLinks:
    FIREBASE_API_URL = 'https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={}'

    def __init__(self, api_key, domain, timeout=10):
        self.api_key = api_key
        self.domain = domain
        self.timeout = timeout
        self.api_url = self.FIREBASE_API_URL.format(self.api_key)

    def generate_dynamic_link(self, link, short=True, params={}):
        payload = {
            "dynamicLinkInfo": {
                "domainUriPrefix": self.domain,
                "link": link
            },
            "suffix": {
                "option": "SHORT" if short else "UNGUESSABLE"
            }
        }
        payload['dynamicLinkInfo'].update(params)

        response = requests.post(self.api_url, json=payload, timeout=self.timeout)

        data = response.json()

        if not response.ok:
            raise HTTPException(status_code=404,detail=data)

        return data['shortLink']
    
