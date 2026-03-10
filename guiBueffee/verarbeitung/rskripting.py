# -*- coding: utf-8 -*- 
import os
import shutil
import subprocess

def check_r_installed() -> bool:
    """Prüft, ob R installiert ist und gibt die Version zurück."""
    try:
        # Prüfen ob R im PATH ist
        r_path = shutil.which("R")
        if not r_path:
            return True, "R nicht im PATH gefunden"
        
        # Version abrufent
        result = subprocess.run(
            [r_path, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            os.environ['R_HOME'] = r_path
            version_line = result.stderr.split('--')[0]
            return True, version_line
        else:
            return False, f"Fehler beim Ausführen: {result.stderr}"
            
    except FileNotFoundError:
        return False, "R-Executable nicht gefunden"
    except subprocess.TimeoutExpired:
        return False, "R-Aufruf hat zu lange gedauert"
    except Exception as e:
        return False, f"Unerwarteter Fehler: {str(e)}"    

r_home, _ = check_r_installed()
if r_home:
    os.environ['RPY2_CFFI_MODE'] = 'ABI'
    try:
        import rpy2.robjects as robjects #pip install rpy2==3.5.12
    except:
        pass

def ergebnisdarstellung(date:str, pfad_input:str, pfad_output:str=None) -> None:
    # pfad_output = r"D:/Erhebungen/2025-10 Kiel/Knoten 1/Digitale_Verkehrsauswertung_14_10_2025_nachmittag_knoten1.png"
    if pfad_output is None:
        pfad_output = pfad_input.replace(".csv", ".png")
    
    robjects.r(f"""
        #set working directory
        #setwd(dirname(rstudioapi::getSourceEditorContext()$path))
        #config_path <- Sys.getenv("R_CONFIG_PATH")
        #source(config_path)
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

        typ = c('bicycle', 'bus', 'car', 'motorcycle', 'person', 'train', 'truck')

        # Daten vorbereiten: Summen je Kategorie berechnen
        df <- events %>%
            group_by(classification) %>%
            summarise(summe = sum(count, na.rm = TRUE), .groups = "drop") %>%
            filter(summe > 10 & classification %in% typ) %>%
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

        gesammteFz <- sum(event$anz, na.rm = TRUE)

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
            caption = paste("n = ", format( gesammteFz, big.mark = ".", decimal.mark = ",", scientific = FALSE)),
            x = "Uhrzeit",
            y = "Anzahl",
            color = "Farzeugart") +
        theme_light()+
        theme(legend.position = "bottom")

        
        
        print(paste("Anzahl Zeilen in df:", nrow(event)))

        #d1
        
        png(filename=paste0(out), width = 21, height = 14.8, res = 600, units = 'cm')#A5
        d1
        print(d1)
        dev.off()

        
    """)
    # Datei öffnen
    if os.path.exists(pfad_output):
        os.startfile(pfad_output)

if __name__ == '__main__':
    pass