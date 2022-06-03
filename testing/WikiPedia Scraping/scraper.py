import wikipedia

result = wikipedia.search("cats")
print(result)
page = wikipedia.page('Cat', auto_suggest=False, redirect=False)

print(page.summary)

# print(wikipedia.summary("Cat"))