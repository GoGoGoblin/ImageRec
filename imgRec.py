import argparse
import base64
import os
import csv

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"" This program takes a directory name as an argument. It reads all image files in the designated directory      """
"""" and send them to Google Cloud Vision. The returned labels and associated file names are written in a csv file  """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def main(dir):
    """ Create service for Google Cloud API """
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    """ Create writer instance, open output file and write header """
    outputFile = 'label.csv'
    f = open(outputFile, 'w', newline='')
    fields = ['FILE NAME', 'LABEL']
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    """ Read file names in the dedignated directory """
    """ Set all necessary information to a json service request """
    for imgFile in os.listdir(dir):
        fileFullPath = dir + "\\" + imgFile
        with open(fileFullPath, 'rb') as image:
            imageContent = base64.b64encode(image.read())
            serviceRequest = service.images().annotate(body={
                'requests': [{
                    'image': {
                        'content': imageContent.decode('UTF-8')
                    },
                    'features': [{
                        'type': 'LABEL_DETECTION',
                        'maxResults': 1
                    }]
                }]
            })

            response = serviceRequest.execute()  #Get service execution result
            label = response['responses'][0]['labelAnnotations'][0]['description']  #Create a lable from a json response
            print('.....................................................')
            print('Detected label: %s for %s' % (label, imgFile))
            print('.......Writing file name and label to CSV file.......')
            writer.writerow({'FILE NAME': imgFile, 'LABEL': label})  #Write file name and label in csv file


""" Parse command line argument. Pass it to main program """
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir')
    args = parser.parse_args()
    main(args.dir)
