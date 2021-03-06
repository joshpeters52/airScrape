import subprocess
import os.path
import re

class PhotoHandler:

    def __init__(self):
        self.TIF_PATH = "data/input.tif"
        self.TXT_PATH = "data/output"
        self.AIRPORT_CODES_PATH = "data/airport_codes.txt"
        self.AIRLINE_INDICATORS_PATH = "data/airline_indicators.txt"

        self.AIRPORT_CODES = self.buildAirportCodesSet()
        self.AIRLINE_INDICATORS = self.buildAirlineIndicatorsSet()

    def buildAirlineIndicatorsSet(self):
        text_file = open(self.AIRLINE_INDICATORS_PATH, "r")
        text = text_file.read()
        
        airline_indicators = set(text.split())

        return airline_indicators

    def buildAirportCodesSet(self):
        text_file = open(self.AIRPORT_CODES_PATH, "r")
        text = text_file.read()
        
        airport_codes = set()

        for i, character in enumerate(text):
            if character == '(':
                code = text[i+1:i+4]
                airport_codes.add(code)

        return airport_codes

    def convertPhotoToTextFile(self, path):
        delete_cmd = "rm " + self.TXT_PATH
        convert_cmd = "convert " + path + " -resize 200% -type Grayscale " + self.TIF_PATH
        ocr_cmd = "tesseract -l eng " + self.TIF_PATH + " " + self.TXT_PATH
        
        # delete old txt just in case
        process = process = subprocess.Popen(delete_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        # convert downloaded image to .tif format
        process = process = subprocess.Popen(convert_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        # find text in .tif and put in .txt
        process = process = subprocess.Popen(ocr_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        # !! should probably handle errors and stuff here

    def findDataInPicture(self, path):
        self.convertPhotoToTextFile(path)

        # something went wrong with OCR
        if not os.path.exists(self.TXT_PATH + ".txt"):
            print("ERROR: no output.txt")
            return None

        text_file = open(self.TXT_PATH + ".txt", "r")
        text = text_file.read()

        confirmationNumber = self.searchTextForConfirmation(text)

        airportCodes = self.searchTextForAirports(text)

        airline = self.searchTextForAirline(text)

        return confirmationNumber, airportCodes, airline

    def searchTextForAirports(self, text):
        matches = re.finditer(r'[A-Z]{3}', text)

        airports = set()

        for match in matches:
            possible_airport = match.group()
            if possible_airport in self.AIRPORT_CODES:
                airports.add(possible_airport)

        return airports

    def searchTextForAirline(self, text):
        for airline in self.AIRLINE_INDICATORS:
            airline = airline.lower()
            if airline in text.lower():
                return airline

        return None

    def searchTextForConfirmation(self, text):
        matches = re.finditer(r'\b[0-9A-Z]{6}\b', text)

        potential_codes = set()

        # matches with all 6 character capital alphanumeric strings
        for match in matches:
            possible_code = match.group()
            num_seen = False
            letter_seen = False

            # if code contains at least 1 num and 1 letter, this could be a confirmation code
            for character in possible_code:
                if character.isdigit():
                    num_seen = True
                else:
                    letter_seen = True

            if num_seen and letter_seen:
                potential_codes.add(possible_code)

        if len(potential_codes) > 0:
            return potential_codes
        else:
            return None