# US Flight Data scrapper
This python scripts allows you to download flight data in the USA currently (as of January 2025) from October 1987 to November 2024. The data is downloaded from the [Bureau of Transportation Statistics](https://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp?pn=1) website. The data is downloaded in CSV format and saved in the `data` folder. 

A sample of the [data processed](data/daily_flight_counts_airports.csv) is shown below:

| Year | Month | DayofMonth | overall_flight_count | top10_flight_count |
|------|-------|------------|----------------------|--------------------|
| 2024 | 2     | 1          | 18455               | 10468             |
| 2024 | 2     | 2          | 18467               | 10498             |
| 2024 | 2     | 3          | 15501               | 9169              |
| 2024 | 2     | 4          | 18400               | 10496             |
| 2024 | 2     | 5          | 18342               | 10405             |

## Setup

Look into [config.yaml](config.yaml) file to change the parameters of the data you want to download. <br>
The year and month range includes all edge cases.

Don't forget to [install R](https://cran.r-project.org/) if you want to run the R to modify the data in the [similar way I do](process_flights.R).  

Install the required packages by yourself or use the conda environment as described below.


Finally, run the script by running the following command:
```bash 
python main.py
```
#### Optional: Conda setup
If you don't have Conda installed, you can download and install it from the [official Conda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

```bash 
conda env create --file=environment.yml
```
```bash
conda activate us-flight-data
```

