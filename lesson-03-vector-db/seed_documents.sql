INSERT INTO rag_documents (title, content, source) VALUES

-- Programming / Python
('Python Decorators Explained',
'A decorator in Python is a function that takes another function and extends its behavior without explicitly modifying it. Common uses include logging function calls, measuring execution time, enforcing access control, and caching results. The @ syntax is just syntactic sugar for calling the decorator with the function as its argument.',
'docs/python/decorators.md'),

('Understanding Python Generators',
'Generators are functions that produce a sequence of values lazily using the yield keyword. Instead of returning all values at once like a list, a generator produces them one at a time, pausing execution between yields. This makes generators memory-efficient for working with large or infinite sequences. The generator protocol is implemented via __iter__ and __next__ methods under the hood.',
'docs/python/generators.md'),

('Async and Await in Python',
'Python''s async and await keywords let you write concurrent code that handles I/O-bound operations efficiently. An async function returns a coroutine that must be awaited or scheduled on an event loop. This pattern shines when your program spends time waiting on network requests, database queries, or file I/O. For CPU-bound work, you still need multiprocessing or threading.',
'docs/python/asyncio.md'),

-- Programming / Web
('REST API Design Principles',
'REST (Representational State Transfer) is an architectural style for designing networked applications. Core principles include statelessness (each request contains all information needed), use of standard HTTP methods (GET, POST, PUT, DELETE), resource-based URLs, and uniform interface. Well-designed REST APIs are predictable, cacheable, and work well with HTTP infrastructure like proxies and CDNs.',
'docs/web/rest.md'),

('What is GraphQL',
'GraphQL is a query language for APIs developed by Facebook. Instead of multiple REST endpoints returning fixed data shapes, GraphQL exposes a single endpoint where clients specify exactly what data they need. This solves over-fetching and under-fetching problems common in REST APIs. GraphQL comes with its own tradeoffs: more complex caching, potential for expensive queries, and additional learning curve for teams.',
'docs/web/graphql.md'),

-- Programming / Database
('Database Indexes Explained',
'Database indexes are data structures that speed up queries at the cost of slower writes and additional storage. The most common type is the B-tree index, which supports range queries and sorted output. Hash indexes are faster for equality lookups but don''t support ranges. Partial indexes cover only rows matching a condition, saving space when queries always filter similarly.',
'docs/database/indexes.md'),

('ACID Properties in Databases',
'ACID stands for Atomicity, Consistency, Isolation, and Durability. These properties guarantee database transactions behave reliably. Atomicity means all operations in a transaction succeed or all fail. Consistency ensures the database moves from one valid state to another. Isolation prevents transactions from interfering with each other. Durability guarantees committed data survives crashes.',
'docs/database/acid.md'),

-- Cooking
('Perfect Pasta Technique',
'Great pasta starts with heavily salted boiling water — about 1 tablespoon of salt per liter. Cook until al dente, meaning firm to the bite with a slight resistance in the center. Reserve a cup of starchy pasta water before draining; it emulsifies sauces beautifully. Finish cooking pasta briefly in the sauce rather than just topping it, so flavors meld together.',
'cooking/techniques/pasta.md'),

('How to Make Sourdough Bread',
'Sourdough bread relies on wild yeast and lactic acid bacteria living in a flour-and-water starter. Mix flour, water, and a bit of starter, then let the dough ferment slowly over 12 to 24 hours. The long fermentation develops complex flavor and improves digestibility. Shape, proof again, and bake in a very hot oven — ideally in a Dutch oven for the first half to trap steam.',
'cooking/baking/sourdough.md'),

('Essential Knife Skills',
'A sharp chef''s knife is the most important tool in any kitchen. Hold it with your dominant hand pinching the blade near the bolster, with your thumb and index finger on opposite sides of the blade. Keep your other hand curled into a claw shape to protect your fingertips while guiding the food. Rock the knife through cuts rather than chopping straight down.',
'cooking/techniques/knife-skills.md'),

-- Travel
('Visiting Kyoto Temples',
'Kyoto has over 1,600 Buddhist temples and 400 Shinto shrines. The most famous include Kinkaku-ji (the Golden Pavilion), Fushimi Inari with its endless red torii gates, and Kiyomizu-dera with its wooden stage overlooking the city. Visit early morning to avoid crowds, especially at Fushimi Inari. Respect the sacred nature of these sites: speak quietly, don''t touch artifacts, and follow photography rules.',
'travel/japan/kyoto.md'),

('Trekking in the Himalayas',
'Himalayan treks range from gentle multi-day walks to serious mountaineering expeditions. Popular routes include the Annapurna Circuit in Nepal, Everest Base Camp, and Markha Valley in Ladakh. Altitude sickness is the main danger above 2,500 meters; acclimatize slowly, drink water constantly, and descend if symptoms worsen. Hire local guides when possible — they support the local economy and genuinely know the terrain.',
'travel/nepal/himalayan-trekking.md'),

-- Science
('How Vaccines Work',
'Vaccines train your immune system to recognize and fight specific pathogens without you having to get sick first. They typically contain weakened or inactivated versions of the pathogen, or just key molecular signatures (antigens) that trigger an immune response. Your body produces antibodies and memory cells that respond quickly if you encounter the real pathogen later.',
'science/biology/vaccines.md'),

('The Theory of Plate Tectonics',
'Plate tectonics is the theory that Earth''s outer shell is divided into large plates that slowly move across the planet''s surface. This movement, driven by convection currents in the mantle below, explains earthquakes, volcanoes, mountain building, and the shapes of continents. Plates can collide, pull apart, or slide past each other, each type of boundary producing different geological features.',
'science/geology/plate-tectonics.md'),

('Black Holes and Spacetime',
'Black holes are regions of spacetime where gravity is so strong that nothing — not even light — can escape once it crosses the event horizon. They form when massive stars collapse at the end of their lives. Despite their name, black holes aren''t empty: they have mass, charge, and spin. Supermassive black holes exist at the centers of most galaxies, including our own Milky Way.',
'science/physics/black-holes.md');