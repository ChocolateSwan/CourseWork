MAX_COUNT_IN_ONE_URL = 16


def cut_found_arr(el):
    if len(el["found_arr"]) > MAX_COUNT_IN_ONE_URL:
        el["found_arr"][MAX_COUNT_IN_ONE_URL-1] = "..."
        for i in range(MAX_COUNT_IN_ONE_URL, len(el["found_arr"])):
            el["found_arr"].pop()
    return el
