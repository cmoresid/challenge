"""Encapsulates requests to challenge API"""

import requests

class ChallengeApi(object):
    """Performs requests to challenge API"""
    BASE_URL = 'http://challenge.curbside.com'
    SESSION_URL = BASE_URL + '/get-session'
    START_URL = BASE_URL + '/start'

    def get_session(self):
        """Retrieve a new session ID"""
        session = self.__get_json(ChallengeApi.SESSION_URL)
        return session['session']

    def get_start(self, session_id):
        """Initial GET request to API to begin the challenge."""
        start_result = self.__get_json(ChallengeApi.START_URL, session_id=session_id)
        return start_result['id'], start_result['next']

    def get_next(self, next_id, session_id):
        """GET request to retrieve node that has an id = next_id"""
        next_url = ChallengeApi.BASE_URL + '/' + next_id
        return self.__get_json(next_url, session_id=session_id)

    def __get_json(self, url, session_id=None):
        """Reusable method to create GET request to challenge API using session_id."""
        get_json_request = requests.get(url, headers={'Session': session_id})

        if get_json_request.status_code != 200:
            raise Exception('Out of time!')

        return get_json_request.json()
