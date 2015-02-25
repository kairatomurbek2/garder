import pyodbc
import codecs
import json
import os
import shutil


DB_NAME = "Execution.mdb"
ACCESS_CON_STR = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s\\%s" % (os.getcwd(), DB_NAME)
BASE_TEMPLATE = '{"fields":%s,"model":%s,"pk":%s}'


def print_header(header):
        print "======== %s ========" % header


class Connector(object):
    def _connect(self):
        self.cnxn = pyodbc.connect(ACCESS_CON_STR)
        self.cursor = self.cnxn.cursor()

    def _disconnect(self):
        self.cursor.close()
        del self.cursor
        self.cnxn.close()

    def _execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
            if self.cursor.rowcount == 0:
                print
                print "===== WARNING ====="
                print "== 0 rows affected =="
                print sql
                print
        except Exception as e:
            print
            print "===== FAIL ====="
            print sql
            print
            print e
            print


class Preloader(Connector):    
    def preload(self):
        self._connect()
        self._preload_customers()
        self._preload_pws()
        self._preload_sites()
        self._preload_surveys()
        self._preload_hazards()
        self._preload_letters()
        self._disconnect()

    def _execute_list(self, sqls):
        for sql in sqls:
            self._execute(sql)

    def _preload_customers(self):
        print_header("PRELOADING CUSTOMERS")
        sqls = (
            "INSERT INTO ALL_CUSTOMERS ( CustomerName, AccountNumber, City, Code, Zip, Address1, Address2, State ) SELECT Services.CustomerName, Services.AccountNumber, Services.CustomerCity, Services.CustomerCode, Services.CustomerZip, Services.CustomerAddress1, Services.CustomerAddress2, Services.CustomerState FROM Services;",
            "UPDATE ALL_CUSTOMERS SET ALL_CUSTOMERS.Address1 = [ALL_CUSTOMERS].[Address2] WHERE (ALL_CUSTOMERS.Address1='' or Address1 is Null);",
            "UPDATE ALL_CUSTOMERS SET ALL_CUSTOMERS.Address2 = '' WHERE (ALL_CUSTOMERS.Address2=Address1);",
            "UPDATE ALL_CUSTOMERS SET ALL_CUSTOMERS.CustomerName = Replace(CustomerName,'\"','''') WHERE (((ALL_CUSTOMERS.CustomerName) Like '%\"%'));",
            "UPDATE ALL_CUSTOMERS SET ALL_CUSTOMERS.Address1 = Replace(Address1,'\\','/') WHERE (((ALL_CUSTOMERS.Address1) Like '%\\%'));",
            "UPDATE ALL_CUSTOMERS SET ALL_CUSTOMERS.CustomerName = Replace(CustomerName,'\\','/') WHERE (((ALL_CUSTOMERS.CustomerName) Like '%\\%'));",
            "UPDATE ALL_CUSTOMERS SET ALL_CUSTOMERS.Code = '200' WHERE (Code='13025');",
            "UPDATE ALL_CUSTOMERS SET ALL_CUSTOMERS.State = '227' WHERE ([ALL_CUSTOMERS].[State] is null);",
            "UPDATE ALL_CUSTOMERS, Pvals SET ALL_CUSTOMERS.Code = [Pvals].[Pval] WHERE ([Pvals].[Pval_ID]=Int([ALL_CUSTOMERS].[Code]));",
            "UPDATE ALL_CUSTOMERS, Pvals SET ALL_CUSTOMERS.State = [Pvals].[Pval] WHERE ([Pvals].[Pval_ID]=Int([ALL_CUSTOMERS].[State]));",
            "UPDATE ALL_CUSTOMERS SET ALL_CUSTOMERS.Address1 = 'No address available' WHERE (([Address1]='' Or [Address1] Is Null));",
            "UPDATE ALL_CUSTOMERS SET ALL_CUSTOMERS.Zip = '123456789' WHERE (([Zip]='' Or [Zip] Is Null));",
        )
        self._execute_list(sqls)
    
    def _preload_pws(self):
        print "======== PRELOADING PWS ========"
        sqls = (
            "INSERT INTO ALL_PWS ([Number], Name, WaterSource) SELECT PWS.PWSNumber, PWS.PWSName, PWS.WaterSource FROM PWS;",
            "UPDATE ALL_PWS, Pvals SET ALL_PWS.WaterSource = [Pval] WHERE (Int([WaterSource])=[Pval_ID]);",
        )
        self._execute_list(sqls)

    def _preload_sites(self):
        print "======== PRELOADING SITES ========"
        sqls = (
            "INSERT INTO ALL_SITES ( Customer, PWS, address1, address2, apt, city, state, zip, Route, site_use, site_type, floors, ic_point, meter_number, meter_size, meter_reading, potable, fire, irrigation, is_due_install, is_backflow ) SELECT ALL_CUSTOMERS.ID, ALL_PWS.ID, Services.ServiceStreetAddress, Services.ServiceStreetNumber, Services.SiteApt, Services.ServiceTown, Services.Service_State, Services.ServiceZip, Services.Route, Services.SiteUse, Services.SiteType, Services.NumberofFloors, Services.InterconnectionPoint, Services.MeterNumber, Services.MeterSize, Services.MeterReading, Services.PotablePresent, Services.FirePresent, Services.IrrigationPresent, Services.IsDueInstall, Services.IsBackflow FROM ALL_PWS INNER JOIN (ALL_CUSTOMERS INNER JOIN Services ON ALL_CUSTOMERS.AccountNumber = Services.AccountNumber) ON ALL_PWS.Number = Services.PWSID;",
            "UPDATE ALL_SITES, Pvals SET ALL_SITES.state = [Pval] WHERE (([Pval_ID]=Int([state])));",
            "UPDATE ALL_SITES, Pvals SET ALL_SITES.site_use = [Pval] WHERE (((Pvals.[Pval_ID])=Int([site_use])));",
            "UPDATE ALL_SITES, Pvals SET ALL_SITES.site_type = [Pval] WHERE (((Pvals.[Pval_ID])=Int([site_type])));",
            "UPDATE ALL_SITES, Pvals SET ALL_SITES.floors = [Pval] WHERE (((Pvals.[Pval_ID])=Int([ALL_SITES].[floors])));",
            "UPDATE ALL_SITES SET ALL_SITES.meter_number = 'N/M' WHERE (((ALL_SITES.meter_number)='N\\M'));",
            "UPDATE ALL_SITES SET ALL_SITES.meter_size = Replace([meter_size],'\"','''''') WHERE (((ALL_SITES.meter_size) Like '%\"%'));",
            "UPDATE ALL_SITES SET ALL_SITES.city = 'LA PLACE' WHERE ((ALL_SITES.city is null or ALL_SITES.city=''));",
        )
        self._execute_list(sqls)

    def _preload_surveys(self):
        print "======== PRELOADING SURVEYS ========"
        sqls = (
            "INSERT INTO ALL_SURVEYS ( site, service_type, Surveyor, survey_date, Metered, pump_present, additives_present, cc_present, Protected, aux_water, detector_manufacturer, detector_model, detector_serial, Notes, Special, old_id ) SELECT ALL_SITES.ID, Surveys.Type, LCase([Surveyor]) AS LS, Surveys.SurveyDate, IIf(LCase([Metered])='yes',-1,0) AS mtr, IIf(LCase([PumpPresent])='yes',-1,0) AS pmp, IIf(LCase([Additives])='yes',-1,0) AS adt, IIf(LCase([CCPresent])='yes',-1,0) AS ccp, IIf(LCase([Protected])='yes',-1,0) AS prt, IIf(LCase([AuxWater])='yes',-1,0) AS auw, Surveys.DetectorManufacturer, Surveys.DetectorModelNo, Surveys.DetectorSerialNo, Surveys.Notes, Surveys.Special, Surveys.SurveyID FROM ALL_CUSTOMERS, Surveys, ALL_SITES WHERE ((Int([Customer])=[ALL_CUSTOMERS].[ID] And [ALL_CUSTOMERS].[AccountNumber]=[Surveys].[AccountNumber]));",
            "UPDATE ALL_SURVEYS, Pvals SET ALL_SURVEYS.service_type = [Pval] WHERE (((Pvals.[Pval_ID])=Int([service_type])));",
            "UPDATE ALL_SURVEYS, Pvals SET ALL_SURVEYS.detector_manufacturer = [Pval] WHERE (((Pvals.[Pval_ID])=Int([detector_manufacturer])));",
            "UPDATE ALL_SURVEYS, Pvals SET ALL_SURVEYS.special = [Pval] WHERE (((Pvals.[Pval_ID])=Int([special])));",
            "UPDATE ALL_SURVEYS SET ALL_SURVEYS.notes = Replace([ALL_SURVEYS].[notes],(Chr(13) & Chr(10)),' ') WHERE (((ALL_SURVEYS.notes) Like ('%' & Chr(13) & Chr(10) & '%')));",
            "UPDATE ALL_SURVEYS SET ALL_SURVEYS.notes = Replace([ALL_SURVEYS].[notes],'\"','''''') WHERE (((ALL_SURVEYS.notes) Like ('%\"%')));",
        )
        self._execute_list(sqls)

    def _preload_hazards(self):
        print "======== PRELOADING HAZARDS ========"
        sqls = (
            "INSERT INTO ALL_HAZARDS ( hazard_type, assembly_status, bp_type_required, due_install_test_date, survey ) SELECT Surveys.Hazard1, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, ALL_SURVEYS.ID FROM Surveys, ALL_SURVEYS WHERE ((Int([ALL_SURVEYS].[old_id])=[Surveys].[SurveyID]));",
            "UPDATE BackflowDevices, ALL_SURVEYS, ALL_HAZARDS SET ALL_HAZARDS.assembly_location = [BackflowDevices].[AssemblyLocation], ALL_HAZARDS.installed_properly = [BackflowDevices].[InstalledProperly], ALL_HAZARDS.installer = [BackflowDevices].[Installer], ALL_HAZARDS.install_date = [BackflowDevices].[InstallDate], ALL_HAZARDS.replace_date = [BackflowDevices].[ReplaceDate], ALL_HAZARDS.orientation = [BackflowDevices].[Orientation], ALL_HAZARDS.bp_type_present = [BackflowDevices].[TypeBPProvided], ALL_HAZARDS.bp_size = [BackflowDevices].[BPSize], ALL_HAZARDS.bp_manufacturer = [BackflowDevices].[Manufacturer], ALL_HAZARDS.model_no = [BackflowDevices].[ModelNo], ALL_HAZARDS.serial_no = [BackflowDevices].[SerialNo] WHERE (((BackflowDevices.SurveyID)=Int([ALL_SURVEYS].[old_id])) AND ((ALL_SURVEYS.ID)=Int([ALL_HAZARDS].[survey])));",
            "INSERT INTO ALL_HAZARDS ( hazard_type, assembly_status, bp_type_required, due_install_test_date, survey ) SELECT Surveys.Hazard2, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, ALL_SURVEYS.ID FROM Surveys, ALL_SURVEYS WHERE (([Hazard2] Is Not Null) AND ((Int([ALL_SURVEYS].[old_id]))=[Surveys].[SurveyID]));",
            "INSERT INTO ALL_HAZARDS ( hazard_type, assembly_status, bp_type_required, due_install_test_date, survey ) SELECT Surveys.Hazard3, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, ALL_SURVEYS.ID FROM Surveys, ALL_SURVEYS WHERE (([Hazard3] Is Not Null) AND ((Int([ALL_SURVEYS].[old_id]))=[Surveys].[SurveyID]));",
            "INSERT INTO ALL_HAZARDS ( hazard_type, assembly_status, bp_type_required, due_install_test_date, survey ) SELECT Surveys.Hazard4, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, ALL_SURVEYS.ID FROM Surveys, ALL_SURVEYS WHERE (([Hazard4] Is Not Null) AND ((Int([ALL_SURVEYS].[old_id]))=[Surveys].[SurveyID]));",
            "INSERT INTO ALL_HAZARDS ( hazard_type, assembly_status, bp_type_required, due_install_test_date, survey ) SELECT Surveys.Hazard5, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, ALL_SURVEYS.ID FROM Surveys, ALL_SURVEYS WHERE (([Hazard5] Is Not Null) AND ((Int([ALL_SURVEYS].[old_id]))=[Surveys].[SurveyID]));",
            "UPDATE ALL_HAZARDS, Pvals, hazardreassignment SET ALL_HAZARDS.hazard_type = [hazardreassignment].[Point to] WHERE (((Int([hazard_type]))=[hazardreassignment].[Pval_ID] And [hazardreassignment].[Point to] Is Not Null));",
            "INSERT INTO Pvals ( Pval, Field, [User], [Last Update], ActivityStatus ) SELECT hazarddelete.Pval, 'Hazard_Type' AS Expr1, 'MegaUser' AS Expr2, #1/1/2010# AS Expr4, -1 AS Expr3 FROM hazarddelete WHERE (((hazarddelete.Delete)='y'));",
            "UPDATE Pvals SET Pvals.Pval = 'Landscape Nursery' WHERE (((Pvals.Pval) Like 'Landscape Nursery%'));",
            "UPDATE ALL_HAZARDS, hazarddelete, Pvals SET ALL_HAZARDS.hazard_type = [Pvals].[Pval_ID] WHERE ((int(ALL_HAZARDS.hazard_type)=[hazarddelete].[Pval_ID] And [Pvals].[Pval]=[hazarddelete].[Pval] And [hazarddelete].[Delete]='y'));",
            "UPDATE ALL_HAZARDS, Pvals SET ALL_HAZARDS.hazard_type = [Pvals].[Pval] WHERE ((Int([hazard_type])=[Pvals].[Pval_ID]));",
            "UPDATE ALL_HAZARDS, Pvals SET ALL_HAZARDS.assembly_location = [Pvals].[Pval] WHERE (((Int([assembly_location]))=[Pvals].[Pval_ID]));",
            "UPDATE ALL_HAZARDS, Pvals SET ALL_HAZARDS.bp_type_present = [Pvals].[Pval] WHERE (((Int([bp_type_present]))=[Pvals].[Pval_ID]));",
            "UPDATE ALL_HAZARDS, Pvals SET ALL_HAZARDS.bp_type_required = [Pvals].[Pval] WHERE (((Int([bp_type_required]))=[Pvals].[Pval_ID]));",
            "UPDATE ALL_HAZARDS, Pvals SET ALL_HAZARDS.bp_size = [Pvals].[Pval] WHERE (((Int([bp_size]))=[Pvals].[Pval_ID]));",
            "UPDATE ALL_HAZARDS, Pvals SET ALL_HAZARDS.bp_manufacturer = [Pvals].[Pval] WHERE (((Int([bp_manufacturer]))=[Pvals].[Pval_ID]));",
        )
        self._execute_list(sqls)

    def _preload_letters(self):
        print "======== PRELOADING LETTERS ========"
        sqls = (
            "INSERT INTO ALL_LETTERS ( LetterDate, Customer ) SELECT Letters.LetterDate, ALL_CUSTOMERS.ID FROM ALL_CUSTOMERS, Letters WHERE (((Letters.AccountNumber)=[ALL_CUSTOMERS].[AccountNumber]));",
        )
        self._execute_list(sqls)


