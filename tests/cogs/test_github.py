from wulkabot.cogs import github


def test_parse_repo():
    assert github.parse_repo("owner/repo") == ("owner", "repo")
    assert github.parse_repo("repo", default_owner="owner") == ("owner", "repo")
    assert github.parse_repo("repo") is None


def test_parse_issue():
    assert github.parse_issue("owner/repo#1") == (("owner", "repo", 1))
    assert github.parse_issue("owner/repo#0") is None
    assert github.parse_issue("#1", default_owner="owner", default_repo="repo") == (
        ("owner", "repo"),
        1,
    )
    assert github.parse_issue("repo#1", default_owner="owner") == (("owner", "repo"), 1)
    assert github.parse_issue("#1", default_owner="owner") is None
    assert github.parse_issue("#1", default_repo="repo") is None
    assert github.parse_issue("repo#1", default_repo="repo") is None
    assert github.parse_issue("repo#1") is None
    assert github.parse_issue("#1") is None
    assert github.parse_issue("") is None


def test_find_repo_in_channel_topic():
    assert github.find_repo_in_channel_topic("https://github.com/owner/repo") == ("owner", "repo")
    assert github.find_repo_in_channel_topic("https://github.com/owner") is None
    assert github.find_repo_in_channel_topic("https://github.com/") is None
    assert github.find_repo_in_channel_topic("owner/repo") is None
    assert github.find_repo_in_channel_topic("") is None
