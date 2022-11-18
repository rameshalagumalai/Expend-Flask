conn = None
import ibm_db

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt;UID=ghc72736;PWD=cTnreyg6kRM90ju9",'','')
    print("Connected to database")
except:
    print("Unable to connect", ibm_db.conn_errormsg())


