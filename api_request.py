import requests

class ChallengeApi(object):
    BASE_URL = 'http://challenge.curbside.com'
    SESSION_URL = BASE_URL + '/get-session'
    START_URL = BASE_URL + '/start'

    def get_session(self):
        session = self.__get_json(ChallengeApi.SESSION_URL)
        return session['session']

    def get_start(self, session_id):
        start_result = self.__get_json(ChallengeApi.START_URL, session_id=session_id)
        return start_result['id'], start_result['next']

    def get_next(self, next_id, session_id):
        next_url = ChallengeApi.BASE_URL + '/' + next_id
        return self.__get_json(next_url, session_id=session_id)

    def __get_json(self, url, session_id=None):
        r = requests.get(url, headers={'Session': session_id})

        if r.status_code != 200:
            raise Exception('Out of time!')
    
        return r.json()
