# Used for dumping from MS Access database
# Works only under Windows as requires pyodbc
# Tuned on BFP database, so will not work for another one
# Jsoner loads pre-saved dictionary data from file
# Jsoner is required to replace actual data with foreign keys

import pyodbc
import codecs
import json


ACCESS_CON_STR = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=d:\\mitch\\Execution.mdb"
BASE_TEMPLATE = '{"fields":%s,"model":%s,"pk":%s}'
TEMPLATES = {
    'site': BASE_TEMPLATE % ('{"customer":%s,"pws":%s,"connect_date":null,"address1":"%s","address2":"","apt":"%s","city":"%s","state":"%s","zip":"%s","site_use":%s,"site_type":%s,"floors":%s,"interconnection_point":%s,"meter_number":"%s","meter_size":"%s","meter_reading":%s,"route":"%s","potable_present":%s,"fire_present":%s,"irrigation_present":%s,"is_due_install":%s,"is_backflow":%s,"next_survey_date":null,"notes":""}', '"webapp.site"', '%s'),
    'customer': BASE_TEMPLATE % ('{"number":"%s","name":"%s","code":%s,"address1":"%s","address2":"%s","city":"%s","state":"%s","zip":"%s","phone":"","notes":""}', '"webapp.customer"', '%s'),
    'survey': BASE_TEMPLATE % ('{"site":%s,"service_type":%s,"survey_date":"%s","survey_type":null,"surveyor":%s,"metered":%s,"pump_present":%s,"additives_present":%s,"cc_present":%s,"protected":%s,"aux_water":%s,"detector_manufacturer":"%s","detector_model":"%s","detector_serial_no":"%s","special":%s,"notes":"%s"}', '"webapp.survey"', '%s'),
    'hazard': BASE_TEMPLATE % ('{"survey":%s,"location1":"","location2":"","hazard_type":%s,"assembly_location":%s,"assembly_status":%s,"installed_properly":%s,"installer":null,"install_date":null,"replace_date":null,"orientation":%s,"bp_type_present":%s,"bp_type_required":%s,"bp_size":%s,"manufacturer":%s,"model_no":"%s","serial_no":"%s","due_install_test_date":%s,"notes":""}', '"webapp.hazard"', '%s'),
    'pws': BASE_TEMPLATE % ('{"number":"%s","name":"%s","city":"","water_source":%s,"notes":""}', '"webapp.pws"', '%s'),
    'letter': BASE_TEMPLATE % ('{"customer":%s,"survey":null,"letter_type":1,"date":"%s","user":2}', '"webapp.letter"', '%s'),
}
SQL_STRS = {
    'dump_sites':'select Customer, PWS, address1, apt, city, state, zip, site_use, site_type, floors, ic_point, meter_number, meter_size, meter_reading, route, potable, fire, irrigation, is_due_install, is_backflow, ID from ALL_SITES',
    'dump_customers':'select AccountNumber, CustomerName, Code, Address1, Address2, City, State, Zip, ID from ALL_CUSTOMERS',
    'dump_surveys':'select site, service_type, survey_date, surveyor, metered, pump_present, additives_present, cc_present, protected, aux_water, detector_manufacturer, detector_model, detector_serial, special, notes, ID from ALL_SURVEYS',
    'dump_pwss':'select Number, Name, WaterSource, ID from ALL_PWS',
    'dump_hazards':'select survey, hazard_type, assembly_location, assembly_status, installed_properly, orientation, bp_type_present, bp_type_required, bp_size, bp_manufacturer, model_no, serial_no, due_install_test_date, ID from ALL_HAZARDS',
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


class Jsoner(object):
    source_type = {}
    site_type = {}
    site_use = {}
    service_type = {}
    survey_type = {}
    bp_type = {}
    bp_size = {}
    bp_manufacturer = {}
    customer_code = {}
    hazard_type = {}
    test_manufacturer = {}
    ic_point_type = {}
    assembly_location = {}
    letter_type = {}
    floors_count = {}
    special = {}
    orientation = {}
    assembly_status = {
        "Installed": 1,
        "Replaced": 2,
        "Due Install": 3,
        "Due Replace": 4,
        "Not Required": 5        
    }
    surveyors = {
        "MLeBas": 2,
        "mlebas": 2,
        "JLeBas": 3,
        "jlebas": 3,
        "knijoka": 4,
        "KNijoka": 4,
        "Knijoka": 4,
        "jjdahl": 5,
        "ndecoteau": 6,
        "dvillien": 7,
        "rleblanc": 8
    }
    models = {}

    def __init__(self):
        self.models = {
            "webapp.sourcetype": self.source_type,
            "webapp.sitetype": self.site_type,
            "webapp.siteuse": self.site_use,
            "webapp.servicetype": self.service_type,
            "webapp.surveytype": self.survey_type,
            "webapp.bptype": self.bp_type,
            "webapp.bpsize": self.bp_size,
            "webapp.bpmanufacturer": self.bp_manufacturer,
            "webapp.customercode": self.customer_code,
            "webapp.hazardtype": self.hazard_type,
            "webapp.testmanufacturer" : self.test_manufacturer,
            "webapp.icpointtype": self.ic_point_type,
            "webapp.assemblylocation" : self.assembly_location,
            "webapp.assemblystatus": self.assembly_status,
            "webapp.lettertype": self.letter_type,
            "webapp.floorscount": self.floors_count,
            "webapp.special": self.special,
            "webapp.orientation": self.orientation,
            "auth.user": self.surveyors,
        }
        self.fill_json()
        self.print_json()
    
    def fill_json(self):
        f = open("dict_data.json")
        json_data = json.loads(f.read())
        for json_object in json_data:
            self.models[json_object["model"]][json_object["fields"].values()[0]] = json_object["pk"]
        for model in self.models:
            self.models[model][""] = "null"
        f.close()

    def print_json(self):
        print json.dumps(self.models, indent=4, separators=(',', ': '))


class Dumper(object):
    cnxn = pyodbc.connect(ACCESS_CON_STR)
    cursor = cnxn.cursor()
    jsoner = Jsoner()
    f = codecs.open("data.json", 'w', "utf-8")

    def dump(self):
        self.f.write('[')
        for data_type in DATA_TYPES:
            print "Starting %s dump" % data_type 
            sql_str = SQL_STRS["dump_%ss" % data_type]
            template = TEMPLATES[data_type]
            self.cursor.execute(sql_str)
            row = self.cursor.fetchone()
            while row:
                data = self.replace_nones(template % tuple(self.replace_fields(row, data_type)))
                self.f.write(',\n'+data)
                row = self.cursor.fetchone()
            print "Finished %s dump" % data_type
        self.f.write(']')
        self.f.close()        

    def replace_nones(self, string):
        return string.replace("None", "null").replace("False", "false").replace("True", "true")

    def replace_fields(self, row, data_type):
        for index, model in FIELDS_TO_REPLACE[data_type]:
            if row[index]:
                row[index] = self.jsoner.models[model][row[index]]
            else:
                row[index] = "null"
        if data_type == "hazard":
            if row[12]:
                row[12] = '"%s"' % row[12]
            else:
                row[12] = "null"
        return row


if __name__ == '__main__':
    dumper = Dumper()
    dumper.dump()
