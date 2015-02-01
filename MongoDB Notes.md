
Introduction

The Greater Vancouver area of around 2.4 million inhabitants is the third most populous metropolitan area in the country and the most populous in Western Canada. 
Vancouver is one of the most ethnically and linguistically diverse cities in Canada; 52% of its residents have a first language other than English.

I chose this particular dataset as Vancouver is my hometown and I know the domain quite well. I chose the GVRD in particular because of the larger population and therefore a large enough dataset to inspect. I would like to confirm some intuition that I've always had about Vancouver and see if the data supports it. 


1. Find the coordinates. Check the XML file.

(node(49.0072,-123.3517,49.4431,-122.2037);<;);out;

1. Problems Encountered in the Map

Different forms of Street Names.

Ave, Ave. transformed to Avenue

West Broadway - I thought it was missing Street. To my surprise, after confirming from Google Maps Street is not on the official map and Broadway must be a street type.

Typos in the name:

'Hwy.': set(['Fraser Hwy.', 'ing George Hwy.']),
Since I've travelled on this Highway I know two things.
First of all, it should be King George and I also know they recently renamed it
to King George Boulevard. 

Another interesting discovery was that Wynd is also a street type. 

Arbutus Wynd - Wynd': set(['Arbutus Wynd']),

Kingsway is another interesting one as there is no street type. The 'way' is included in the one name itself.

Extra spacing
 Beatty St =>  Beatty Street



I need to rename the whole thing. For no

For something ambigious like this, I have chosen to delete this record since it is too vague.
'Park': set(['Park']),

 However, before doing that I looked through the data to find if I could see from the other tags and context what it could be renamed to.
skip = ["Tsawwassen","Park","Terminal","Sanders","8500"]


2. Retrieval Date and Time. Check the XML file.

bash command: $ ls -l GVRD\ -\ Vancouver\ -\ OSM\ XML\ Raw.osm

-rw-r--r--    1 user     Administ 177183117 Jan 30 00:54 GVRD - Vancouver - OSM
XML Raw.osm

[Jan 30 00:54 Pacific]

3. Data Overview

File Sizes 

XML file

bash command: $ ls -lh GVRD\ -\ Vancouver\ -\ OSM\ XML\ Raw.osm

-rw-r--r--    1 user     Administ     169M Jan 30 00:54 GVRD - Vancouver - OSM X
ML Raw.osm

[169 MB]



JSON file

Number of documents  -  db.van.find().count()

Number of nodes -		db.van.find( { "type" : "node"} ).count()

Number of ways -		db.van.find( { "type" : "way"} ).count()

Number of unique users - db.van.distinct({"created.user"}).length()


3. Additional Ideas

- See how many streets are named after Canadian Provinces

- See how many amenities are named after Royalty (King or Queen) or Knights (Sir)

- Top 10 Amenities

- Top 3 most popular cuisines

- Are there more yoga studios or fitness facilities?

- Top 3 Religions

- How many amenities mention Bitcoin?



References

http://en.wikipedia.org/wiki/Vancouver







