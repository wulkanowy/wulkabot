from wulkabot.cogs import github


def test_parse_repo():
    assert github.parse_repo("wulkanowy/sdk") == ("wulkanowy", "sdk")
    assert github.parse_repo("sdk") is None
    assert github.parse_repo("sdk", default_owner="wulkanowy") == ("wulkanowy", "sdk")


def test_parse_issue():
    assert github.parse_issue("#1") is None
    assert github.parse_issue("") is None
    assert github.parse_issue("#1", default_owner="wulkanowy") is None
    assert github.parse_issue("#1", default_repo="wulkanowy") is None
    assert github.parse_issue("#1", default_owner="wulkanowy", default_repo="wulkanowy") == (
        ("wulkanowy", "wulkanowy"),
        1,
    )
    assert github.parse_issue("wulkanowy#1") is None
    assert github.parse_issue("wulkanowy#1", default_owner="wulkanowy") == (
        ("wulkanowy", "wulkanowy"),
        1,
    )
    assert github.parse_issue("wulkanowy#1", default_repo="wulkanowy") is None


def test_find_repo_in_channel_topic():
    assert github.find_repo_in_channel_topic("") is None
    assert github.find_repo_in_channel_topic("wulkanowy/wulkanowy") is None
    assert github.find_repo_in_channel_topic("https://github.com/wulkanowy/wulkanowy") == (
        "wulkanowy",
        "wulkanowy",
    )
    assert github.find_repo_in_channel_topic("https://github.com/wulkanowy") is None
    assert github.find_repo_in_channel_topic("https://github.com/") is None
