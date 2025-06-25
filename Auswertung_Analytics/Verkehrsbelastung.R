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
library(scales)
library(lubridate)

file <- "D:/Erhebungen/06-2025 Böhler/Böhler12_06_2025_reduziert.csv"
# Read the CSV file into R
events <- read.csv(file, header = TRUE)

format_hhmm <- function(x) {
  format(as.POSIXct(x, format="%Y-%m-%d %H:%M:%S"), "%H:%M")
}

event = events %>%
  mutate(
    time = as.POSIXct(start.time, format="%Y-%m-%d %H:%M:%S")
  ) %>%
  filter(
    from.section == "A" | to.section == "A"
  ) %>%
  group_by(
    classification, time
  ) %>%
  summarise(
    anz = sum(count, na.rm = TRUE),
    .groups = "drop"
  ) 

d1 <- event %>%
  ggplot(aes(x=time, y=anz, color=classification))+
  geom_point()+
  geom_line()+
  #geom_smooth(method="loess")+
  scale_x_continuous(labels = format_hhmm,)+
  labs(title = "Digitale Verkehrsauswertung - Ein und Ausfahrten Areal Böjler", 
       subtitle = "12.06.2025",
       caption = paste("n =",format( nrow(event), big.mark = ".", decimal.mark = ",", scientific = FALSE)),
       x = "Uhrzeit",
       y = "Anzahl",
       color = "Farzeugart") +
  theme_light()+
  theme(legend.position = "bottom")

d1

out <- "D:/Erhebungen/06-2025 Böhler/Digitale_Verkehrsauswertung_12-06-2025_2.png"
png(filename=paste0(out), width = 21, height = 14.8, res = 600, units = 'cm')#A5
d1
dev.off()
