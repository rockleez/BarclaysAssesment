'''
Created on Oct 9, 2017

@author: leemalin

Required:
Python 3

Tested On:
Pythong 3.5.2

'''
import argparse
import csv
import json
import logging
import os
import urllib.request


def get_json_data(url,description,add_params=[]):
    '''
    returns json data from specified url
    '''
    #timeout in seconds
    socket_timeout = 20
    
       
    try:        
        
        params_string = ''
        
        if len(add_params) > 0:
            for i in add_params:
                params_string = '?' + i
            
        url = url + params_string
        
        logger.info('retrieving %s data from: %s',description,url)
        logging.debug('socket timeout = %s' ,socket_timeout)
        response = urllib.request.urlopen(url, None, socket_timeout)
        
        return response.read()
    
    except Exception as ex:
        logger.error(ex)
        

def decode_json_data(data):
    ''' 
    returns dict of json data
    '''
    return json.loads(data.decode('utf-8'))
    

def print_json_data(data):
    '''
    pretty prints the json data to the log
    '''
    if data != None:            
        logger.info((json.dumps(data, indent=2)))
    
    else:
        logger.warn('no data to display')

if __name__ == '__main__':
    
    #######################################################
    #
    # Logging
    #
    #######################################################
    FORMAT = '[%(asctime)-15s] [%(levelname)s] %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('DogAPI')
    logger.setLevel(logging.DEBUG)
    
    
    parser = argparse.ArgumentParser(description='NFL Arrest API')
    parser.add_argument('-testdatafile', required=True, help='an integer for the accumulator')
    args = parser.parse_args()
    
    
    logger.info('----- NFL ARREST API -----')
    testdatafile = args.testdatafile
    logging.info('Test Data File: %s',testdatafile)
    
    #######################################################
    #
    # Test Data
    #
    #######################################################
    
    #Testdata index's
    TEST_ID     = 0
    URL         = 1
    DESCRIPTION = 2
    PARAMS      = 3
    ASSERT      = 4
    
    testdata = []
    
    test_result = []
    data_returned = False
    try:
        
        with open(testdatafile, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader)
            for row in reader:
                testdata.append(row)
        
    except Exception as ex:
        logger.error(ex)
        
    
    
    #######################################################
    #
    # Test Cases
    #
    #######################################################
    
    test_result = []

    
    for row in testdata:
        
        #reset variables
        assert_result = 'False'

        
        data = get_json_data(row[URL], row[DESCRIPTION],row[PARAMS])
        json_dict = decode_json_data(data)
                
        print_json_data(json_dict)
        
        
        
        if row[ASSERT] != '':
            
            logger.info('Asserting %s' ,row[ASSERT])
                 
            for item in json_dict:
                #keyword for special assert to validate data present
                if '**SYSTEM**:DataPresent' in row[ASSERT]:
                    assert_result = 'True'
                                         
                else:  
                    if row[ASSERT] in item:
                        assert_result = 'True'
   
        test_result.append([row[TEST_ID],assert_result]) 
     
 
    
    
    #######################################################
    #
    # Results
    #
    #######################################################
    
    try:
        outputfile = 'output.csv'
        if os.path.exists(outputfile):
                os.remove(outputfile)
                
        logger.info('writing test output file')
        with open(outputfile, 'w',newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)                     

            for result in test_result:
                wr.writerow(result)  
    
    except Exception as ex:
        logger.error(ex)
    
    finally:
        logger.info('exiting...')
        os._exit(0)
