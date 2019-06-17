import requests
from json import loads
API_URL = "https://api.comments.bot/{0}"

def _make_request(token, method_name, params=None):
    """
    Делает реквест к апи Comments
    """
    request_url = API_URL.format(method_name)
    params['api_key'] = token
    result = requests.post(request_url, params=params)

    if result.status_code != 200:
        msg = f"The server returned HTTP {result.status_code} {result.reason}. Response body:\n[{result.text.encode('utf8')}]"
        raise CommentsApiException(msg, method_name, result)
    try:
        result_json  = loads(result.text)
    except:
        msg = f"The server returned an invalid JSON response. Response body:\n[{result.text.encode('utf8')}]"
        raise CommentsApiException(msg, method_name, result)

    if not result_json['ok']:
        msg = f"Error code: {result_json['error']['code']} Description: {result_json['error']['name']}"
        raise CommentsApiException(msg, method_name, result)

    if method_name == 'createPost':
        return request(result_json['result']['post_id'], result_json['result']['link'])

    elif method_name in ['editPost', 'deletePost']:
        return request(params['post_id'], f"https://comments.bot/thread/{params['post_id']}")

class request:
    def __init__(self, post_id, link):
        self.id = post_id
        self.link = link

class CommentsApiException(Exception):
    def __init__(self, msg, function_name, result):
        super(CommentsApiException, self).__init__(f"A request to the Comments API was unsuccessful. {msg}")
        self.function_name = function_name
        self.result = result