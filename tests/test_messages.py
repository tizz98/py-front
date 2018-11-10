import json

from front.marshalling import detect_encoding


class TestSendMessageJson:
    _data = {
      "author_id": "alt:email:leela@planet-exress.com",
      "sender_name": "Leela",
      "subject": "Good news everyone!",
      "body": "Why is Zoidberg the only one still alone?",
      "text": "Why is Zoidberg the only one still alone?",
      "attachments": [],
      "options": {
        "tags": [],
        "archive": True,
      },
      "to": [
        "calculon@momsbot.com",
        "mom@momsbot.com",
      ],
      "cc": [],
      "bcc": [],
    }

    def test_http_method_is_correct(self, api):
        api.send_message("cha_55c8c149", data=self._data)
        req = api._requester.calls[0].request

        assert req.method == 'POST'

    def test_json_body_is_correct(self, api):
        api.send_message("cha_55c8c149", data=self._data)
        req = api._requester.calls[0].request

        assert json.loads(req.body.decode(detect_encoding(req.body), 'surrogatepass')) == {
          "author_id": "alt:email:leela@planet-exress.com",
          "sender_name": "Leela",
          "subject": "Good news everyone!",
          "body": "Why is Zoidberg the only one still alone?",
          "text": "Why is Zoidberg the only one still alone?",
          "attachments": [],
          "options": {
            "tags": [],
            "archive": True,
          },
          "to": [
            "calculon@momsbot.com",
            "mom@momsbot.com",
          ],
          "cc": [],
          "bcc": [],
        }

    def test_response_has_id(self, api):
        msg = api.send_message("cha_55c8c149", self._data)
        assert msg.id == "msg_55c8c149"


class TestSendMessageMultipart:
    def test_http_method_is_correct(self, api):
        pass

    def test_multipart_body_is_correct(self, api):
        pass

    def test_response_has_id(self, api):
        pass
