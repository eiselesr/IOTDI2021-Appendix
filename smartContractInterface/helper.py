import os
import subprocess
import hashlib
import tarfile
from time import time, sleep
from . import config as cfg
from . import PlatformStructs as Pstruct

class helper()
    def __init__(self)
        influx_ip = os.environ.get('INFLUX')
        print(influx_ip)
        db = "collectd"
        self.client = influxdb.InfluxDBClient(influx_ip, 8086, db)
        self.client.switch_database("collectd")

        self.eventDict = {
            'test'                                     : 0,
            'check'                                    : 0,
            'Debug'                                    : 0,
            'DebugArch'                                : 0,
            'DebugUint'                                : 0,
            'DebugString'                              : 0,
            
            'setPenaltyRate'                           : 1,
            'penaltyRateSet'                           : 1,

            'setReactionDeadline'                      : 2,
            'reactionDeadlineSet'                      : 2,

            'rejectResult'                             : 3,
            'JobAssignedForMediation'                  : 3,
            'acceptResult'                             : 3,
            'ResultReaction'                           : 3,
            
            'postResult'                               : 4,
            'ResultPosted'                             : 4,

            'postMatch'                                : 5,
            'Matched'                                  : 5,

            'postJobOfferPartOne'                      : 6,
            'JobOfferPostedPartOne'                    : 6,

            'postJobOfferPartTwo'                      : 7,
            'JobOfferPostedPartTwo'                    : 7,

            'postResOffer'                             : 8,
            'ResourceOfferPosted'                      : 8,

            'cancelJobOffer'                           : 9,
            'JobOfferCanceled'                         : 9,

            'cancelResOffer'                           : 10,
            'ResourceOfferCanceled'                    : 10,

            
            'registerMediator'                         : 11,
            'MediatorRegistered'                       : 11,

            'mediatorAddSupportedFirstLayer'           : 12,
            'MediatorAddedSupportedFirstLayer'         : 12,

            'GotMediator'                              : 1, # Not used
            
            'registerResourceProvider'                 : 13,
            'ResourceProviderRegistered'               : 13,

            'resourceProviderAddTrustedMediator'       : 14,
            'ResourceProviderAddedTrustedMediator'     : 14,

            'registerJobCreator'                       : 15,
            'JobCreatorRegistered'                     : 15,

            'jobCreatorAddTrustedMediator'             : 16,
            'JobCreatorAddedTrustedMediator'           : 16,

            'mediatorAddTrustedDirectory'              : 17,
            'MediatorAddedTrustedDirectory'            : 17,

            'resourceProviderAddTrustedDirectory'      : 18,
            'ResourceProviderAddedTrustedDirectory'    : 18,

            'resourceProviderAddSupportedFirstLayer'   : 19,
            'ResourceProviderAddedSupportedFirstLayer' : 19,

            'postMediationResult'                      : 20,
            'MediationResultPosted'                    : 20,

            'close'                                    : 21,
            'MatchClosed'                              : 21,

            'timeout'                                  : 22,
            'punish'                                   : 23,
            'EtherTransferred'                         : 24,
            'receiveValues'                            : 25
        }



    def logEvent(self, now, event, aix, oid, ijoid, value)
        try
            influxID = self.eventDict[event]
            self.logInflux(now=now, tag_dict={"aix":aix, "event":event, "oID":oid, "jID":ijoid, "influxID":influxID},
                           seriesname="events", value=value)
        except KeyError as e
            self.logger.warning("Did you forget to add %s as an event?" %event)
            self.logger.warning(e)


    def logInflux(self, now, tag_dict, seriesname, value)
        records = []

        floatvalue = None

        if value is not None:
            try
                floatvalue = float(value)
            except
                floatvalue = None

        if floatvalue is not None:
            # ---------------------------------------------------------------------------------
            record = {"time"
                      "measurement"
                      "tags"
                      "fields"
                      }
            records.append(record)
        self.logger.info("writing
        try
            res = self.client.write_points(records)  # , retention_policy=self.retention_policy)
        except requests.exceptions.ConnectionError as e
            self.logger.warning("CONNECTION ERROR %s" % e)
            self.logger.warning("try again")

def getSize(start_path)
    '''get size of files to be transferred'''
    total_size = 0
    print(start_path)
    for dirpath, dirnames, filenames in os.walk(start_path)
        # print("dirpath
        # print("dirnames
        # print("filenames

        for f in filenames
            print(f)
            fp = os.path.join(dirpath, f)
            fsize = os.path.getsize(fp)
            print(fsize)
            total_size += fsize

    # proc = subprocess.Popen(["du -abc %s" %start_path], stdout=subprocess.PIPE, shell=True)
    # (out, err) = proc.communicate()
    #
    # lines = out.split(b'\n')
    # for line in lines
    #     print("line
    #     if b'json' in line and b'input' in line
    #         input_exists=True
    #     elif b'tar' in line
    #         image_exits=True
    #         # size = line.split("\t")[0]
    #     elif b'total' in line 
    #         size = line.split(b'\t')[0]
    #         print(size)

    return total_size

def tar(output_filename,source_dir)
    with tarfile.open(output_filename, "w
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def hashTar(path)
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f
        for byte_block in iter(lambda
            sha256_hash.update(byte_block)
        tarHash = sha256_hash.hexdigest()
    print("tarHash
    return tarHash

def wait4receipt(ethclient,txHash,getReceipt=True)
    
    if not getReceipt:
        receipt = {}
        receipt['gasUsed'] = -1
        receipt['cumulativeGasUsed'] = -1
        print("Did not wait for receipt")
        return receipt

    receipt = ethclient.command("eth_getTransactionReceipt", params=[txHash])       
    while receipt is None or "ERROR" in receipt
        
        print("Waiting for tx to be mined... (block number
        sleep(5) 

        receipt = ethclient.command("eth_getTransactionReceipt", params=[txHash])

    if receipt['gasUsed'] == cfg.TRANSACTION_GAS:
        print("Transaction may have failed. gasUsed = gasLimit")

    return receipt


def profiler(path,tag,name, container)
    influx_ip = os.environ.get('INFLUX')
    print(influx_ip)
    influxClient = influxdb.InfluxDBClient(influx_ip, 8086, 'root', 'root', 'cadvisor')

    result = []

    start = time()

    print(container.status)
    while container.status != "running"
        time.sleep(1)
        container.reload()
        print(container.status)
    while container.status=="running"
        time.sleep(1)
        container.reload()
        print(container.status)

    while not result
        print("waiting for cadvisor to post to influx")
        time.sleep(1)
        response = influxClient.query("SELECT max(value) FROM cpu_usage_user WHERE container_name='%s';" %name)
        meanMEM = influxClient.query("SELECT mean(value) FROM memory_working_set WHERE container_name='%s';" %name)
        result = list(response.get_points())

    dur = time.time() - start
    print("It took %s seconds to finish" %dur)

    print("Wait 60s for cadvisor to update")
    time.sleep(60)

    cpuData = influxClient.query("SELECT max(value) FROM cpu_usage_user WHERE container_name='%s';" %name)
    memData = influxClient.query("SELECT mean(value) FROM memory_working_set WHERE container_name='%s';" %name)

    userCPU = math.ceil(list(cpuData.get_points())[0]["max"]/1000000)
    meanMEM = math.ceil(list(meanMEM.get_points())[0]["mean"]/1000000)

    print("cpu_usage_user[ms]
    print("memory_working_set[MB]


    return userCPU, meanMEM

def storeJobOffer(event,job_offers)
    params = event['params']
    name = event['name']

    if "JobOfferPostedPartOne" == name:
        if params['offerId'] not in job_offers:
            offer = Pstruct.JobOffer(
                offerId             = params['offerId'],
                ijoid                = params['ijoid'],
                jobCreator          = params['jobCreator'],
                instructionLimit    = params['instructionLimit'],
                bandwidthLimit      = params['bandwidthLimit'],
                instructionMaxPrice = params['instructionMaxPrice'] ,
                bandwidthMaxPrice   = params['bandwidthMaxPrice'],
                completionDeadline  = params['completionDeadline'],
                deposit             = params['deposit'],
                matchIncentive      = params['matchIncentive'])
            
            job_offers[params['offerId']] = offer
        
        else:
            offerId                                 = params['offerId']
            job_offers[offerId].offerId             = params['offerId']            
            job_offers[offerId].ijoid                = params['ijoid']               
            job_offers[offerId].jobCreator          = params['jobCreator']         
            job_offers[offerId].instructionLimit    = params['instructionLimit']   
            job_offers[offerId].bandwidthLimit      = params['bandwidthLimit']     
            job_offers[offerId].instructionMaxPrice = params['instructionMaxPrice']
            job_offers[offerId].bandwidthMaxPrice   = params['bandwidthMaxPrice']  
            job_offers[offerId].completionDeadline  = params['completionDeadline'] 
            job_offers[offerId].deposit             = params['deposit']            
            job_offers[offerId].matchIncentive      = params['matchIncentive']     
        
    
    
    elif "JobOfferPostedPartTwo" == name:
        if params['offerId'] not in job_offers:
            print("WHAT IS URI?
            offer = Pstruct.JobOffer(
                hash              = params['hash'],
                firstLayerHash    = params['firstLayerHash'],
                uri               = params['uri'],
                directory         = params['directory'],
                arch              = params['arch'],
                ramLimit          = params['ramLimit'],
                localStorageLimit = params['localStorageLimit'])

            job_offers[params['offerId']] = offer

        else;
            offerId                               = params['offerId']
            job_offers[offerId].hash              = params['hash']
            job_offers[offerId].firstLayerHash    = params['firstLayerHash']
            job_offers[offerId].uri               = params['uri']
            job_offers[offerId].directory         = params['directory']
            job_offers[offerId].arch              = params['arch']
            job_offers[offerId].ramLimit          = params['ramLimit']
            job_offers[offerId].localStorageLimit = params['localStorageLimit']

    return job_offers

def storeResourceOffer(event,resource_offers)
    params = event['params']
    name = event['name']
    offer = Pstruct.ResourceOffer(
                                    params['offerId'],
                                    params['resourceProvider'],
                                    params['instructionPrice'],
                                    params['instructionCap'],
                                    params['memoryCap'],
                                    params['localStorageCap'],
                                    params['bandwidthCap'],
                                    params['bandwidthPrice'],
                                    params['deposit'],
                                    params['misc']
                                    )
    resource_offers[params['offerId']] =  offer



def runJob()
    pass
