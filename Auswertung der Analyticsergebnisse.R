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
events <- read.csv(zaehlstelle_test, header = TRUE)
type <- c('bicycle', 'bus', 'car', 'person', 'truck')
events <- events %>% filter(road_user_type %in% type)
# Print the content of the CSV file
print(events)

# Read the CSV file into R
data <- read.csv(zaehlstelle_test_15, header = TRUE)
type <- c('bicycle', 'bus', 'car', 'person', 'truck')
data <- data %>% filter(#classification %in% type & 
                          count != 0)
# Print the content of the CSV file
print(data)

# Dummy data
x <- LETTERS[1:20]
y <- paste0("var", seq(1,20))
data <- expand.grid(X=events$occurrence_day, Y=events$occurrence_time)
data$Z <- events$road_user_type

# Heatmap 
ggplot(data, aes(X, Y, fill= Z)) + 
  geom_tile()
