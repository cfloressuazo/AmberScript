# ML Application Diagram
The ML Application Diagram file displays a diagram of a proposed solution for a real time LDA topic model running in production environment with the use case of multiple files landing to a common location.
The process involves a set of AWS resources to extract the data, format, preprocessed (NLP) train a model and deploy this model to a production environment.
For this use case I will mainly focus in the training part, but suggested approach to solve a real scenario is displayed in the diagram.

The second part is composed by a movie scraper that is able to extract descriptions and story lines form movies in IMDB and store them locally.
After scraping the data, the Topic Modeling is applied to these, the chosen technique is LDA.
The cleaning and processing pipeline is wrapped in a function after the analysis, that can be found in the notebook.
The model objects are stored into the directory model within the notebooks folder.

The inference script then is in charge of loading the model and dictionary and providing the topic distribution to an unseen movie description. 
 
# Movie scraper
move_scraper is a small Scrapy project to scrape the top 1000 movies from IMDB.
## Extracted data
The scraper gets the title, year, genres, summary and story line from each of the movies in the top 1000.
```
{
    "title": "Spider-Man: Far from Home", 
    "year": "2019", "genre": ["Action", "Adventure", "Sci-Fi"], 
    "story_line": "Peter Parker's world has changed a lot since ...", 
    "description": "..."
}
```
## Running the movie spider
To run the scraper, navigate to the movie_scraper folder:

`$ cd movie_scraper`

Then run the spider as:

`$ scrapy crawl movies`

## Data
The data is extracted and stored under the movie_scraper/data folder with the name movies.json (the format is a JSON).

# LDA MODEL
The model analysis is under the notebooks folder. You can find the way data was cleaned and preprocessed and the kodel chosen to be used for future inference.
The process followed:
1. Read data
2. Tokenize
3. remove stopwords
4. lemmatization of field
5. leave only alpha characters
6. create dictionary
7. analysis and model training
8. parameter tuning
9. persist model to disk plus dictionary
10. deploy model into local file

## Inference
The inference script will print out the topic distribution of a new unseen movie description and also the most common words for that topic.
The inference script should be run as follow:
```
# this is the movie description for Saving the Private Ryan movie
$ python inference_topics.py "{\"text\": \"Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.\"}"
```

