from googlesearch import search

def get_first_result(query):
    try:
        lis = [""," "]
        for result in search(query, num=10):
            if result in lis:
                continue
            return result
    except Exception as e:
        return f"Error occurred: {e}"


# topic = "Python programming"
# link = get_first_result(topic)
# print("First result:", link)
