import requests, re, collections
from bs4 import BeautifulSoup

START = "https://bbc.co.uk"

def f(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def flatten(xs):
    return list(f(xs))

def in_tree(element, xs):
    return element in flatten(xs)


def strip_links(url):
    headers = {
        'User-Agent': 'Mrrrrrr. Spidey',
        'From': 'mrrrspidey@wow-your-sad-enough-to-be-looking-at-the-logs-im-a-web-spider-that-somebody-made-for-fun-nothing-suspicous-here-if-you-want-to-chat-my-real-email-is-ollybritton-at-gmail-com.com'
    }

    data = requests.get(url, headers = headers).text
    soup = BeautifulSoup(data, "lxml")

    links = []

    for link in soup.find_all("a"):
        try:
            if not re.compile("https|http").match(link["href"]):
                if link["href"][-1] == "/" and url[-1] == "/":
                    # links.append(url + link["href"][1:])
                    pass

                else:
                    links.append(url + link["href"])

            else:
                links.append(link["href"])

        except:
            pass

    return links

# full_list = [START]
#
# for link in strip_links(full_list[0]):
#     full_list.append([link])

all_links = []

def build_tree(start_url = "https://bbc.co.uk", stop_iterations = 3, debug = True):
    count = stop_iterations - 1
    tree = [start_url]

    print(tree)

    if len(strip_links(start_url)) == 0 or count <= 0:
        return []

    for link in strip_links(start_url):
        # if in_tree(link, all_links):
        #     return []

        #else:
        all_links.append(link)
        tree.append([link, build_tree(link, count, False)])

    return tree



print(build_tree())