class Formatter(Connector):
    CREATE_TABLE_PATTERN = "create table %s (ID autoincrement(1, 1) constraint %s_pk primary key, %s);"
    FIELD_PATTERN = "[%s] %s %s"
    TABLES = {
        "customers": ("ALL_CUSTOMERS", ["CustomerName", "AccountNumber", "City", "Code", "Zip", "Address1", "Address2", "State"]),
        "sites": ("ALL_SITES", ["Customer", "PWS", ("connect_date", "date"), "address1", "address2", "apt", "city", "state", "zip", "site_use", "site_type", "floors", "ic_point", ("potable", "yesno"), ("fire", "yesno"), ("irrigation", "yesno"), ("is_due_install", "yesno"), ("is_backflow", "yesno"), "route", "meter_number", "meter_size", "meter_reading"]),
        "pws": ("ALL_PWS", ["Number", "Name", "City", "WaterSource"]),
        "letters": ("ALL_LETTERS", ["Customer", ("LetterDate", "date")]),
        "surveys": ("ALL_SURVEYS", ["site", "service_type", ("survey_date", "date"), "survey_type", "surveyor", ("metered", "yesno"), ("pump_present", "yesno"), ("additives_present", "yesno"), ("cc_present", "yesno"), ("protected", "yesno"), ("aux_water", "yesno"), "detector_manufacturer", "detector_model", "special", "detector_serial", "notes", "old_id"]),
        "hazards": ("ALL_HAZARDS", ["survey", "location1", "location2", "hazard_type", "assembly_location", "assembly_status", ("installed_properly", "yesno"), "installer", ("install_date", "date"), ("replace_date", "date"), "orientation", "bp_type_present", "bp_type_required", "bp_size", "bp_manufacturer", "model_no", "serial_no", ("due_install_test_date", "date")])
    }

    def _create_database(self):
        print "======== CREATING DATABASE ========"
        self._discard_database()
        shutil.copy("BPS_L.mdb", DB_NAME)

    def _discard_database(self):
        try:
            shutil.copy(DB_NAME, "prev_%s" % DB_NAME)
        except:
            pass

    def _create_tables(self):
        print "======== CREATING TABLES ========"
        for table in self.TABLES.values():
            sql = self.CREATE_TABLE_PATTERN % (table[0], table[0], self._format_fields(table[1]))
            self._execute(sql)
        
    def _format_fields(self, field_list):
        formatted_field_list = []
        for field in field_list:
            if isinstance(field, tuple):
                if field[1] == "bool":
                    formatted_field_list.append(self.FIELD_PATTERN % (field[0], field[1], ""))
                else:
                    formatted_field_list.append(self.FIELD_PATTERN % (field[0], field[1], "null"))
            else:
                formatted_field_list.append(self.FIELD_PATTERN % (field, "varchar", "null"))
        return ', '.join(formatted_field_list)

    def _preload(self):
        preloader = Preloader()
        preloader.preload()

    def prepare_db(self):
        self._create_database()
        self._connect()
        self._create_tables()
        self._disconnect()
        self._preload()


