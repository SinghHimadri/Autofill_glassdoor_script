# Software Engineering Job Application Bot (2.0) 👩🏾‍💻

A script to automatically search Glassdoor for job listings, aggregate every application URL, and apply to each job using pre-populated data. ***All with one click!***

![app demo](demo.gif)

## Inspiration
Ever sit at your desk for hours, clicking through endless job listings hoping to strike gold with one response? To solve this, I made a script a few months ago, which would take in a list of job URLs and automatically apply to potentially 100s of jobs with the click of a button. This was great, but there was one problem — the process of aggregating those links is painstaking. So, I wanted to automate that process with this project! ✨

## Installation
1. Install Selenium: `pip install selenium`
2. Install BeautifulSoup: `pip install beautifulsoup4`

## Usage
#### To test `job_list.py`
1. Uncomment the last line `job_list.py`
2. Run `$ python job_list.py`

#### To run the entire script:
1. Set a number of pages you'd like to iterate through here
2. Upload your Resume 
3. Fill Choices in job_list.py at line 17
4. FIll Information in autofill.py at line 13
5. Run `$ python autofill.py`
6. The script will open [glassdoor.com](https://www.glassdoor.com/index.htm), at which point you should log-in
7. From there on, everything is automatic!


## Thanks

* [Selenium](https://selenium-python.readthedocs.io/) - A tool designed for QA testing, but that actually works great for making these types of bots
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/doc) - A tool to scrape HTML/XML content (that saved be *big time* with this project)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/harshibar/5-python-projects/blob/master/LICENSE) file for details.
