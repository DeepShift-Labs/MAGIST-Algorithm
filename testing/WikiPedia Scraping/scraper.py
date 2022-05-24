import wikipedia

result = wikipedia.search("door")
print(result[0])
page = wikipedia.page('Doors')

print(page.summary)

