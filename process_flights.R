library(tidyverse)

# Define top 10 airports
top_10_airports <- c("ATL", "LAX", "DFW", "DEN", "ORD", "JFK", "MCO", "MIA", "CLT", "LAS")

# Command-line arguments
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]  # Input CSV file
output_file <- args[2] # Output CSV file

# Read the input data
flights_data <- read_csv(input_file)

# Filter flights involving top 10 airports
filtered_flights <- flights_data %>%
  filter(Origin %in% top_10_airports | Dest %in% top_10_airports)

# Calculate individual airport counts
airport_flight_counts <- filtered_flights %>%
  pivot_longer(cols = c(Origin, Dest), names_to = "Type", values_to = "Airport") %>%
  filter(Airport %in% top_10_airports) %>%
  group_by(Year, Month, DayofMonth, Airport, Type) %>%
  summarise(flight_count = n(), .groups = 'drop') %>%
  pivot_wider(
    names_from = c(Airport, Type),
    values_from = flight_count,
    names_glue = "{Airport}_{Type}",
    values_fill = 0
  )

# Calculate overall flight counts
overall_flights <- flights_data %>%
  group_by(Year, Month, DayofMonth) %>%
  summarise(overall_flight_count = n(), .groups = 'drop')

# Calculate flights exclusively between top 10 airports
top10_flights <- filtered_flights %>%
  filter(Origin %in% top_10_airports | Dest %in% top_10_airports) %>%
  group_by(Year, Month, DayofMonth) %>%
  summarise(top10_flight_count = n(), .groups = 'drop')

top10_flights_in_between <- filtered_flights %>%
  filter(Origin %in% top_10_airports & Dest %in% top_10_airports) %>%
  group_by(Year, Month, DayofMonth) %>%
  summarise(top10_flight_count_between = n(), .groups = 'drop')

# Combine all metrics into a single dataframe
daily_flight_counts <- overall_flights %>%
  left_join(top10_flights, by = c("Year", "Month", "DayofMonth")) %>%
  left_join(top10_flights_in_between, by = c("Year", "Month", "DayofMonth")) %>%
  left_join(airport_flight_counts, by = c("Year", "Month", "DayofMonth")) %>%
  mutate(top10_flight_count = replace_na(top10_flight_count, 0)) %>%
  mutate(top10_flight_count_between = replace_na(top10_flight_count_between, 0))

# Write the processed data to the output file
write_csv(daily_flight_counts, output_file)
