import requests # Libreria para hacer peticiones HTTP
import json # Libreria para manejar JSON
import os # Libreria para limpiar la consola
import pandas as pd # Libreria para crear tablas

# Esta es la API Key que se obtiene en el portal de Cloud _One 
apiki=input("Bienvenido a la herramienta de optimizacion de costos de Trend Micro Cloud One Conformity, por favor ingrese su API Key: ") # Ingresar la API Key
# Ingresar el nombre del cliente, este será el nombre que tendrá el archivo
nameCustomer=input("Por favor ingrese el nombre del cliente: ")
if not os.path.exists(nameCustomer): # Si no existe el directorio
    os.makedirs(nameCustomer) # Crear el directorio 
fileToSave= pd.ExcelWriter('{}/{}.xlsx'.format(nameCustomer,nameCustomer)) # Crear el archivo de excel
probemos={}
restData={}
recomendationsByServiceRelationships={}
accInfo=[]
nameServ=[]
contadordeplataquesegastaporrecursoquenoseliminamuchachoslimpienloqueusenydemenaccesoalacuentaporquemegaste33usdenlamia=0
headers = { # Headers para la peticion
  'Content-Type': 'application/vnd.api+json', # Tipo de contenido
    "Authorization": "ApiKey {}".format(apiki), # API Key
      }
 

