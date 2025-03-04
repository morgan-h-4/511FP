# Adapted from code found in this thread:
# https://stackoverflow.com/questions/32342935/using-opencv-with-tkinter

from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from tkinter import ttk
import argparse
import cv2
import os
import os.path
import logging

class ImageCaptureFrame(ttk.Frame):
    def __init__(self, parent=None, output_path = "./"):
        """ Initialize frame which uses OpenCV + Tkinter. 
            The frame:
            - Uses OpenCV video capture and periodically captures an image
              and show it in Tkinter
            - A save button allows saving the current image to output_path.
            - Consecutive numbering is used, starting at 00000001.jpg.
            - Checks if output_path exists, creates folder if not.
            - Checks if images are already present and continues numbering.
            
            attributes:
                vs (cv2 VideoSource): webcam to capture images from
                output_path (str): folder to save images to.
                count (int): number used to create the next filename.
                current_image (PIL Image): current image displayed
                btn (ttk Button): press to save image
                panel (ttk Label): to display image in frame
        """
        super().__init__(parent)
        self.grid()
        
        # 0 is your default video camera
        self.vs = cv2.VideoCapture(0) 
        
        # TODO: create output directory if it does not exist. 
        #       store output_path in an instance variable
        #       create a method to handle this?
        self.output_path = output_path
        
        # Create folder if it doesnt exist yet
        # output path points to desired folder
        # python has os folder makers 
        # os.makedirs()
        # os make dirs to make nested folders 
        # python lab2_image_capture_gui.py -o digits/train/one/
        # you dont make nested loops just manually make the folders by typing that above for each ^
        # 5 folders in train and 5 folders in valid for each finger

        # directory = 'digits'
        # path = os.path.join(output_path, directory)
        # if os.path.exists(directory):
        if os.path.exists(output_path):
            pass
        else:
            # path = os.path.join(output_path, directory)
            os.makedirs(output_path)
        # try:
        #     os.makedirs(path, exist_ok = True)
        #     print("Directory '%s' created successfully" %directory)
        # except OSError as error:
        #     print("Directory '%s' can not be created")
        
        # Get current largest file number already in folder
        self.count = self.get_current_count(output_path)
        logging.info("current image count in output folder is {}".format(self.count))
        
        # Prepare an attribute for the image
        self.current_image = None 
        
        # Custom method to execute when window is closed.
        parent.protocol('WM_DELETE_WINDOW', self.destructor)

         # Button to save current image to file
        btn = ttk.Button(self, text="Save", command=self.save_image)
        btn.grid(row=0, column=0, sticky='nwes', padx=10, pady=10)
        
        # Label to display image
        self.panel = ttk.Label(self)  
        self.panel.grid(row=1, column=0,padx=10, pady=10)

        # start the display image loop
        self.video_loop()

    def get_current_count(self, folder):

        """Checks for existing images and returns current file number.
        
            assumes jpg files have names 00000001.jpg, 00000002.jpg, etc.
        
            folder(str): directory to search for existing images
            
            return: (int) the current highest number of jpg filename
                          or 0 if no jpg files present.
        """
        #TODO: implement this method

        # i = 1
        # if os.path.isfile(folder) == True: # if file already exists
        #     i += 1 #currentfilenumber has to be the next number
        #     currentfilenumber = i
        # else: # if it doesnt exist
        #     currentfilenumber = i
        currentfilenumber = 1 
        for f in os.listdir(folder):
            if f.endswith("jpg"):
                try:
                    numberr = int(f.split(".")[0])
                    if numberr > currentfilenumber:
                        currentfilenumber = numberr
                except:
                    pass


        return currentfilenumber
        
    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter 
            
            The image is processed using PIL: 
            - crop left and right to make image smaller
            - mirror 
            - convert to Tkinter image
            
            Uses after() to call itself again after 30 msec.
        
        """
        # read frame from video stream
        ok, frame = self.vs.read()  
        # frame captured without any errors
        if ok:  
            # convert colors from BGR (opencv) to RGB (PIL)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            # convert image for PIL
            self.current_image = Image.fromarray(cv2image)  
            # Optional if camera is wide: crop 200 from left and right
            #self.current_image = ImageOps.crop(self.current_image, (200,0,200,0)) 
            # mirror, easier to locate objects
            self.current_image = ImageOps.mirror(self.current_image) 
            # convert image for tkinter for display, scale to 50% of size of original image
            imgtk = ImageTk.PhotoImage(image=ImageOps.scale(self.current_image, 0.5)) 
            # anchor imgtk so it does not get deleted by garbage-collector
            self.panel.imgtk = imgtk  
             # show the image
            self.panel.config(image=imgtk)
        # do this again after 30 msec
        self.after(30, self.video_loop) 

    def save_image(self):
        """ Save current image to the file 
        
        self.current_image is saved to output_path using
        consecutive numbering using self.count 
        zero-filled, eight-number format, e.g. 00000001.jpg.
        
        """
        #TODO: implement this method
         
        # logging.info("save not yet implemented ")
        

        name = "{:08d}.jpg".format(self.count)
        # self.current_image.save(self.output_path("00000000{}.jpg".format(thenumber)))
        path = os.path.join(self.output_path, name)
        self.current_image.save(path)
        self.count += 1
        

    def destructor(self):
        """ Destroy the root object and release all resources """
        logging.info("closing GUI...")
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # close OpenCV windows
        self.master.destroy() # close the Tk window

        
def main():
    logging.basicConfig(level=logging.INFO)
    
    # construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", default="./",
        help="path to output directory to store images (default: current folder")
    args = parser.parse_args()
    logging.info(f"saving images to {args.output}")

    
    # start the app
    logging.info("starting GUI...")
    gui = tk.Tk() 
    gui.title("Image Capture")  
    ImageCaptureFrame(gui, args.output)
    gui.mainloop()
        
if __name__ == '__main__':
    main()


