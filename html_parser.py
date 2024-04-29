import json

def get_apollo_state(html_text):
    start_index = html_text.find("window.__APOLLO_STATE__ = ")
    if start_index == -1:
        return False

    end_index = html_text.find("</script>", start_index)
    if end_index == -1:
        return False

    json_string = html_text[start_index + len("window.__APOLLO_STATE__ = "):end_index]

    try:
        apollo_state_dict = json.loads(json_string)
        return apollo_state_dict
    except:
        pass
    return False