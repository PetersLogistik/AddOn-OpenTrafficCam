# -*- coding: utf-8 -*- 
import os
os.environ.setdefault("RPY2_CFFI_MODE", "ABI")   
from rpy2 import robjects 

def ergebnisdarstellung(date:str, pfad_input:str, pfad_output:str=None) -> None:
    # pfad_output = r"D:/Erhebungen/2025-10 Kiel/Knoten 1/Digitale_Verkehrsauswertung_14_10_2025_nachmittag_knoten1.png"
    if pfad_output is None:
        pfad_output = pfad_input.replace(".csv", ".png")
    
    robjects.r(f"""
        #set working directory
        setwd(dirname(rstudioapi::getSourceEditorContext()$path))
        config_path <- Sys.getenv("R_CONFIG_PATH")
        source(config_path)
        library(ggplot2)
        library(dplyr)
        library(png)
        library(ggpattern)
        library(hrbrthemes)
        library(scales)
        library(lubridate)

        date = "{date}"
        out <- "{pfad_output}"
        pfad = "{pfad_input}"
        file <- paste0(pfad)
        # Read the CSV file into R
        events <- read.csv(file, header = TRUE)

        # Daten vorbereiten: Summen je Kategorie berechnen
        df <- events %>%
        group_by(classification) %>%
        summarise(summe = sum(count, na.rm = TRUE), .groups = "drop") %>%
        filter(summe > 10) %>%
        pull(classification)

        #events <- events %>%
        #  filter(classification %in% df, classification != "person")

        event = events %>%
        filter(classification %in% df) %>%
        mutate(
            time = as.POSIXct(start.time, format="%Y-%m-%d %H:%M:%S")
        ) %>%
        #filter(
        #  from.section == "A" | to.section == "A"
        #) %>%
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
        #scale_x_datetime( breaks = seq(as.POSIXct(min(event$time)), as.POSIXct(max(event$time)), by = "1 hour"),
        #  labels = date_format("%H:%M")
        # )+
        #scale_x_continuous(labels = format_hhmm,)+
        labs(title = "Digitale Verkehrsauswertung - Kiel", 
            subtitle = date,
            caption = paste("n = ","None"),#,format( nrow(event), big.mark = ".", decimal.mark = ",", scientific = FALSE)),
            x = "Uhrzeit",
            y = "Anzahl",
            color = "Farzeugart") +
        theme_light()+
        theme(legend.position = "bottom")

        d1

        png(filename=paste0(out), width = 21, height = 14.8, res = 600, units = 'cm')#A5
        d1
        dev.off()
    """)