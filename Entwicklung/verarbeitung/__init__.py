## Import functions from modules
from .analyse_erfassung import (get_standard_values, dateien_laden, convert_to_pandas, 
                                test_zeiteingabe, zeiten_anpassen, dateiname_anpassen, make_onevideo,
                                videozeit_in_video)
from .opentracffic import (start_otc, short_ota)
from .video_verarbeitung import (extrahiere_datum, timeparser, get_next_starttime, 
                                 get_video_len_ffprobe, datei_name_anpassen, dateipfad_anpassen, 
                                 make_video_overlay, one_video)

## Define package-level variables
__version__ = "0.1.0"
__author__ = "Patrick Peters"

## Print a message when the package is imported
print(f"Help Package for 'Open Traffic Cam'- Graphical User Interface v{__version__} initialized")