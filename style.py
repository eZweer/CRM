class stylesheet:
    
    
    def __init__(self):
        self.style = {   "background":"#ffffff",
                    "background_frame":"#808080",
                    "font_type":"Script MT Bold",
                    "foreground_color":"black",
                    "foreground_color_header":"black",
                    "relief_type":"sunken"}
        self.frame_styles = {"relief": self.style["relief_type"],
                            "bd": 3, "bg": self.style["background"],
                            "fg": self.style["foreground_color"], "font": (self.style["font_type"], 12)}  
        self.text_styles = {"font": (self.style["font_type"], 16),
                       "background": self.style["background"],
                       "foreground": self.style["foreground_color"]} 
            
      