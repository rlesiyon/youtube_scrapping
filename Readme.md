## Youtube Scrapping Project.

This project implements a method for scrapping youtube search result using selenium. Selenium is a perform document that allows for automation of website by the use of webdriver. 

### Sofware Engineering Technologies Employed: 

- selenium: Automating website scrolling to get a large source html to parse. The html is parse using find_element* methods provided in selenium. We used an xpath. Inspected the html and obtained the video id

- Youtube api: Use the video id to query youtube database using the api; to get all the information necessary for downstream application. 

- hydra: abstract the project configuration like json file containing credentials, website headers.

- sqlite: maintain a youtube search database for update purpose of the data.

### Data Science Technologies used:
- lemmatizaton
- Text representation: BOW, Term Frequency and Inverse Document Frequency(TFiDF)
- LDA

### Application: 

The idea of this project is to understand the current issues being discussed on youtube videos for a particular country. The selenium returns the search result for a particular African country. The data is then analyzed to obtain to gain insights into data. Analysis considered are as follows:

- EDA: give a higher overview of the data
- Topic analysis: Get the top topics discussed in youtube videos for a country.
- Document Clustering: understand the kind of clusters available 