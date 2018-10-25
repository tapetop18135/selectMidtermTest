from spyne import Iterable, Integer, Unicode, rpc, Application, ServiceBase, Array, TTableModel, Integer32, String, ComplexModel, Float, xml
from spyne.protocol.soap import Soap11

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

import dicttoxml
import datetime 

from lxml import etree
import xmlschema

# Generate a ComplexModelBase subclass with
# metadata information
# Initialize SQLAlchemy Environment
engine = create_engine('sqlite:///./air.db')

# class TempValue(ComplexModel):
#     __namespace__ = "TempValue"
#     key = Integer()
#     lat = Float()
#     sst = Float()
#     date_use = String()

# def mapArray(Array_t):
#     temp = []
#     for i in Array_t:
#         temp.append(TempValue(key=i[0], lat=i[1], sst=i[2], date_use=i[3],))

#     return temp

class AirTempService(ServiceBase):

    @rpc(String, Float, Float, _returns=String)
    def setTempData(ctx, room_id, tempV, humidV):
        Tnow = datetime.datetime.now()
        result = engine.execute('insert into tempTB values ("'+room_id+'",'+str(tempV)+','+str(humidV)+',"'+str(Tnow)+'")')
        result_ = "Success"
        
        return result_

    @rpc(String ,_returns=String)
    def getTempData(ctx, text):

        if(text == "get_temp"):
            results = engine.execute('select * from tempTB')
            dictTemp = []
            for r in results:
                tempData={}
                tempData['room_id'] = r[0]
                tempData['temp'] = r[1]
                tempData['humid'] = r[2]
                tempData['date'] = r[3]
            
                dictTemp.append(tempData)
            
            xml = dicttoxml.dicttoxml(dictTemp)
            # print(xml)
        else:
            xml = "Error"
            
        return xml

    
    @rpc(String ,_returns=String)
    def getInformation(ctx, text):

        if(text == "get_information"):
            results = engine.execute('select * from information')
            # print(results)
            dictTemp = []
            for r in results:
                # print(r)
                tempData={}
                tempData['id'] = r[0]
                tempData['name'] = r[1]
                tempData['hobby'] = r[2]
            
                dictTemp.append(tempData)
            xml = dicttoxml.dicttoxml(dictTemp)
            
            my_schema = xmlschema.XMLSchema('./data/xsd/information.xsd')
            root = etree.XML(xml)
            if(my_schema.is_valid(root)):
                result = xml
            else:
                result = """<Error>Error NOT Valid</Error>"""

        else:
            result = "Error"
            
        return result

def create_app(flask_app):
    """Creates SOAP services application and distribute Flask config into
    user con defined context for each method call.
    """
    application = Application([AirTempService], 'spyne.examples.flask',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11()
        # out_protocol=Soap11(),
    )

    return application