<p align="center">
  👮📊

  <h3 align="center">HPD Stats</h3>

  <p align="center">
    A project to track the statistics of the arrests of the <a href="https://www.honolulupd.org/">Honolulu Police Department</a>
    <br />
    <a href="https://hpdstats.com">View Project</a>
</p>

<!-- ABOUT THE PROJECT -->
## About The Project

This project provides a dashboard interface that tracks and updates from the [HPD's published daily arrest log reports](https://www.honolulupd.org/information/arrest-logs/).

### Why this exists:
The Attorney General's Office provdes [annual reports](https://ag.hawaii.gov/cpja/rs/cih/) as to the state of crime in Hawaii. This project provides a mechanism to validate these reports, track the numbers daily, and keep an archive of the raw data.

### Project Screenshots

#### Arrests by Sex

![Chart comparing arrests by Sex](docs/chart_compare_by_sex.png)

#### Arrests by Age

![Chart comparing arrests by Age](docs/chart_compare_by_age.png)

#### Arrests by Ethnicity

![Chart comparing arrests by Ethnicity](docs/chart_compare_by_ethnicity.png)

![Percentages of comparing arrests by Ethnicity](docs/percentages_compare_by_ethnicity.png)

#### Officer Breakdown

![Officer Breakdown](docs/officer_breakdown.png)

![Officer Breakdown Detailed View](docs/officer_breakdown_detail.png)

## How It Works

Using a combination of image cropping and OCR, we extract data about each arrest from each daily published arrest log.

### Full Breakdown

Everyday (with `cron`!), the script is run (`python3 main.py`) to scrape and parse the newly published arrest log. It then does the following:

1. Uploads the PDF file to AWS S3 [for archiving](https://hpdstats.com/archive)
2. Downloads the PDF file locally for parsing purposes

After we download the file, we prepare it for image cropping and OCR. To do this, we

1. Convert all the PDF file's pages into images ([Example Page](docs/2021-04-08_page_1.png))
2. Vertically concat all the page images into one long image, cropping the top and the bottom out so we only contain arrest records ([Example Image](docs/concat.png))
3. Crop each individual arrest record using the location of pixels ([Example Image](docs/record_10.png))
4. Crop each portion of the arrest record by the categories we want to parse ([Example Image - Race, Age, and Sex](docs/record_10_race_age_and_sex.png))
5. Use OCR([PyTesseract](https://pypi.org/project/pytesseract/)) to parse the text

We then upload the data to AWS DynamoDB. Using Flask and DynamoDB's boto3 module, data is served to the [HPDStats website](https://hpdstats.com/).
