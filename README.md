# **💼 Jobs Study Tn**

Back with another project.

This time it’s a full ETL (Extract, Transform, and Load) project with a PowerBI dashboard

This is a study to further understand the Tunisian job market through a sample pulled from LinkedIn and Bayt websites.

It first begins with a Python web scraper using Selenium, Beautifulsoup, along with a proxy switcher, that bypasses the IP blockage of Linkedin and Bayt jobs websites to extract the needed data such as job titles, job descriptions, post date, employment type, industry, etc...

Then, using a locally downloaded LLM; llama3 with the ollama library and custom prompts I applied it to extract the required skills from each job. Additionally, I used LLAMA3 to transform the job titles extracted into their general format to facilitate analysis later on.

After that, with an Azure PostgreSQL database connected to the Python script with the pyodbc library, I managed to load the data into SQL tables for persistent storage.

PS: You can leverage the university’s email to get $100 credits in your Azure account.

Finally, directly from the database, I created a direct query to the PowerBI dashboard that allows an up-to-date dashboard with the newly fed data for visualization and analysis.

A glimpse of the insights found:

- The majority of the jobs posted are entry-level positions.
- The most sought-after jobs are managers and engineers followed by directors and technicians.
- Most required skills are mainly soft ones such as communication, leadership, and problem-solving, and the most required language is generally English.
- It is the service provider industry that has the highest level of recruitment.

You can check out the dashboard via this link: https://app.powerbi.com/view?r=eyJrIjoiMzc3ZWFlZWYtMWMwMi00ZTRhLTlmMzItYjk0OTJkZTg4N2I3IiwidCI6ImRiZDY2NjRkLTRlYjktNDZlYi05OWQ4LTVjNDNiYTE1M2M2MSIsImMiOjl9


## Used Libraries:

The main libraries used in this project:

- `pandas`: fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.

- `bs4`: s a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser.

- `requests`: is an HTTP client library for the Python programming language. Requests is one of the most downloaded Python libraries, with over 300 million monthly downloads. It maps the HTTP protocol onto Python's object-oriented semantics.

- `selenium`: is used to carry out automated test cases for browsers or web applications. You can easily use it to simulate tests such as tapping on a button, entering content to the structures, skimming the entire site, etc.

- `pyodbc`: an open source Python module that makes accessing ODBC databases simple. It implements the DB API 2.0 specification but is packed with even more Pythonic convenience.

- `ollama`: facilitates LLMs in applications such as chatbots, customer support agents, and content generation tools. Code generation, debugging, and cross-language programming support can be accelerated with LLMs if used effectively.

- `fake-useragent`:  a Python library that provides an easy way to identify/detect devices like mobile phones, tablets and their capabilities by parsing (browser/HTTP) user agent strings. 


## Screenshots
<img width="1280" alt="Screen Shot 2024-08-02 at 2 09 40 PM" src="https://github.com/user-attachments/assets/b99080c1-10a0-42c6-9271-2634ab51436b">

<img width="1280" alt="Screen Shot 2024-08-02 at 2 09 47 PM" src="https://github.com/user-attachments/assets/352f6501-21f6-4ed8-a1f3-5d5ab030f5a0">

<img width="1280" alt="Screen Shot 2024-08-02 at 2 09 56 PM" src="https://github.com/user-attachments/assets/901fa691-1d5e-4c4d-9d3f-c6b808817525">

<img width="1280" alt="Screen Shot 2024-08-02 at 2 10 10 PM" src="https://github.com/user-attachments/assets/247c8c1e-2ddf-454d-bd78-9d48948d1367">





## Feedback

If you have any feedback, please reach out to us at mohamedazizkhezam@gmail.com

