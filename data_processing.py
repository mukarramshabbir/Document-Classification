def get_attributes(json_data):
    extracted_data = []
    for item in json_data[0]["data"]["search"]["posts"]["items"]:
        extracted_data.append({
                    "id": item["id"],
                    "title": item["title"],
                    "author": item["creator"]["name"],
                    "follower_count": item["creator"]["socialStats"]["followerCount"],
                    "medium_url": item["mediumUrl"],
                    "clap_count": item["clapCount"],
                    "published_at": item["firstPublishedAt"],
                    "image_url": item["previewImage"]["id"] if "previewImage" in item else None,
                    "reading_time": item["readingTime"],
                    "uniqueSlug": item["uniqueSlug"],
                    "isLocked": item["isLocked"]
                })
    return extracted_data

def validity_condition(dic):
    return (not dic.get('isLocked', True)) and dic.get('reading_time', 0) >= 4