#set working directory
setwd(dirname(rstudioapi::getSourceEditorContext()$path))
#load packages
config_path <- Sys.getenv("R_CONFIG_PATH")
source(config_path)
library(ggplot2)
library(dplyr)
library(png)
library(ggpattern)
# Read the CSV file into R
data <- read.csv(zaehlstelle_test, header = TRUE)
type <- c('bicycle', 'bus', 'car', 'person', 'truck')
data <- data %>% filter(road_user_type %in% type)
# Print the content of the CSV file
print(data)

# Read the CSV file into R
data <- read.csv(zaehlstelle_test_15, header = TRUE)
type <- c('bicycle', 'bus', 'car', 'person', 'truck')
data <- data %>% filter(#classification %in% type & 
                          count != 0)
# Print the content of the CSV file
print(data)
