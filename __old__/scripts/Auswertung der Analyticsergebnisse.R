#set working directory
setwd(dirname(rstudioapi::getSourceEditorContext()$path))
#load packages
config_path <- Sys.getenv("R_CONFIG_PATH")
source(config_path)
library(ggplot2)
library(dplyr)
library(png)
library(ggpattern)
library(hrbrthemes)

file <- zaehlstelle_test
# Read the CSV file into R
events <- read.csv(file, header = TRUE)
type <- c('bicycle', 'bus', 'car', 'person', 'truck')
events <- events %>% filter(road_user_type %in% type)
# Print the content of the CSV file
print(events)

file15 <- zaehlstelle_test_15
file15 <- "D:/Erhebungen/24.04.2024 Meerbusch Areal Böhler/21Uhr.counts_15min.csv"
# Read the CSV file into R
data <- read.csv(file15, header = TRUE)
type <- c('bicycle', 'bus', 'car', 'person', 'truck')
data <- data %>% filter(classification %in% type)
data$utc <- as.numeric(as.POSIXct(data$start.time, format="%Y-%m-%d %H:%M:%S")) 

data_ <- filter(data, from.section == "a" & to.section == "b" 
                & utc >= as.numeric(as.POSIXct("2024-04-24 06:00:00", format="%Y-%m-%d %H:%M:%S"))
                )#& utc < as.numeric(as.POSIXct("2024-04-24 12:00:00", format="%Y-%m-%d %H:%M:%S")))
data_ <- data_ %>% group_by(classification, utc, start.time) %>% summarise(count=sum(count), .groups = "drop")
write.csv(data_, file="D:/Erhebungen/24.04.2024 Meerbusch Areal Böhler/21Uhr.csv", sep=";", )

#grids <- expand.grid(X=data_$classification, Y=data_$start.time)
#grids$Z <- data_$count

# Heatmap 
ggplot(data_, aes(x=classification, y=start.time, fill=count))+
#ggplot(grids, aes(X, Y, fill= Z)) + 
  geom_tile() +
  geom_text(aes(label= count), color="white")+
  #scale_fill_gradient(low="white", high="blue") +
  #scale_y_reverse()+
  theme_ipsum() +
  theme(legend.position = "none")
