from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int
    id_str: str
    name: str
    screen_name: str
    location: str
    url: str
    description: str
    protected: bool
    verified: bool
    followers_count: int
    friends_count: int
    listed_count: int
    favourites_count: int
    statuses_count: int
    created_at: str
    profile_banner_url: str
    profile_image_url_https: str
    default_profile: bool
    default_profile_image: bool
    first_scrape: str
    last_update: str = field(init=False, default="")
    suspended: bool = field(init=False, default=False)


# https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user


# {
# 	"id": 6253282,
# 	"id_str": "6253282",
# 	"name": "Twitter API",
# 	"screen_name": "TwitterAPI",
# 	"location": "San Francisco, CA",
# 	"profile_location": null,
# 	"description": "The Real Twitter API. Tweets about API changes, service issues and our Developer Platform. Don't get an answer? It's on my website.",
# 	"url": "https:\/\/t.co\/8IkCzCDr19",
# 	"entities": {
# 		"url": {
# 			"urls": [{
# 				"url": "https:\/\/t.co\/8IkCzCDr19",
# 				"expanded_url": "https:\/\/developer.twitter.com",
# 				"display_url": "developer.twitter.com",
# 				"indices": [
# 					0,
# 					23
# 				]
# 			}]
# 		},
# 		"description": {
# 			"urls": []
# 		}
# 	},
# 	"protected": false,
# 	"followers_count": 6133636,
# 	"friends_count": 12,
# 	"listed_count": 12936,
# 	"created_at": "Wed May 23 06:01:13 +0000 2007",
# 	"favourites_count": 31,
# 	"utc_offset": null,
# 	"time_zone": null,
# 	"geo_enabled": null,
# 	"verified": true,
# 	"statuses_count": 3656,
# 	"lang": null,
# 	"contributors_enabled": null,
# 	"is_translator": null,
# 	"is_translation_enabled": null,
# 	"profile_background_color": null,
# 	"profile_background_image_url": null,
# 	"profile_background_image_url_https": null,
# 	"profile_background_tile": null,
# 	"profile_image_url": null,
# 	"profile_image_url_https": "https:\/\/pbs.twimg.com\/profile_images\/942858479592554497\/BbazLO9L_normal.jpg",
# 	"profile_banner_url": null,
# 	"profile_link_color": null,
# 	"profile_sidebar_border_color": null,
# 	"profile_sidebar_fill_color": null,
# 	"profile_text_color": null,
# 	"profile_use_background_image": null,
# 	"has_extended_profile": null,
# 	"default_profile": false,
# 	"default_profile_image": false,
# 	"following": null,
# 	"follow_request_sent": null,
# 	"notifications": null,
# 	"translator_type": null
# }


# API RESPONSE FULL EXAMPLE

# tweepy.models.User(
#     _api=None,
#     _json={
#         "id": 1103349513295667201,
#         "id_str": "1103349513295667201",
#         "name": "Celso Serra",
#         "screen_name": "CelsoSerra1",
#         "location": "Campinas, Brasil",
#         "description": "Brasileiro acima de tudo",
#         "url": None,
#         "entities": {"description": {"urls": []}},
#         "protected": False,
#         "followers_count": 1933,
#         "friends_count": 3667,
#         "listed_count": 1,
#         "created_at": "Wed Mar 06 17:39:57 +0000 2019",
#         "favourites_count": 9251,
#         "utc_offset": None,
#         "time_zone": None,
#         "geo_enabled": False,
#         "verified": False,
#         "statuses_count": 1619,
#         "lang": None,
#         "contributors_enabled": False,
#         "is_translator": False,
#         "is_translation_enabled": False,
#         "profile_background_color": "F5F8FA",
#         "profile_background_image_url": None,
#         "profile_background_image_url_https": None,
#         "profile_background_tile": False,
#         "profile_image_url": "http://pbs.twimg.com/profile_images/1485914373533147139/e16WErxX_normal.jpg",
#         "profile_image_url_https": "https://pbs.twimg.com/profile_images/1485914373533147139/e16WErxX_normal.jpg",
#         "profile_banner_url": "https://pbs.twimg.com/profile_banners/1103349513295667201/1643104568",
#         "profile_link_color": "1DA1F2",
#         "profile_sidebar_border_color": "C0DEED",
#         "profile_sidebar_fill_color": "DDEEF6",
#         "profile_text_color": "333333",
#         "profile_use_background_image": True,
#         "has_extended_profile": True,
#         "default_profile": True,
#         "default_profile_image": False,
#         "following": False,
#         "follow_request_sent": False,
#         "notifications": False,
#         "translator_type": "none",
#         "withheld_in_countries": [],
#     },
#     id=1103349513295667201,
#     id_str="1103349513295667201",
#     name="Celso Serra",
#     screen_name="CelsoSerra1",
#     location="Campinas, Brasil",
#     description="Brasileiro acima de tudo",
#     url=None,
#     entities={"description": {"urls": []}},
#     protected=False,
#     followers_count=1933,
#     friends_count=3667,
#     listed_count=1,
#     created_at=datetime.datetime(2019, 3, 6, 17, 39, 57, tzinfo=datetime.timezone.utc),
#     favourites_count=9251,
#     utc_offset=None,
#     time_zone=None,
#     geo_enabled=False,
#     verified=False,
#     statuses_count=1619,
#     lang=None,
#     contributors_enabled=False,
#     is_translator=False,
#     is_translation_enabled=False,
#     profile_background_color="F5F8FA",
#     profile_background_image_url=None,
#     profile_background_image_url_https=None,
#     profile_background_tile=False,
#     profile_image_url="http://pbs.twimg.com/profile_images/1485914373533147139/e16WErxX_normal.jpg",
#     profile_image_url_https="https://pbs.twimg.com/profile_images/1485914373533147139/e16WErxX_normal.jpg",
#     profile_banner_url="https://pbs.twimg.com/profile_banners/1103349513295667201/1643104568",
#     profile_link_color="1DA1F2",
#     profile_sidebar_border_color="C0DEED",
#     profile_sidebar_fill_color="DDEEF6",
#     profile_text_color="333333",
#     profile_use_background_image=True,
#     has_extended_profile=True,
#     default_profile=True,
#     default_profile_image=False,
#     following=False,
#     follow_request_sent=False,
#     notifications=False,
#     translator_type="none",
#     withheld_in_countries=[],
# )
