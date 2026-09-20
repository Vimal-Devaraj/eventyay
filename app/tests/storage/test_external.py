import requests
import responses

from eventyay.storage.external import retrieve_url


@responses.activate
def test_retrieve_url_success_sends_user_agent(settings):
    responses.add(responses.GET, "https://example.com/page", status=200, body="hello")

    result = retrieve_url("https://example.com/page")

    assert result is not None
    assert result.status_code == 200
    sent_headers = responses.calls[0].request.headers
    assert sent_headers["User-Agent"] == f"{settings.INSTANCE_NAME}/1.0 ({settings.SITE_URL})"


@responses.activate
def test_retrieve_url_connection_error_returns_none():
    responses.add(
        responses.GET,
        "https://unreachable.example.com/",
        body=requests.exceptions.ConnectionError(),
    )

    assert retrieve_url("https://unreachable.example.com/") is None


@responses.activate
def test_retrieve_url_non_2xx_returns_none():
    responses.add(responses.GET, "https://example.com/missing", status=404)

    assert retrieve_url("https://example.com/missing") is None
