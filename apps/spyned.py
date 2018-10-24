from spyne import Iterable, Integer, Unicode, rpc, Application, ServiceBase, Array, TTableModel, Integer32, String, ComplexModel, Float, xml
from spyne.protocol.soap import Soap11

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

import dicttoxml
import datetime 

# Generate a ComplexModelBase subclass with
# metadata information
# Initialize SQLAlchemy Environment
engine = create_engine('sqlite:///./air.db')

class TempValue(ComplexModel):
    __namespace__ = "TempValue"
    key = Integer()
    lat = Float()
    sst = Float()
    date_use = String()

def mapArray(Array_t):
    temp = []
    for i in Array_t:
        temp.append(TempValue(key=i[0], lat=i[1], sst=i[2], date_use=i[3],))

    return temp

class AirTempService(ServiceBase):

    @rpc(String, String,_returns=String)
    def setTempData(ctx, room_id, tempV):
        Tnow = datetime.datetime.now()
        print(room_id, tempV)
        result = engine.execute('insert into tempTB values ("'+room_id+'","'+tempV+'","'+str(Tnow)+'")')
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
                tempData['date'] = r[2]
            
                dictTemp.append(tempData)
            
            xml = dicttoxml.dicttoxml(dictTemp)
        else:
            xml = "Error"
            
        return xml


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