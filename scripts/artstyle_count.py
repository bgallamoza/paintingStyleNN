from bs4 import BeautifulSoup
import requests as re
import matplotlib.pyplot as plt

"""
Short script for determining what painting artstyles to use based on counts from
the WikiArt.org website
"""

########## BEAUTIFULSOUP TEXT EXTRACTION ##########

# We want to look at the most common painting artstyles from the WikiArt page
url = "https://www.wikiart.org/en/paintings-by-style"
tuples = []
content = re.get(url).text
soup = BeautifulSoup(content, 'html.parser')

# In the HTML, the bulletpoints of styles & count exists in the 'ul' tag
# Individual bulletpoints are in many 'a' tags
style_list = soup.find('ul', attrs={"class":"dictionaries-list"}) 
lines = style_list.find_all('a')

for line in lines:
    count = line.find('sup').text                   # painting count exists in the 'sup' tag
    line.sup.decompose()                            # remove 'sup' tag to isolate artstyle name
    tuples.append((line.text.strip(), int(count)))  # append tuple of (name, count) to tuples list

tuples.sort(key=lambda x: x[1], reverse=True)       # sort list according to the count
print(tuples[:15])                                  # print 15 most common artstyles and handpick styles from there

########## OUTPUT FOR MATPLOTLIB BAR PLOT ##########
names = [i[0] for i in tuples]
counts = [i[1] for i in tuples]

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(names, counts)
plt.show()

# Impressionism
# Romanticism
# Expressionism
# Post-Impressionism
# Surrealism
# Baroque
# Symbolism
# Neoclassicism
# Rococo
# Cubism
# Northern Renaissance