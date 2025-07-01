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

date = "03.06.2025"
out <- "D:/Erhebungen/06-2025 Böhler/Digitale_Verkehrsauswertung_03_06_2025_3.png"
file <- paste0("D:/Erhebungen/06-2025 Böhler/Böhler03_06_2025_reduziert.csv")
# Read the CSV file into R
events <- read.csv(file, header = TRUE)

# Daten vorbereiten: Summen je Kategorie berechnen
df <- events %>%
  group_by(classification) %>%
  summarise(summe = sum(count, na.rm = TRUE), .groups = "drop") %>%
  filter(summe > 10) %>%
  pull(classification)

events <- events %>%
  filter(classification %in% df, classification != "person")

event = events %>%
  filter(classification %in% df) %>%
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
  geom_label(aes(label = anz), nudge_y = 1, size = 3)+
  scale_x_datetime(
    breaks = seq(as.POSIXct(min(event$time)), as.POSIXct(max(event$time)), by = "1 hour"),
    labels = date_format("%H:%M")
    )+
  #scale_x_continuous(labels = format_hhmm,)+
  labs(title = "Digitale Verkehrsauswertung - Ein und Ausfahrten Areal Böjler", 
       subtitle = date,
       caption = paste("n =",format( nrow(event), big.mark = ".", decimal.mark = ",", scientific = FALSE)),
       x = "Uhrzeit",
       y = "Anzahl",
       color = "Farzeugart") +
  theme_light()+
  theme(legend.position = "bottom")

d1

png(filename=paste0(out), width = 21, height = 14.8, res = 600, units = 'cm')#A5
d1
dev.off()