class Jsoner(object):    
    def __init__(self):
        self.models = {
            "webapp.sourcetype": {},
            "webapp.sitetype": {},
            "webapp.siteuse": {},
            "webapp.servicetype": {},
            "webapp.surveytype": {},
            "webapp.bptype": {},
            "webapp.bpsize": {},
            "webapp.bpmanufacturer": {},
            "webapp.customercode": {},
            "webapp.hazardtype": {},
            "webapp.testmanufacturer": {},
            "webapp.icpointtype": {},
            "webapp.assemblylocation": {},
            "webapp.assemblystatus": {
                "Installed": 1,
                "Replaced": 2,
                "Due Install": 3,
                "Due Replace": 4,
                "Not Required": 5        
            },
            "webapp.lettertype": {},
            "webapp.floorscount": {},
            "webapp.special": {},
            "webapp.orientation": {},
            "auth.user": {
                "mlebas": 2,
                "jlebas": 3,
                "knijoka": 4,
                "jjdahl": 5,
                "ndecoteau": 6,
                "dvillien": 7,
                "rleblanc": 8
            }
        }
        self.fill_json()
        self.print_json()
    
    def fill_json(self):
        f = open("ddata.json")
        json_data = json.loads(f.read())
        for json_object in json_data:
            self.models[json_object["model"]][json_object["fields"].values()[0]] = json_object["pk"]
        for model in self.models:
            self.models[model][""] = "null"
        f.close()

    def print_json(self):
        print json.dumps(self.models, indent=4, separators=(',', ': '))