def getCost(idAccC1,awsID): # Funcion para obtener el costo de una cuenta
    # global testxd
    global restData
    global nameServ
    global probemos
    global contadordeplataquesegastaporrecursoquenoseliminamuchachoslimpienloqueusenydemenaccesoalacuentaporquemegaste33usdenlamia
    global recomendationsByServiceRelationships
    url = "https://conformity.us-1.cloudone.trendmicro.com/api/checks?accountIds={}&filter[categories]={}&filter[statuses]=FAILURE".format(idAccC1,"cost-optimisation") # URL para obtener los costos
    response = requests.get(url, headers=headers) # Peticion
    costos=response.json() # Respuesta en formato JSON
    amountWaste=0 # Variable para almacenar el costo total
    
    tam= len(costos["data"])
    listaTemp=[]
    print("::::::::::::::::::::::::::::::::::::::::INICIO DE LA CUENTA:::::::::::::::::::::::::::::::::::::::::::::::::") 
    for i in range(tam): # Ciclo para obtener los datos de cada servicio
        nameAccount= awsID 
        try:
            tipoNameSrv= str(costos["data"][i]["attributes"]["service"])
            idResource= str(costos["data"][i]["attributes"]["resource"])
            region=str(costos["data"][i]["attributes"]["region"])
            title= str(costos["data"][i]["attributes"]["link-title"])
            message=str(costos["data"][i]["attributes"]["message"])
            tipoServ = str(costos["data"][i]["attributes"]["descriptorType"])
            risklevel= str(costos["data"][i]["attributes"]["risk-level"])
            ruleId= str(costos["data"][i]["relationships"]["rule"]["data"]["id"])
            if tipoServ not in restData: # Si el servicio no esta en la lista
                restData[tipoServ]=[] 
                saveNameService(tipoServ)
                print("No existe el servicio: ",tipoServ," en la lista por eso se agrega")
            
            if ((tipoServ == "ebs-volume") and ((ruleId == "EBS-003") or (ruleId == "EBS-010"))): # Si el servicio es EBS y el ruleId es EBS-003 o EBS-010 
                if 'ebs-risk' not in restData:
                    restData['ebs-risk']=[]
                    saveNameService('ebs-risk')
                    print("No existe el servicio: ","ebs-risk"," en la lista por eso se agrega")
                
                    

                dataExtra=(costos["data"][i]["attributes"]["extradata"])
                cost = (costos["data"][i]["attributes"]["cost"])
                amountWaste= amountWaste + float(cost)
                contadordeplataquesegastaporrecursoquenoseliminamuchachoslimpienloqueusenydemenaccesoalacuentaporquemegaste33usdenlamia+=amountWaste
                createTime = None
                volSize = None
                volType = None
                insId = None
            
                
                try:
                    for searchMoreInfo in range (len(dataExtra)):
                        if dataExtra[searchMoreInfo]["name"] == "CREATE_TIME" or dataExtra[searchMoreInfo]["name"] =="CreateTime":
                            createTime = dataExtra[searchMoreInfo]["value"]
                        if dataExtra[searchMoreInfo]["name"] == "VOLUME_SIZE" or dataExtra[searchMoreInfo]["name"] == "Size":
                            volSize = dataExtra[searchMoreInfo]["value"]
                        if dataExtra[searchMoreInfo]["name"] == "VOLUME_TYPE" or dataExtra[searchMoreInfo]["name"] == "VolumeType":
                            volType = dataExtra[searchMoreInfo]["value"]
                        if dataExtra[searchMoreInfo]["name"] == "InstanceId":
                            insId = dataExtra[searchMoreInfo]["value"]
                       
                    restData["ebs-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"createTime":createTime,"volSize":volSize,"volType":volType,"insId":insId,"wasted-total":amountWaste})    
                except KeyError as e:
                    if (str(e) == dataExtra[searchMoreInfo]["name"] == "InstanceId"):
                        insId = None
                        restData["ebs-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"createTime":createTime,"volSize":volSize,"volType":volType,"insId":insId,"wasted-total":amountWaste})    
            
            
            if ((tipoServ == "rds-dbinstance") and ((ruleId == "RDS-019") or (ruleId == "RDS-013"))):
                if 'rds-risk' not in restData:
                    restData['rds-risk']=[]
                    saveNameService('rds-risk')
                    print("No existe el servicio: ","rds-risk"," en la lista por eso se agrega")
                
                dataExtra=(costos["data"][i]["attributes"]["extradata"])
                cost = (costos["data"][i]["attributes"]["cost"])
                amountWaste= amountWaste + float(cost)
                DBInstanceClass = None
                totalIops = None
                writeIops = None
                cpuUtilization = None
                # insId = None
            
                try:
                    for searchMoreInfo in range (len(dataExtra)):
                        if dataExtra[searchMoreInfo]["name"] == "DBInstanceClass":
                            DBInstanceClass = dataExtra[searchMoreInfo]["value"]
                        if dataExtra[searchMoreInfo]["name"] == "TOTAL_IOPS":
                            totalIops = dataExtra[searchMoreInfo]["value"]
                        if dataExtra[searchMoreInfo]["name"] == "WRITE_IOPS":
                            writeIops = dataExtra[searchMoreInfo]["value"]
                        if dataExtra[searchMoreInfo]["name"] == "CPU_UTILIZATION":
                            cpuUtilization = dataExtra[searchMoreInfo]["value"]
                    if idResource in [item.get('idResource') for item in restData['rds-risk']]:
                        for item in restData['rds-risk']:
                            if item['idResource'] == idResource:
                                if "DBInstanceClass" not in item:
                                    item["DBInstanceClass"] = DBInstanceClass
                                if "TOTAL_IOPS" not in item:
                                    item["TOTAL_IOPS"] = totalIops
                                if "WRITE_IOPS" not in item:
                                    item["WRITE_IOPS"] = writeIops
                                if "cpu-utilization" not in item:
                                    item["cpu-utilization"] = cpuUtilization
                                message="The rds instance {}, is underutilized and idle. Is recommended to stop the instance to avoid unnecessary costs. Because, The CPU utilization is ({}%) and the IOPS is ({}) of the total provisioned. Also the instance has a DB Instance Class of ({}) and its not using the full capacity of the instance. This missconfiguration is causing a waste ${}".format(idResource,cpuUtilization,totalIops,DBInstanceClass,cost)
                                item["message"] = message
                                
                    else:
                        restData["rds-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"DBInstanceClass":DBInstanceClass,"TOTAL_IOPS":totalIops, "WRITE_IOPS":writeIops,"cpu-utilization":cpuUtilization,"wasted-total":amountWaste})
                except KeyError as e:
                    print("Error: ",str(e))
                    # if (str(e) == dataExtra[searchMoreInfo]["name"] == "InstanceId"):
                    #     insId = None
                    #     restData["ebs-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"DBInstanceClass":DBInstanceClass,"TOTAL_IOPS":totalIops,"cpu-utilization":cpuUtilization,"wasted-total":amountWaste})    
            # restData[tipoServ].append({"Account Name":nameAccount,"service":tipoNameSrv,"title":title,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region})
            if ((tipoServ == "ec2-instance") and ((ruleId == "EC2-047") or (ruleId == "EC2-055"))):
                if 'ec2-risk' not in restData:
                    restData['ec2-risk']=[]
                    saveNameService('ec2-risk')
                    print("No existe el servicio: ","ec2-risk"," en la lista por eso se agrega")
                
                dataExtra=(costos["data"][i]["attributes"]["extradata"])
                cost = (costos["data"][i]["attributes"]["cost"])
                amountWaste= amountWaste + float(cost)
                DBInstanceClass = None
                totalIops = None
                cpuUtilization = None
                # plataperdia = plataperdia + cost
                # insId = None
            
                try:
                    for searchMoreInfo in range (len(dataExtra)):
                        if dataExtra[searchMoreInfo]["name"] == "TYPE":
                            DBInstanceClass = dataExtra[searchMoreInfo]["value"]
                        if dataExtra[searchMoreInfo]["name"] == "NETWORK_UTILIZATION":
                            totalIops = dataExtra[searchMoreInfo]["value"]
                        if dataExtra[searchMoreInfo]["name"] == "CPU_UTILIZATION":
                            cpuUtilization = dataExtra[searchMoreInfo]["value"]
                    if idResource in [item.get('idResource') for item in restData['ec2-risk']]:
                        for item in restData['ec2-risk']:
                            if item['idResource'] == idResource:
                                if "TYPE" not in item:
                                    item["TYPE"] = DBInstanceClass
                                if "NETWORK_UTILIZATION" not in item:
                                    item["NETWORK_UTILIZATION"] = totalIops
                               
                                if "CPU_UTILIZATION" not in item:
                                    item["CPU_UTILIZATION"] = cpuUtilization
                                message="The instance {}, is underutilized and idle. Is recommended to stop the instance to avoid unnecessary costs. Because, The CPU utilization is ({}%) of the total provisioned. Also the instance has a type of ({}) and its not using the full capacity of the instance and network utilization is {}. This missconfiguration is causing a waste ${}".format(idResource,cpuUtilization,DBInstanceClass,totalIops,cost)
                                item["message"] = message
                                
                    else:
                        restData["ec2-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"Type":DBInstanceClass,"NETWORK_UTILIZATION":totalIops,"CPU_UTILIZATION":cpuUtilization,"wasted-total":amountWaste})
                except KeyError as e:
                    print("Error: ",str(e))
            if (((tipoServ == "ebs-volume") and ((ruleId == "EBS-003") or (ruleId == "EBS-010"))) or (((tipoServ == "ec2-image") and (ruleId == "EC2-026"))) or ((tipoServ == "ec2-address") and (ruleId == "EC2-024")) or ((tipoServ == "autoscaling-group") and (ruleId == "ASG-002")) or ((tipoServ == "elbv2-loadbalancer") and (ruleId == "ELBv2-008")) ):
                
                if 'not-used-risk' not in restData:
                    restData['not-used-risk']=[]
                    saveNameService('not-used-risk')
                    print("No existe el servicio: ","not-used-risk"," en la lista por eso se agrega")
                dataExtra=(costos["data"][i]["attributes"]["extradata"])
                cost = (costos["data"][i]["attributes"]["cost"])
                try:
                    if(tipoServ=="ebs-volume"): 
                        createTime = None
                        volSize = None
                        volType = None
                        insId = None
                        message= ""
                        for searchMoreInfo in range (len(dataExtra)):
                            if dataExtra[searchMoreInfo]["name"] == "CREATE_TIME" or dataExtra[searchMoreInfo]["name"] =="CreateTime":
                                createTime = dataExtra[searchMoreInfo]["value"]
                            if dataExtra[searchMoreInfo]["name"] == "VOLUME_SIZE" or dataExtra[searchMoreInfo]["name"] == "Size":
                                volSize = dataExtra[searchMoreInfo]["value"]
                            if dataExtra[searchMoreInfo]["name"] == "VOLUME_TYPE" or dataExtra[searchMoreInfo]["name"] == "VolumeType":
                                volType = dataExtra[searchMoreInfo]["value"]
                            if dataExtra[searchMoreInfo]["name"] == "InstanceId":
                                insId = dataExtra[searchMoreInfo]["value"]
                        message="The EBS volume '{}', is not used. Is recommended to delete the volume to avoid unnecessary costs or move the data to another storage more cheaper like S3. Because, The volume was created on {} and has a size of {}GB and a type of {}. This missconfiguration is causing a waste ${}".format(idResource,createTime,volSize,volType,cost)
                        restData["not-used-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"wasted-total":amountWaste})
                    if(tipoServ=="ec2-image"):
                        volSize= None
                        volType= None
                        message= ""
                        for searchMoreInfo in range (len(dataExtra)):
                            if dataExtra[searchMoreInfo]["name"] == "VOLUME_SIZE":
                                volSize = dataExtra[searchMoreInfo]["value"]
                            if dataExtra[searchMoreInfo]["name"] == "VOLUME_TYPE":
                                volType = dataExtra[searchMoreInfo]["value"]
                        message="The AMI '{}', is not used. Is recommended to delete the AMI to avoid unnecessary costs. Because, The AMI has a size of {}GB and a type of {}. This missconfiguration is causing a waste ${}, and is important to mention the risk because the AMI can be used to create a new instance and the instance can be used to attack the network for example".format(idResource,volSize,volType,cost)
                        restData["not-used-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"wasted-total":amountWaste})

                    if(tipoServ=="autoscaling-group"):
                        message= ""
                        message="The AutoScaling Group '{}' is empty, because it has 0 instances associated. Its recommended to delete the AutoScaling Group to avoid unnecessary costs. Because, The AutoScaling Group is not being used. This missconfiguration is causing a waste ${}".format(idResource,cost)
                        restData["not-used-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"wasted-total":amountWaste})

                    if(tipoServ=="elbv2-loadbalancer"):
                        message= ""
                        countInstances= None
                        for searchMoreInfo in range (len(dataExtra)):
                            if dataExtra[searchMoreInfo]["name"] == "NumberOfHealthyInstances":
                                countInstances = dataExtra[searchMoreInfo]["value"]
                        message= "The Load Balancer '{}' is unused, the minimum number of healthy instances should be 2, but the current number of healthy instances is {}. Its recommended to delete the Load Balancer to avoid unnecessary costs. Because, The Load Balancer is not being used. This missconfiguration is causing a waste ${}".format(idResource,countInstances,cost)
                        restData["not-used-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"wasted-total":amountWaste})
                    if(tipoServ=="ec2-address"):
                        message= ""
                        message="The IP {} is not associated with any instance. The recommendation is to delete the IP or associate it with an instance if it is necessary. The risk of that missconfiguration is uneeded costs of ${}".format(idResource,cost)
                        restData["not-used-risk"].append({"Account Name":nameAccount,"service":tipoNameSrv,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region,"cost":cost,"wasted-total":amountWaste})
                except KeyError as e:
                    print("Error: ",str(e))
                    print("No se encontro el servicio: ",str(restData[tipoServ]))



            restData[tipoServ].append({"Account Name":nameAccount,"service":tipoNameSrv,"title":title,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region})


        except KeyError as e:
            verify = str(e)
            if verify == "descriptorType":
                tipoServ = None
                tipoNameSrv= str(costos["data"][i]["attributes"]["service"])
                idResource= str(costos["data"][i]["attributes"]["resource"])
                region=str(costos["data"][i]["attributes"]["region"])
                title= str(costos["data"][i]["attributes"]["link-title"])
                message=str(costos["data"][i]["attributes"]["message"])
                risklevel= str(costos["data"][i]["attributes"]["risk-level"])
                if tipoServ not in restData: # Si el servicio no esta en la lista
                    restData[tipoServ]=[] 
                    saveNameService(tipoServ)
                    print("No existe el servicio: ",tipoServ," en la lista por eso se agrega")

                restData[tipoServ].append({"Account Name":nameAccount,"service":tipoNameSrv,"title":title,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region})
            if verify == "service":
                tipoServ = str(costos["data"][i]["attributes"]["descriptorType"])
                tipoNameSrv= None
                idResource= str(costos["data"][i]["attributes"]["resource"])
                region=str(costos["data"][i]["attributes"]["region"])
                title= str(costos["data"][i]["attributes"]["link-title"])
                message=str(costos["data"][i]["attributes"]["message"])
                risklevel= str(costos["data"][i]["attributes"]["risk-level"])
                if tipoServ not in restData:
                    restData[tipoServ]=[]
                    saveNameService(tipoServ)
                    print("No existe el servicio: ",tipoServ," en la lista por eso se agrega")
                restData[tipoServ].append({"Account Name":nameAccount,"service":tipoNameSrv,"title":title,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region})
            if verify == "resource":
                tipoServ = str(costos["data"][i]["attributes"]["descriptorType"])
                tipoNameSrv= str(costos["data"][i]["attributes"]["service"])
                idResource= None
                region=str(costos["data"][i]["attributes"]["region"])
                title= str(costos["data"][i]["attributes"]["link-title"])
                message=str(costos["data"][i]["attributes"]["message"])
                risklevel= str(costos["data"][i]["attributes"]["risk-level"])
                if tipoServ not in restData:
                    restData[tipoServ]=[]
                    saveNameService(tipoServ)
                    print("No existe el servicio: ",tipoServ," en la lista por eso se agrega")
                restData[tipoServ].append({"Account Name":nameAccount,"service":tipoNameSrv,"title":title,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region})
            if verify == "region":
                tipoServ = str(costos["data"][i]["attributes"]["descriptorType"])
                tipoNameSrv= str(costos["data"][i]["attributes"]["service"])
                idResource= str(costos["data"][i]["attributes"]["resource"])
                region=None
                title= str(costos["data"][i]["attributes"]["link-title"])
                message=str(costos["data"][i]["attributes"]["message"])
                risklevel= str(costos["data"][i]["attributes"]["risk-level"])
                if tipoServ not in restData:
                    restData[tipoServ]=[]
                    saveNameService(tipoServ)
                    print("No existe el servicio: ",tipoServ," en la lista por eso se agrega")
                restData[tipoServ].append({"Account Name":nameAccount,"service":tipoNameSrv,"title":title,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region})
            if verify == "link-title":
                tipoServ = str(costos["data"][i]["attributes"]["descriptorType"])
                tipoNameSrv= str(costos["data"][i]["attributes"]["service"])
                idResource= str(costos["data"][i]["attributes"]["resource"])
                region=str(costos["data"][i]["attributes"]["region"])
                title= None
                message=str(costos["data"][i]["attributes"]["message"])
                risklevel= str(costos["data"][i]["attributes"]["risk-level"])
                if tipoServ not in restData:
                    restData[tipoServ]=[]
                    saveNameService(tipoServ)
                    print("No existe el servicio: ",tipoServ," en la lista por eso se agrega")
                restData[tipoServ].append({"Account Name":nameAccount,"service":tipoNameSrv,"title":title,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region})
            if verify == "message":
                tipoServ = str(costos["data"][i]["attributes"]["descriptorType"])
                tipoNameSrv= str(costos["data"][i]["attributes"]["service"])
                idResource= str(costos["data"][i]["attributes"]["resource"])
                region=str(costos["data"][i]["attributes"]["region"])
                title= str(costos["data"][i]["attributes"]["link-title"])
                message=None
                risklevel= str(costos["data"][i]["attributes"]["risk-level"])
                if tipoServ not in restData:
                    restData[tipoServ]=[]
                    saveNameService(tipoServ)
                    print("No existe el servicio: ",tipoServ," en la lista por eso se agrega")
                restData[tipoServ].append({"Account Name":nameAccount,"service":tipoNameSrv,"title":title,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region})
            if verify == "risk-level":
                tipoServ = str(costos["data"][i]["attributes"]["descriptorType"])
                tipoNameSrv= str(costos["data"][i]["attributes"]["service"])
                idResource= str(costos["data"][i]["attributes"]["resource"])
                region=str(costos["data"][i]["attributes"]["region"])
                title= str(costos["data"][i]["attributes"]["link-title"])
                message=str(costos["data"][i]["attributes"]["message"])
                risklevel= None
                if tipoServ not in restData:
                    restData[tipoServ]=[]
                    saveNameService(tipoServ)
                    print("No existe el servicio: ",tipoServ," en la lista por eso se agrega")
                restData[tipoServ].append({"Account Name":nameAccount,"service":tipoNameSrv,"title":title,"idResource":idResource,"message":message,"risklevel":risklevel,"region":region})
    return amountWaste # Retornar el costo total


def saveNameService(serviceName):
    global nameServ # Lista para almacenar la informacion de las cuentas
    nameServ.append(str(serviceName))

def dfToSheet():
    global restData
    global probemos
    global nameServ
    print(nameServ)
    for i in range (len(nameServ)):
        print("i: ",i)
        print("nameServ: ",nameServ[i])
        print("restData[nameServ[i]]: ",restData[nameServ[i]])
        if nameServ[i] == "ebs-risk":
            df = pd.DataFrame(restData[nameServ[i]])
            df = df.append({"Account Name":None,"service":None,"idResource":None,"message":None,"risklevel":None,"region":None,"cost":None,"createTime":None,"volSize":None,"volType":None,"insId":None,"wasted-total":None,"Recomendation":'it has been detected that there are ebs volumes associated with instances that are stopped, as well as volumes that have not been used for a long time, both scenarios will add charges to our AWS account. Based on best practices, it is recommended that, if these volumes and the data stored within them are no longer needed, proceed to delete them.'}, ignore_index=True)
            makeTable(df,nameServ[i])
        if nameServ[i] == "rds-risk":
            df = pd.DataFrame(restData[nameServ[i]])
            df = df.append({"Account Name":None,"service":None,"idResource":None,"message":None,"risklevel":None,"region":None,"cost":None,"wasted-total":None,"Recomendation":'We have found RDS instances that have not received requests for a long time, and we have also seen instances that are oversized concerning our operations on them, i.e. their computing resources have not been used. Now, even if they are not being used, they continue to generate charges to our AWS bill, the recommendation is that if they are not needed it would be best to terminate the instances or move to a smaller size.'}, ignore_index=True)
            makeTable(df,nameServ[i])
        if nameServ[i] == "not-used-risk":
            df = pd.DataFrame(restData[nameServ[i]])
            df = df.append({"Account Name":None,"service":None,"idResource":None,"message":None,"risklevel":None,"region":None,"cost":None,"wasted-total":None,"Recomendation":'In this section we found several resources that are not being used and many of these are generating unnecessary charges to the AWS bill. It is advisable to check if they are not necessary and proceed to eliminate these resources. Having these resources that are not being used are considered bad configurations and represent a considerable risk to our infrastructure.'}, ignore_index=True)
            makeTable(df,nameServ[i])
        
        df = pd.DataFrame(restData[nameServ[i]])

        makeTable(df,nameServ[i])
        
    
    
def getAccounts(): # Funcion para obtener la informacion de las
    global accounts
    global contadordeplataquesegastaporrecursoquenoseliminamuchachoslimpienloqueusenydemenaccesoalacuentaporquemegaste33usdenlamia
    global accInfo # Lista para almacenar la informacion de las cuentas
    url = "https://conformity.us-1.cloudone.trendmicro.com/api/accounts" # URL para obtener la informacion de las cuentas
    response = requests.get(url, headers=headers) # Peticion
    accounts = response.json() # Respuesta en formato JSON
  
    for i in range (len(accounts["data"])): # Ciclo para obtener la informacion de cada cuenta
        try: 
            accIdForCost=accounts["data"][i]["id"]
            accName=accounts["data"][i]["attributes"]["name"]
            accIdCloud=accounts["data"][i]["attributes"]["awsaccount-id"]
            accEnviroment=accounts["data"][i]["attributes"]["environment"]
            accTags=accounts["data"][i]["attributes"]["tags"]
            accCloud_Type=accounts["data"][i]["attributes"]["cloud-type"]
            accNumResources=accounts["data"][i]["attributes"]["resources-count"]
            accTier=accounts["data"][i]["attributes"]["consumption-tier"]
            plata=getCost(accIdForCost,accIdCloud)
        
            accTemp={"id":accIdForCost,"name":accName,"idCloud":accIdCloud,"enviroment":accEnviroment,"tags":accTags,"cloudType":accCloud_Type,"numResources":accNumResources,"tier":accTier} # Crear un diccionario con la informacion de la cuenta
            accInfo.append(accTemp)
            print("Si se pudo obtener info de la cuenta: ",accName)
        except KeyError as e:
            print("No se pudo obtener la información de la cuenta '{}': {}".format(accName, str(e)))
    df=pd.DataFrame(accInfo) # Crear un dataframe con la informacion de las cuentas
    df = df.append({"id":None,"name":None,"enviroment":None,"tags":None,"cloudType":None,"numResources":None,"tier":None,"waste-total": contadordeplataquesegastaporrecursoquenoseliminamuchachoslimpienloqueusenydemenaccesoalacuentaporquemegaste33usdenlamia}, ignore_index=True)

    makeTable(df, "Accounts") # Llamar a la funcion para crear la tabla
    return accInfo # Retornar la informacion de las cuentas

def menu(): # Funcion para mostrar el menu
    os.system("cls") # Limpiar la consola
    print("Bienvenido a la herramienta de optimizacion de costos de Trend Micro Cloud One Conformity")
    print("1. Obtener informacion de cuentas y costos")
    print("2. Guardar excel")
    print("3. Salir")
    option=input("Por favor ingrese una opcion: ") # Ingresar una opcion
    if(option=="1"):
        getAccounts() # Llamar a la funcion para obtener la informacion de las cuentas
        input("Presione enter para continuar...") # Pausar la ejecucion del programa
        menu() # Llamar a la funcion para mostrar el menu
    elif(option=="2"):
        dfToSheet()
        
        saveFile()
        print("Archivo guardado con exito")
        print("Presione enter para continuar...")
        input()
        menu()
    elif(option=="3"):
        print("Gracias por usar la herramienta")
        exit()
    else:
        print("Opcion invalida, por favor ingrese una opcion valida")
        menu() 

def makeTable(nameTopic,namePage): # Funcion para crear una tabla con la informacion de las cuentas
   # Crear un archivo de excel
    nameTopic.to_excel(fileToSave, sheet_name=namePage, index=False ) # Guardar la informacion en el archivo de excel

def saveFile(): # Funcion para guardar el archivo de excel
    fileToSave.save() # Guardar el archivo de excel
menu() # Llamar a la funcion para mostrar el menu