class Dumper(Connector):
    TEMPLATES = {
        'site': BASE_TEMPLATE % ('{"status":1,"customer":%s,"pws":%s,"connect_date":null,"address1":"%s","address2":"","apt":"%s","city":"%s","state":"%s","zip":"%s","site_use":%s,"site_type":%s,"floors":%s,"interconnection_point":%s,"meter_number":"%s","meter_size":"%s","meter_reading":%s,"route":"%s","potable_present":%s,"fire_present":%s,"irrigation_present":%s,"is_due_install":%s,"is_backflow":%s,"next_survey_date":null,"notes":""}', '"webapp.site"', '%s'),
        'customer': BASE_TEMPLATE % ('{"number":"%s","name":"%s","code":%s,"address1":"%s","address2":"%s","city":"%s","state":"%s","zip":"%s","phone":"","fax":"","email":"","notes":""}', '"webapp.customer"', '%s'),
        'survey': BASE_TEMPLATE % ('{"site":%s,"service_type":%s,"survey_date":"%s","survey_type":null,"surveyor":%s,"metered":%s,"pump_present":%s,"additives_present":%s,"cc_present":%s,"protected":%s,"aux_water":%s,"detector_manufacturer":"%s","detector_model":"%s","detector_serial_no":"%s","special":%s,"notes":"%s"}', '"webapp.survey"', '%s'),
        'hazard': BASE_TEMPLATE % ('{"survey":%s,"location1":"","location2":"","hazard_type":%s,"assembly_location":%s,"assembly_status":%s,"installed_properly":%s,"installer":null,"install_date":null,"replace_date":null,"orientation":%s,"bp_type_present":%s,"bp_type_required":%s,"bp_size":%s,"manufacturer":%s,"model_no":"%s","serial_no":"%s","due_install_test_date":null,"notes":""}', '"webapp.hazard"', '%s'),
        'pws': BASE_TEMPLATE % ('{"number":"%s","name":"%s","city":"","water_source":%s,"notes":""}', '"webapp.pws"', '%s'),
        'letter': BASE_TEMPLATE % ('{"customer":%s,"survey":null,"letter_type":1,"date":"%s","user":2}', '"webapp.letter"', '%s'),
    }
    SQL_STRS = {
        'dump_sites':'select Customer, PWS, address1, apt, city, state, zip, site_use, site_type, floors, ic_point, meter_number, meter_size, meter_reading, route, potable, fire, irrigation, is_due_install, is_backflow, ID from ALL_SITES',
        'dump_customers':'select AccountNumber, CustomerName, Code, Address1, Address2, City, State, Zip, ID from ALL_CUSTOMERS',
        'dump_surveys':'select site, service_type, survey_date, surveyor, metered, pump_present, additives_present, cc_present, protected, aux_water, detector_manufacturer, detector_model, detector_serial, special, notes, ID from ALL_SURVEYS',
        'dump_pwss':'select Number, Name, WaterSource, ID from ALL_PWS',
        'dump_hazards':'select survey, hazard_type, assembly_location, assembly_status, installed_properly, orientation, bp_type_present, bp_type_required, bp_size, bp_manufacturer, model_no, serial_no, ID from ALL_HAZARDS',
        'dump_letters':'select customer, letterdate, ID from ALL_LETTERS',
    }
    DATA_TYPES = [
        'customer',
        'pws',
        'site',
        'survey',
        'hazard',
        'letter'
    ]
    FIELDS_TO_REPLACE = {
        'site': [(7, "webapp.siteuse"),
                 (8, "webapp.sitetype"),
                 (9, "webapp.floorscount"),
                 (10, "webapp.icpointtype")],
        'customer': [(2, "webapp.customercode"),],
        'survey': [(1, "webapp.servicetype"),
                   (3, "auth.user"),
                   (13, "webapp.special")],
        'hazard': [(1, "webapp.hazardtype"),
                   (2, "webapp.assemblylocation"),
                   (3, "webapp.assemblystatus"),
                   (5, "webapp.orientation"),
                   (6, "webapp.bptype"),
                   (7, "webapp.bptype"),
                   (8, "webapp.bpsize"),
                   (9, "webapp.bpmanufacturer")],
        'pws': [(2, "webapp.sourcetype"),],
        'letter': []
    }
        
    def __init__(self):
        formatter = Formatter()
        formatter.prepare_db()
        self.jsoner = Jsoner()
        self._connect()

    def dump(self):
        full = codecs.open("data_full.json", 'w', 'utf-8')
        full.write('[')
        for data_type in self.DATA_TYPES:
            f = codecs.open("data_%s.json" % data_type, 'w', 'utf-8')
            f.write('[')
            print "=== Starting %s dump ===" % data_type
            try:
                sql_str = self.SQL_STRS["dump_%ss" % data_type]
                template = self.TEMPLATES[data_type]
                self.cursor.execute(sql_str)
                row = self.cursor.fetchone()
                data = self.replace_nones(template % tuple(self.replace_fields(row, data_type)))
                f.write('\n' + data)
                if data_type == 'customer':
                    full.write('\n' + data)
                else:
                    full.write(',\n' + data)
                row = self.cursor.fetchone()
                while row:
                    data = self.replace_nones(template % tuple(self.replace_fields(row, data_type)))
                    f.write(',\n'+data)
                    full.write(',\n'+data)
                    row = self.cursor.fetchone()
            except Exception as e:
                print row
                print
                print e
                print
            f.write(']')
            f.close()
            print "=== Finished %s dump ===" % data_type
        full.write(']')
        full.close()
        self._disconnect()

    def replace_nones(self, string):
        return string.replace("None", "null").replace("False", "false").replace("True", "true").replace('"null"', 'null')

    def replace_fields(self, row, data_type):
        for index, model in self.FIELDS_TO_REPLACE[data_type]:
            if row[index]:
                row[index] = self.jsoner.models[model][row[index]]
            else:
                row[index] = "null"
        #replace letter date, remove time part
        if data_type == "letter" and row[1]:
            row[1] = ('%s' % row[1])[:10]
        #and for survey
        if data_type == "survey" and row[2]:
            row[2] = ('%s' % row[2])[:10]
        #and replacing blank values on site.meter_reading with Nulls
        if data_type == "site" and row[13]=="":
            row[13] = ('null')
        return row


dumper = Dumper()
dumper.dump()
