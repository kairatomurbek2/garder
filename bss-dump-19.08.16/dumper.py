import pyodbc
import codecs
import json
import os
import shutil
from time import sleep


DB_NAME = "Execution.mdb"
ACCESS_CON_STR = r"""
DRIVER={SQL Server Native Client 10.0};
SERVER=.;
DATABASE=BSS110816;
UID=root;
PWD=root;
"""
BASE_TEMPLATE = '{"fields":%s,"model":%s,"pk":%s}'


def print_header(header):
    print "======== %s ========" % header


class Connector(object):
    def _connect(self):
        self.cnxn = pyodbc.connect(ACCESS_CON_STR)
        self.cursor = self.cnxn.cursor()

    def _connect_another(self):
        # required for dumping hazards for surveys (many-to-many relation)
        self.cnxn2 = pyodbc.connect(ACCESS_CON_STR)
        self.cursor2 = self.cnxn2.cursor()

    def _disconnect(self):
        self.cursor.close()
        del self.cursor
        self.cnxn.close()

    def _disconnect_another(self):
        self.cursor2.close()
        del self.cursor2
        self.cnxn2.close()

    def _execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
            print
            if self.cursor.rowcount == 0:
                print "===== WARNING ====="
                print "0 rows affected"
                print
                print sql
                sleep(5)
            else:
                print "===== SUCCESS ====="
                print sql
            print "== %s rows affected ==" % self.cursor.rowcount
            print
        except Exception as e:
            print
            print "===== FAIL ====="
            print sql
            print
            print e
            print
            sleep(30)

    def _execute_with_parameter(self, sql, parameter):
        pass


class Preloader(Connector):
    def preload(self):
        self._connect()
        self._preload_pws()
        self._preload_sites()
        self._preload_surveys()
        self._preload_hazards()
        self._preload_devices()
        self._preload_letters()
        self._preload_tests()
        self._preload_test_kits()
        self._preload_tester_certs()
        self._disconnect()

    def _execute_list(self, sqls):
        for sql in sqls:
            self._execute(sql)

    def _preload_pws(self):
        print "======== PRELOADING PWS ========"
        sqls = (
            "INSERT INTO ALL_PWS ([Number], Name, WaterSource) SELECT PWS.PWSNumber, PWS.PWSName, PWS.WaterSource FROM PWS;",
            "UPDATE ALL_PWS SET ALL_PWS.WaterSource = (Select Pval from Pvals WHERE ([WaterSource]=[Pval_ID]));",
        )
        self._execute_list(sqls)

    def _preload_sites(self):
        print "======== PRELOADING SITES ========"
        sqls = (
            "update [Services] set PWSID = 'LA1095003' where PWSID = '26';",
            """INSERT INTO ALL_SITES ( PWS, address1, address2, street_number, apt, city, state, zip,
                Route, site_use, site_type, floors, ic_point, meter_number, meter_size, meter_reading,
                potable, fire, irrigation, is_due_install, is_backflow,
                CustomerName, AccountNumber, CustCity, Code, CustZip,
                CustAddress1, CustAddress2, CustApt, CustState,
                LastSurveyDate, NextSurveyDate, connect_date)
            SELECT ALL_PWS.ID, Services.ServiceStreetAddress, Services.ServiceAddress2, Services.ServiceStreetNumber, Services.SiteApt,
                Services.ServiceTown, Services.Service_State, Services.ServiceZip,
                Services.Route, Services.SiteUse, Services.SiteType, Services.NumberofFloors,
                Services.InterconnectionPoint, Services.MeterNumber, Services.MeterSize, Services.MeterReading,
                Services.PotablePresent, Services.FirePresent, Services.IrrigationPresent,
                Services.IsDueInstall, Services.IsBackflow,
                Services.CustomerName, Services.AccountNumber, Services.CustomerCity,
                Services.CustomerCode, Services.CustomerZip, Services.CustomerAddress1, Services.CustomerAddress2, Services.CustApt,
                Services.CustomerState, Services.LastSurveyDate, Services.NextSurveyDate, Services.ConnectDate
            FROM ALL_PWS INNER JOIN Services ON ALL_PWS.Number = Services.PWSID;""",
            """UPDATE ALL_SITES 
SET [state] = (Select Pval from Pvals WHERE ([Pval_ID]=[state])),
    site_use = (Select Pval from Pvals WHERE ([Pval_ID]=[site_use])),
    site_type = (Select Pval from Pvals WHERE ([Pval_ID]=[site_type])),
    floors = (Select Pval from Pvals WHERE ([Pval_ID]=[floors]));""",
            "UPDATE ALL_SITES SET ALL_SITES.meter_number = 'N/M' WHERE (((ALL_SITES.meter_number)='N\\M'));",
            "UPDATE ALL_SITES SET ALL_SITES.meter_size = Replace([meter_size],'\"','\\\"') WHERE (((ALL_SITES.meter_size) Like '%\"%'));",
            "UPDATE ALL_SITES SET ALL_SITES.city = 'Unknown' WHERE ((ALL_SITES.city is null or ALL_SITES.city=''));",
            "UPDATE ALL_SITES SET ALL_SITES.CustAddress1 = [ALL_SITES].[CustAddress2] WHERE (ALL_SITES.CustAddress1='' or CustAddress1 is Null);",
            "UPDATE ALL_SITES SET ALL_SITES.CustAddress2 = '' WHERE (ALL_SITES.CustAddress2=CustAddress1);",
            "UPDATE ALL_SITES SET ALL_SITES.address1 = [ALL_SITES].[address2] WHERE (ALL_SITES.address1='' or address1 is Null);",
            "UPDATE ALL_SITES SET ALL_SITES.address2 = '' WHERE (ALL_SITES.address2=address1);",
            "UPDATE ALL_SITES SET ALL_SITES.CustomerName = Replace(CustomerName,'\\','/') WHERE (((ALL_SITES.CustomerName) Like '%\\%'));",
            "UPDATE ALL_SITES SET ALL_SITES.CustomerName = Replace(CustomerName,'\"','\\\"') WHERE (((ALL_SITES.CustomerName) Like '%\"%'));",
            "UPDATE ALL_SITES SET ALL_SITES.CustAddress1 = Replace(CustAddress1,'\\','/') WHERE (((ALL_SITES.CustAddress1) Like '%\\%'));",
            "UPDATE ALL_SITES SET ALL_SITES.CustAddress1 = Replace(CustAddress1,'\"','\\\"') WHERE (((ALL_SITES.CustAddress1) Like '%\"%'));",
            "UPDATE ALL_SITES SET ALL_SITES.CustAddress2 = Replace(CustAddress2,'\\','/') WHERE (((ALL_SITES.CustAddress2) Like '%\\%'));"
            "UPDATE ALL_SITES SET ALL_SITES.Code = '200' WHERE (Code='13025' or Code ='1');",
            "UPDATE ALL_SITES SET ALL_SITES.fire = 0 WHERE fire IS NULL;",
            "UPDATE ALL_SITES SET ALL_SITES.potable = 0 WHERE potable IS NULL;",
            "UPDATE ALL_SITES SET ALL_SITES.irrigation = 0 WHERE irrigation IS NULL;",
            "UPDATE ALL_SITES SET ALL_SITES.is_due_install = 0 WHERE is_due_install IS NULL;",
            "UPDATE ALL_SITES SET ALL_SITES.is_backflow = 0 WHERE is_backflow IS NULL;",
            "update ALL_SITES set CustomerName = 'Unknown' where CustomerName is null;",
            "UPDATE ALL_SITES SET ALL_SITES.address1 = [ALL_SITES].[address2] WHERE (ALL_SITES.address1='' or address1 is Null);",
            "UPDATE ALL_SITES SET ALL_SITES.address2 = '' WHERE (ALL_SITES.address2=address1);",
            "UPDATE ALL_SITES SET ALL_SITES.address1 = 'Unknown' where address1 is Null or address1 = '';",
            """UPDATE ALL_SITES
SET ALL_SITES.Code = (Select Pval from Pvals WHERE ([Pval_ID]=[Code])),
    ALL_SITES.CustState = (select Pval from Pvals WHERE (Pval_ID=CustState));""",
            "update ALL_SITES set Code = 'Other' where Code is null;",
            "UPDATE ALL_SITES SET ALL_SITES.meter_reading = 0 WHERE (meter_reading='' or meter_reading is null);",
        )
        self._execute_list(sqls)

    def _preload_surveys(self):
        print "======== PRELOADING SURVEYS ========"
        sqls = (
            "update Surveys set AccountNumber = '2004614i-30' where AccountNumber = '2004614F-30';",
            "update Surveys set AccountNumber = '2004560i-30' where AccountNumber = '2004560F-30';",
            "INSERT INTO ALL_SURVEYS ([site], service_type, Surveyor, survey_date, Metered, pump_present, additives_present, cc_present, Protected, aux_water, detector_manufacturer, detector_model, detector_serial, Notes, Special, old_id ) SELECT ALL_SITES.ID, Surveys.[Type], LOWER([Surveyor]) AS LS, Surveys.SurveyDate, isnull((select 1 where LOWER([Metered])='yes'), 0) AS mtr, isnull((select 1 where LOWER([PumpPresent])='yes'), 0) AS pmp, isnull((select 1 where LOWER([Additives])='yes'), 0) AS adt, isnull((select 1 where LOWER([CCPresent])='yes'), 0) AS ccp, isnull((select 1 where LOWER([Protected])='yes'), 0) AS prt, isnull((select 1 where LOWER([AuxWater])='yes'), 0) AS auw, Surveys.DetectorManufacturer, Surveys.DetectorModelNo, Surveys.DetectorSerialNo, Surveys.Notes, Surveys.Special, Surveys.SurveyID FROM Surveys, ALL_SITES WHERE ([ALL_SITES].[AccountNumber]=[Surveys].[AccountNumber]);",
            """UPDATE ALL_SURVEYS SET ALL_SURVEYS.service_type = (select [Pval] from Pvals WHERE [Pval_ID]=[service_type]),
    ALL_SURVEYS.detector_manufacturer = (select [Pval] from Pvals WHERE [Pval_ID]=[detector_manufacturer]),
    ALL_SURVEYS.special = (select [Pval] from Pvals WHERE [Pval_ID]=[special]);""",
            "UPDATE ALL_SURVEYS SET ALL_SURVEYS.notes = Replace([ALL_SURVEYS].[notes],(Char(13) + Char(10)),'') WHERE ((ALL_SURVEYS.notes) Like ('%' + Char(13) + Char(10) + '%'));",
            "UPDATE ALL_SURVEYS SET ALL_SURVEYS.notes = Replace([ALL_SURVEYS].[notes],'\"','\\\"') WHERE (((ALL_SURVEYS.notes) Like ('%\"%')));",
        )
        self._execute_list(sqls)

    def _preload_hazards(self):
        print "======== PRELOADING HAZARDS ========"
        sqls = (
            """INSERT INTO ALL_HAZARDS ( 
	hazard_type, assembly_status, bp_type_required,
	due_install_test_date,survey, service_type, 
	[site], assembly_location, installer,
	install_date, replace_date, orientation,
	bp_type_present, bp_size, bp_manufacturer,
	model_no, serial_no, old_survey_id, old_device_id )
SELECT Surveys.Hazard1, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, 
	ALL_SURVEYS.ID, BackflowDevices.BPType, ALL_SURVEYS.[site],
	BackflowDevices.AssemblyLocation, BackflowDevices.Installer, BackflowDevices.InstallDate, 
	BackflowDevices.ReplaceDate, BackflowDevices.Orientation, BackflowDevices.TypeBPProvided,
	BackflowDevices.BPSize, BackflowDevices.Manufacturer, BackflowDevices.ModelNo,
	BackflowDevices.SerialNo, BackflowDevices.SurveyID, BackflowDevices.BackflowID
FROM BackflowDevices, Surveys, ALL_SURVEYS 
WHERE ALL_SURVEYS.old_id=BackflowDevices.SurveyID and Surveys.SurveyID=BackflowDevices.SurveyID;""",
            """UPDATE ALL_HAZARDS set
ALL_HAZARDS.installed_properly = isnull((select 1 where LOWER(BackflowDevices.InstalledProperly)='yes'), 0)
FROM BackflowDevices
where ALL_HAZARDS.old_device_id = BackflowDevices.BackflowID""",
            "update ALL_HAZARDS set ALL_HAZARDS.service_type = (Select Pval from Pvals WHERE service_type=Pval_ID);",
            """INSERT INTO ALL_HAZARDS ( 
	hazard_type, assembly_status, bp_type_required, 
	due_install_test_date, survey, 
	service_type, site, old_survey_id ) 
SELECT Surveys.Hazard1, Surveys.AssemblyStatus, Surveys.TypeBPReqd, 
	Surveys.DueInstall, ALL_SURVEYS.ID, ALL_SURVEYS.service_type, 
	ALL_SURVEYS.site, Surveys.SurveyID 
FROM Surveys, ALL_SURVEYS 
WHERE [Hazard1] Is Not Null AND 
	[ALL_SURVEYS].[old_id]=[Surveys].[SurveyID] AND
	Surveys.SurveyID not in (Select ALL_HAZARDS.old_survey_id from ALL_HAZARDS)""",
            "INSERT INTO ALL_HAZARDS ( hazard_type, assembly_status, bp_type_required, due_install_test_date, survey, service_type, site, old_survey_id ) SELECT Surveys.Hazard2, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, ALL_SURVEYS.ID, ALL_SURVEYS.service_type, ALL_SURVEYS.site, ALL_SURVEYS.old_id FROM Surveys, ALL_SURVEYS WHERE (([Hazard2] Is Not Null) AND ([ALL_SURVEYS].[old_id]=[Surveys].[SurveyID]));",
            "INSERT INTO ALL_HAZARDS ( hazard_type, assembly_status, bp_type_required, due_install_test_date, survey, service_type, site, old_survey_id ) SELECT Surveys.Hazard3, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, ALL_SURVEYS.ID, ALL_SURVEYS.service_type, ALL_SURVEYS.site, ALL_SURVEYS.old_id FROM Surveys, ALL_SURVEYS WHERE (([Hazard3] Is Not Null) AND ([ALL_SURVEYS].[old_id]=[Surveys].[SurveyID]));",
            "INSERT INTO ALL_HAZARDS ( hazard_type, assembly_status, bp_type_required, due_install_test_date, survey, service_type, site, old_survey_id ) SELECT Surveys.Hazard4, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, ALL_SURVEYS.ID, ALL_SURVEYS.service_type, ALL_SURVEYS.site, ALL_SURVEYS.old_id FROM Surveys, ALL_SURVEYS WHERE (([Hazard4] Is Not Null) AND ([ALL_SURVEYS].[old_id]=[Surveys].[SurveyID]));",
            "INSERT INTO ALL_HAZARDS ( hazard_type, assembly_status, bp_type_required, due_install_test_date, survey, service_type, site, old_survey_id ) SELECT Surveys.Hazard5, Surveys.AssemblyStatus, Surveys.TypeBPReqd, Surveys.DueInstall, ALL_SURVEYS.ID, ALL_SURVEYS.service_type, ALL_SURVEYS.site, ALL_SURVEYS.old_id FROM Surveys, ALL_SURVEYS WHERE (([Hazard5] Is Not Null) AND ([ALL_SURVEYS].[old_id]=[Surveys].[SurveyID]));",
            "UPDATE Pvals SET Pvals.Pval = 'Landscape Nursery' WHERE (((Pvals.Pval) Like 'Landscape Nursery%'));",
            """UPDATE ALL_HAZARDS
                SET
                ALL_HAZARDS.hazard_type = (Select Pval from Pvals WHERE hazard_type=Pval_ID),
                ALL_HAZARDS.assembly_location = (Select Pval from Pvals WHERE assembly_location=Pval_ID),
                ALL_HAZARDS.bp_type_present = (Select Pval from Pvals WHERE bp_type_present=Pval_ID),
                ALL_HAZARDS.bp_type_required = (Select Pval from Pvals WHERE bp_type_required=Pval_ID),
                ALL_HAZARDS.bp_size = (Select Pval from Pvals WHERE bp_size=Pval_ID),
                ALL_HAZARDS.bp_manufacturer = (Select Pval from Pvals WHERE bp_manufacturer=Pval_ID);""",
            "UPDATE ALL_HAZARDS set assembly_status='Due Install' where assembly_status='due install'",
            "UPDATE ALL_HAZARDS set assembly_status='Installed' where assembly_status='installed'",
            "update ALL_HAZARDS set installed_properly = 0 where installed_properly is null;",
            "UPDATE ALL_HAZARDS SET ALL_HAZARDS.bp_size = '1.25\"' WHERE ALL_HAZARDS.bp_size = '1.25';",
            "UPDATE ALL_HAZARDS SET ALL_HAZARDS.bp_manufacturer = 'Ames' WHERE ALL_HAZARDS.bp_manufacturer = 'DCDA';",
            "delete from ALL_HAZARDS where ALL_HAZARDS.hazard_type is NULL",
        )
        self._execute_list(sqls)

    def _preload_devices(self):
        print "======== PRELOADING DEVICES ========"
        sqls = (
            """INSERT INTO ALL_DEVICES ( 
                    due_install_test_date, assembly_location, installer,
                    install_date, replace_date, orientation, installed_properly,
                    bp_type_present, bp_size, bp_manufacturer,
                    model_no, serial_no, old_device_id, hazard )
                SELECT
                    due_install_test_date, assembly_location, installer,
                    install_date, replace_date, orientation, installed_properly,
                    bp_type_present, bp_size, bp_manufacturer,
                    model_no, serial_no, old_device_id, ID
                FROM ALL_HAZARDS
                WHERE ALL_HAZARDS.old_device_id is not NULL""",
            "UPDATE ALL_HAZARDS SET ALL_HAZARDS.bp_device = ALL_DEVICES.ID FROM ALL_DEVICES WHERE ALL_HAZARDS.ID = ALL_DEVICES.hazard",
            "UPDATE ALL_DEVICES SET bp_type_present = ALL_HAZARDS.bp_type_required FROM ALL_HAZARDS WHERE ALL_DEVICES.bp_type_present is NULL and ALL_DEVICES.hazard = ALL_HAZARDS.ID",
##            "UPDATE ALL_HAZARDS SET bp_device = NULL where bp_device in (select ALL_DEVICES.ID from ALL_DEVICES where bp_type_present is NULL)",
##            "DELETE FROM ALL_DEVICES WHERE bp_type_present is NULL",
            "UPDATE ALL_DEVICES SET bp_type_present = 'Unknown' where bp_type_present is NULL",
        )
        self._execute_list(sqls)

    def _preload_letters(self):
        print "======== PRELOADING LETTERS ========"
        sqls = (
            "INSERT INTO ALL_LETTERS ( LetterDate, LetterType, Site, Sender) SELECT Letters.LetterDate, Letters.LetterType, ALL_SITES.ID, UserGenerated FROM ALL_SITES, Letters WHERE ([Letters].[AccountNumber]=[ALL_SITES].[AccountNumber]);",
            "Update ALL_LETTERS set LetterType = (select Pval from Pvals where Pval_ID = LetterType);",
            "Update ALL_LETTERS set LetterType = 'Annual Test First' where lettertype='Annual Test';",
            "Update ALL_LETTERS set LetterType = 'Due Install First' where lettertype='Due Install';",
        )    
        self._execute_list(sqls)

    def _preload_tests(self):
        print "======== PRELOADING TESTS ========"
        sqls = (
            """Insert into ALL_TESTS ( bp_device, tester, [user], test_date, 
                cv1_leaked, cv1_gauge_pressure, cv1_cleaned, cv1_retest_pressure,
                cv2_leaked, cv2_gauge_pressure, cv2_cleaned, cv2_retest_pressure,
                rv_opened, rv_psi1, rv_cleaned, rv_psi2,
                outlet_sov_leaked, 
                cv_leaked, cv_held_pressure, cv_retest_psi,
                pvb_opened, air_inlet_psi, pvb_cleaned, air_inlet_retest_psi,
                test_result, account_number, notes, TesterCertNumber, test_serial, test_manufacturer, test_last_cert )
            SELECT BackflowID, TesterName, [User], TestDate, 
                CheckValve1Status, GaugePressure1Valve1, MaintenanceValve1, MaintPressure2Valve1,
                CheckValve2Status, GaugePressure1Valve2, MaintenanceValve2, MaintPressure2Valve2,
                ReliefValveStatus, ReliefValvePSI, MaintenanceReliefValve, ReliefValvePSI1,
                OutletSOValve,
                CheckValveLeaked, CheckValveHeldPressure, CheckValvePSI,
                PVBOpened, PVBOpenPressure, PVBMaintenance, AirInletPSI,
                case TestResult when 305 then 1 else 0 end, AccountNumber, Notes, TesterCertNumber, TestSerialNumber, TestManufacturer, LastCalibrationDate
            FROM Tests;
            """,
            "update all_tests set cv1_leaked = 0 where cv1_leaked is Null;",
            "update all_tests set cv2_leaked = 0 where cv2_leaked is Null;",
            "update all_tests set cv_leaked = 0 where cv_leaked is Null;",
            "update all_tests set rv_opened = 0 where rv_opened is Null;",
            "update all_tests set pvb_opened = 1 where pvb_opened is Null;",
            "update all_tests set cv1_cleaned = 1 where cv1_cleaned is Null;",
            "update all_tests set cv2_cleaned = 1 where cv2_cleaned is Null;",
            "update all_tests set rv_cleaned = 1 where rv_cleaned is Null;",
            "update all_tests set pvb_cleaned = 1 where pvb_cleaned is Null;",
            "update all_tests set outlet_sov_leaked = 0 where outlet_sov_leaked is Null;",
            "UPDATE ALL_TESTS set bp_device=(select ALL_DEVICES.ID from ALL_DEVICES where ALL_DEVICES.old_device_id=bp_device)",
##            "delete from all_tests where bp_device is null;",
            "UPDATE ALL_TESTS set tester='Bill Travis' where TesterCertNumber='6871'",
            "UPDATE ALL_TESTS set TesterCertNumber='LJP4526', tester='David Zeringue' where TesterCertNumber like '%4526%'",
            "UPDATE ALL_TESTS set TesterCertNumber='2010057', tester='Walter Barado III' where TesterCertNumber like '%201005%' or TesterCertNumber='2010097'",
            "UPDATE ALL_TESTS set TesterCertNumber='LJP4526', tester='David Zeringue' where TesterCertNumber like '%4526%'",
            "UPDATE ALL_TESTS set TesterCertNumber='LJP4527', tester='Michael Zeringue' where TesterCertNumber like '%4527%'",
            "UPDATE ALL_TESTS set tester='Jesse McMillian' where TesterCertNumber='2010031'",
            "UPDATE ALL_TESTS set tester='Gerard Hotard' where TesterCertNumber like '%200900%' or TesterCertNumber like '%20130006%' or tester='G' or tester='Gerard hotard'",
            "UPDATE ALL_TESTS set tester='Chad Varnado' where TesterCertNumber like '%2707%'",
            "UPDATE ALL_TESTS set TesterCertNumber='LJP5731', tester='Joel Frusha' where TesterCertNumber like '%5731%'",
            "UPDATE ALL_TESTS set tester='Leo Raymond' where TesterCertNumber like '%1393%'",
            "UPDATE ALL_TESTS set tester='Leo Raymond' where tester like '%Raymond%'",
            "UPDATE ALL_TESTS set tester='James Syrdal' where TesterCertNumber='2008061301'",
            "UPDATE ALL_TESTS set tester='Eugene Chauvin' where tester like '%Eugene%'",
            "UPDATE ALL_TESTS set tester='Dawn Deshotel' where tester='Dawn Destotel'",
            "UPDATE ALL_TESTS set tester='Arthur Boucher' where tester='Arthur Bouchon' or tester='Arthur boucher'",
            "Update ALL_TESTS set tester='Unknown' where tester is null or tester=''",
            "UPDATE ALL_TESTS set tester='Christian Schmidt' where tester='Chris Schmidt' or tester='christian Schmidt' or tester='christian schmidt' or tester='Christian schmidt'",
            "UPDATE ALL_TESTS set tester='Stephen Kelley' where tester='Steohen Kelley'",
            "UPDATE ALL_TESTS set tester='R.H. Reynolds' where tester='RH Reynolds'",
            "UPDATE ALL_TESTS set tester='David Deville' where tester='David'",
            "UPDATE ALL_TESTS set tester='Donald Gudry' where tester='Donald Guidry'",
            "UPDATE ALL_TESTS set tester='Edward Bonvillian' where tester='Edward Bonvillain'",
            "UPDATE ALL_TESTS set tester='Greg Neely' where tester='Greg Neelly' or tester='Greg neely'",
            "UPDATE ALL_TESTS set tester='Jesse McMillian' where tester='j m'",
            "update ALL_TESTS set TesterCertNumber = '6871' where tester = 'Bill Travis';",
            "update ALL_TESTS set TesterCertNumber = '2707074978-03' where tester = 'Chad Varnado';",
            "update ALL_TESTS set TesterCertNumber = '2014230' where tester = 'Christian Alleman';",
            "update ALL_TESTS set TesterCertNumber = 'UA060-08032013-29386' where tester = 'Christian Schmidt';",
            "update ALL_TESTS set TesterCertNumber = '2013154' where tester = 'Cody Dugas';",
            "update ALL_TESTS set TesterCertNumber = 'LJP-5399' where tester = 'David Deville';",
            "update ALL_TESTS set TesterCertNumber = 'LJP-4526' where tester = 'David Zeringue';",
            "update ALL_TESTS set TesterCertNumber = 'LMP-2209' where tester = 'Edward Bonvillian';",
            "update ALL_TESTS set TesterCertNumber = '000508' where tester = 'Eugene Chauvin';",
            "update ALL_TESTS set TesterCertNumber = '1610' where tester = 'Gary Paline';",
            "update ALL_TESTS set TesterCertNumber = 'R20130006' where tester = 'Gerard Hotard';",
            "update ALL_TESTS set TesterCertNumber = '2014199' where tester = 'Greg Neely';",
            "update ALL_TESTS set TesterCertNumber = 'LJP4501' where tester = 'Jeff';",
            "update ALL_TESTS set TesterCertNumber = '2014222' where tester = 'Jeremy Griffin';",
            "update ALL_TESTS set TesterCertNumber = '2010031' where tester = 'Jesse McMillian';",
            "update ALL_TESTS set TesterCertNumber = 'LMP-1481' where tester = 'John Robin';",
            "update ALL_TESTS set TesterCertNumber = '1393' where tester = 'Leo Raymond';",
            "update ALL_TESTS set TesterCertNumber = 'LJP-3187' where tester = 'Lloyd Johnson';",
            "update ALL_TESTS set TesterCertNumber = 'R20130031' where tester = 'R.H. Reynolds';",
            "update ALL_TESTS set TesterCertNumber = 'LJP-2689' where tester = 'Richard Duet';",
            "update ALL_TESTS set TesterCertNumber = 'Unknown' where TesterCertNumber is NULL;",
            "update ALL_TESTS set test_manufacturer = (select Pval from Pvals where Pval_ID = test_manufacturer)",
            "UPDATE ALL_TESTS SET ALL_TESTS.notes = Replace([ALL_TESTS].[notes],Char(13),' ') WHERE (ALL_TESTS.notes Like ('%' + Char(13) + '%'));",
            "UPDATE ALL_TESTS SET ALL_TESTS.notes = Replace([ALL_TESTS].[notes],Char(10),'') WHERE (ALL_TESTS.notes Like ('%' + Char(10) + '%'));",
            "update all_tests set tester='Brett Mayeaux' where tester='Brett mayeaux';",
            "update ALL_TESTS set tester='Cody Dugas' where tester='cody dugas';",
            "update ALL_TESTS set tester='Nathan Carter' where tester='nathan Carter';",
            "UPDATE ALL_TESTS SET ALL_TESTS.notes = Replace([notes],'\"','\\\"') WHERE (((ALL_TESTS.notes) Like '%\"%'));",
            "update all_tests set test_serial='Unknown', test_manufacturer=NULL where test_serial is NULL",
            "update all_tests set test_manufacturer='Midwest' where test_serial in ('02141335', '03081402', '03081482', '09071723','10101981','11091672','11101625','12100678')",
            "update all_tests set test_manufacturer='Wilkins' where test_serial = '04090973'",
            "update all_tests set test_manufacturer='Watts' where test_serial in ('191722','433934','RMA8530')",
        )
        self._execute_list(sqls)

    def _preload_test_kits(self):
        print "======== PRELOADING TEST KITS ========"
        sqls = (
            "INSERT INTO ALL_TEST_KITS ( [user], serial, manufacturer, last_cert ) \
(select tester, test_serial, test_manufacturer, MAX(test_last_cert) \
from ALL_TESTS \
group by tester, test_serial, test_manufacturer)",
            "Update ALL_TESTS set test_kit = (select ID from all_test_kits where ALL_TEST_KITS.[user]=ALL_TESTS.tester and ALL_TEST_KITS.serial=ALL_TESTS.test_serial and ALL_TEST_KITS.manufacturer=ALL_TESTS.test_manufacturer);"
        ) 
        self._execute_list(sqls)

    def _preload_tester_certs(self):
        print "======== PRELOADING TESTER CERTS ========"
        sqls = (
            "INSERT INTO ALL_TESTER_CERTS ( [user], cert_number ) \
(select tester, TesterCertNumber from ALL_TESTS \
group by tester, TesterCertNumber);",
            "Update ALL_TESTS set tester_cert = (select ID from all_tester_certs where ALL_TESTer_cerTS.[user]=ALL_TESTS.tester and ALL_TESTer_cerTS.cert_number=ALL_TESTS.testercertnumber);",
        )    
        self._execute_list(sqls)


class Formatter(Connector):
    CREATE_TABLE_PATTERN = "create table %s (ID int IDENTITY(1, 1) PRIMARY KEY, %s);"
    FIELD_PATTERN = "[%s] %s %s"
    TABLES = {
        "sites": ("ALL_SITES", [
            "Customer", "PWS", ("connect_date", "date"),
            "address1", "address2", "street_number", "apt", "city", "state", "zip",
            "site_use", "site_type", "floors", "ic_point",
            ("potable", "bit"), ("fire", "bit"), ("irrigation", "bit"),
            ("is_due_install", "bit"), ("is_backflow", "bit"),
            "route", "meter_number", "meter_size", "meter_reading",
            "CustomerName", "AccountNumber", "CustCity", "Code",
            "CustZip", "CustAddress1", "CustAddress2", "CustApt", "CustState",
            ("LastSurveyDate", "date"), ("NextSurveyDate", "date")
        ]),
        "pws": ("ALL_PWS", [
            "Number", "Name", "City", "WaterSource"
        ]),
        "letters": ("ALL_LETTERS", ["Site", ("LetterDate", "date"), "LetterType", "Sender"]),
        "surveys": ("ALL_SURVEYS", [
            "site", "service_type", ("survey_date", "date"),
            "survey_type", "surveyor", ("metered", "bit"),
            ("pump_present", "bit"), ("additives_present", "bit"), ("cc_present", "bit"),
            ("protected", "bit"), ("aux_water", "bit"),
            "detector_manufacturer", "detector_model", "special", "detector_serial",
            ("notes", "nvarchar(max)"), "old_id"
        ]),
        "hazards": ("ALL_HAZARDS", [
            "site", "survey", "service_type", "location1", "location2",
            "hazard_type", "assembly_location", "assembly_status",
            ("installed_properly", "bit"), "installer",
            ("install_date", "date"), ("replace_date", "date"),
            "orientation", "bp_type_present", "bp_type_required",
            "bp_size", "bp_manufacturer", "model_no", "serial_no",
            ("due_install_test_date", "date"), "old_survey_id", "old_device_id", "bp_device"
        ]),
        "bp_devices": ("ALL_DEVICES", [
            "hazard", "bp_type_present", "assembly_location",
            "bp_size", "bp_manufacturer", "model_no", "serial_no",
            ("due_install_test_date", "date"),
            ("installed_properly", "bit"), "installer",
            ("install_date", "date"), ("replace_date", "date"),
            "orientation", "old_device_id"
        ]),
        "tests": ("ALL_TESTS", [
            "bp_device", "tester", "user", ("test_date", "date"),
            ("cv1_leaked", "bit"), "cv1_gauge_pressure", ("cv1_cleaned", "bit"), "cv1_retest_pressure",
            ("cv2_leaked", "bit"), "cv2_gauge_pressure", ("cv2_cleaned", "bit"), "cv2_retest_pressure",
            ("rv_opened", "bit"), "rv_psi1", ("rv_cleaned", "bit"), "rv_psi2",
            ("outlet_sov_leaked", "bit"),
            ("cv_leaked", "bit"), "cv_held_pressure", "cv_retest_psi",
            ("pvb_opened", "bit"), "air_inlet_psi", ("pvb_cleaned", "bit"), "air_inlet_retest_psi",
            ("test_result", "bit"), "account_number",
            ("notes", "nvarchar(max)"), "TesterCertNumber", "test_serial", "test_manufacturer", ("test_last_cert", "date"),
                "test_kit", "tester_cert"
        ]),
        "test_kits": ("ALL_TEST_KITS", [
            "user", "serial", "manufacturer", ("last_cert", "date")
        ]),
        "tester_certs": ("ALL_TESTER_CERTS", [
            "user", "cert_number"
        ]),
    }

    def _create_tables(self):
        print "======== CREATING TABLES ========"
        for table in self.TABLES.values():
            try:
                sql = "DROP TABLE %s;" % table[0]
            except Exception as e:
                print "%s" % e
            self._execute(sql)
            sql = self.CREATE_TABLE_PATTERN % (table[0], self._format_fields(table[1]))
            self._execute(sql)

    def _format_fields(self, field_list):
        formatted_field_list = []
        for field in field_list:
            if isinstance(field, tuple):
                if field[1] == "bit":
                    formatted_field_list.append(self.FIELD_PATTERN % (field[0], field[1], ""))
                else:
                    formatted_field_list.append(self.FIELD_PATTERN % (field[0], field[1], "null"))
            else:
                formatted_field_list.append(self.FIELD_PATTERN % (field, "nvarchar(255)", "null"))
        return ', '.join(formatted_field_list)

    def _preload(self):
        preloader = Preloader()
        preloader.preload()

    def prepare_db(self):
        self._connect()
        self._create_tables()
        self._disconnect()
        self._preload()


class Jsoner(object):
    def __init__(self):
        models = {}
        self.models = {
            "webapp.sourcetype": {},
            "webapp.sitetype": {},
            "webapp.siteuse": {},
            "webapp.servicetype": {},
            "webapp.sitestatus": {},
            "webapp.surveytype": {},
            "webapp.bpsize": {},
            "webapp.bpmanufacturer": {},
            "webapp.customercode": {},
            "webapp.hazardtype": {},
            "webapp.testmanufacturer": {},
            "webapp.icpointtype": {},
            "webapp.assemblylocation": {},
            "webapp.assemblystatus": {},
            "webapp.lettertype": {},
            "webapp.floorscount": {},
            "webapp.special": {},
            "webapp.orientation": {},
            "test.maintenance": {},
            "auth.user": {
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
                "rleblanc": 8,
                "cdugas": 9,
                "dlouque": 10,
                "rdufrene": 11,
                "rmeyer": 12,
                "dmccann": 13,
                "mjacaruso": 14,
                "mvitale": 15,
                "ncarter": 16,
                "Adam Hodges": 21,
                "Al Wilder": 22,
                "Amado Enamorado": 23,
                "Ar.": 24,
                "Arthur Boucher": 25,
                "B Miller": 26,
                "Barry Conner": 27,
                "Ben": 28,
                "Bill Travis": 29,
                "Billy Johnson": 30,
                "Blake Louviere": 31,
                "Brett Mayeaux": 32,
                "Central plumbing": 33,
                "Chad Varnado": 34,
                "Charles Schaub": 35,
                "Chris Montalbano": 36,
                "Christian Alleman": 37,
                "Christian Schmidt": 38,
                "Cody Dugas": 9,
                "Dale Guillory": 40,
                "Daryl A Heyl": 41,
                "David Deville": 42,
                "David Zeringue": 43,
                "Dawn Deshotel": 44,
                "Donald Gudry": 45,
                "Doug Gremillion": 46,
                "Ed Dimaggio": 47,
                "Edward Bonvillian": 48,
                "Eugene Chauvin": 49,
                "Floyd Mitchell": 50,
                "Gary Paline": 51,
                "Gerard Hotard": 52,
                "Greg Neely": 53,
                "James Syrdal": 54,
                "james wilson": 55,
                "Jason Fontenot": 56,
                "Jeff": 57,
                "Jeremy Griffin": 58,
                "Jesse McMillian": 59,
                "Joel Frusha": 60,
                "John Alfred": 61,
                "John Robin": 62,
                "Kenneth": 63,
                "Kevin Doise": 64,
                "Kyle Robicheaux": 65,
                "Larry Dale Cole": 66,
                "Leo Raymond": 67,
                "Lloyd Johnson": 68,
                "Louis Bienvenu": 69,
                "Luke George": 70,
                "Mark Malte": 71,
                "Mark Michel": 72,
                "Melvin Etue": 73,
                "Michael Nunez": 74,
                "Michael Zeringue": 75,
                "Nathan Carter": 16,
                "Nolan": 77,
                "Perirroux": 78,
                "Phillip Gremillion": 79,
                "R.H. Reynolds": 80,
                "Richard Duet": 81,
                "Ronnie": 82,
                "Ronnie Cruse": 83,
                "Roy Tillman": 84,
                "Stacy Fletcher": 85,
                "Stephen Kelley": 86,
                "Steve Cole": 87,
                "Ted Hebert": 88,
                "Unknown": 89,
                "Walter Barado III": 90,
                "William laird": 91,
                "William Laird": 91,
                "Armand Malbrough": 92,
                "Barry Brunet": 93,
                "Chrisitan Alleman": 37,
                "Chrisitan Schmidt": 38,
                "Chrsitian Alleman": 37,
                "christian alleman": 37,
                "floyd mitchell": 50,
                "Geg Neely": 53,
                "Geraard Hotard": 52,
                "Gerad Hotard": 52,
                "Jessie McMillian": 59,
                "Joey Alfred": 100,
                "Jude Barker": 94,
                "Kevin Martinez": 95,
                "Mar kMichel": 72,
                "Mike Lasseigne": 96,
                "Patrick Gremillon": 97,
                "Phillip  Gremillion": 79,
                "Randall Fontenot": 98,
                "Randy Scott": 99,
                "NCARTER": 16,
                "joey alfred": 100,
                "CHRISTIAN ALLEMAN": 37,
                "Christian alleman": 37,
                "Phillip gremillion": 79,
                "Barry brunet": 93,
            }
        }
        self.fill_json()
        #self.print_json()

    def fill_json(self):
        f = open("data_base.json")
        json_data = json.loads(f.read())
        for json_object in json_data:
            if json_object["model"] == 'webapp.lettertype':
                self.models[json_object["model"]][json_object["fields"]["letter_type"]] = json_object["pk"]
            else:
                self.models[json_object["model"]][json_object["fields"].values()[0]] = json_object["pk"]
        for model in self.models:
            self.models[model][""] = "null"
        f.close()

    def print_json(self):
        print json.dumps(self.models, indent=4, separators=(',', ': '))


class Dumper(Connector):
    TEMPLATES = {
        'site': BASE_TEMPLATE % (
            '{"status":1,"pws":%s,"connect_date":"%s","address1":"%s","address2":"%s","street_number":"%s","apt":"%s",\
            "city":"%s","state":"%s","zip":"%s","site_use":%s,"site_type":%s,"floors":%s,"interconnection_point":%s,\
            "meter_number":"%s","meter_size":"%s","meter_reading":%s,"route":"%s","potable_present":%s,"fire_present":%s,"irrigation_present":%s,\
            "is_due_install":%s,"is_backflow":%s,"cust_number":"%s","cust_name":"%s","cust_code":%s,"cust_address1":"%s","cust_address2":"%s","cust_apt":"%s",\
            "cust_city":"%s","cust_state":"%s","cust_zip":"%s","contact_phone":"","contact_fax":"","contact_email":"",\
            "notes":"","last_survey_date":"%s","next_survey_date":"%s"}',
            '"webapp.site"',
            '%s'
        ),
        'survey': BASE_TEMPLATE % (
        '{"site":%s,"service_type":%s,"survey_date":"%s","survey_type":null,"surveyor":%s,"metered":%s,"pump_present":%s,"additives_present":%s,"cc_present":%s,"protected":%s,"aux_water":%s,"detector_manufacturer":"%s","detector_model":"%s","detector_serial_no":"%s","special":%s,"notes":"%s","hazards":[%s]}',
        '"webapp.survey"', '%s'),
        'hazard': BASE_TEMPLATE % (
            '{"site":%s,"service_type":%s,"location1":"","location2":"","hazard_type":%s,\
             "assembly_status":"%s","bp_type_required":"%s","is_present":true,"notes":"","bp_device":%s}',
            '"webapp.hazard"',
            '%s'
        ),
        'device': BASE_TEMPLATE % (
            '{"assembly_location":%s,"installed_properly":%s,"installer":"%s",\
              "install_date":"%s","replace_date":"%s",\
              "orientation":%s,"bp_type_present":"%s",\
              "bp_size":%s,"manufacturer":%s,"model_no":"%s",\
              "serial_no":"%s","due_test_date":"%s","notes":""}',
            '"webapp.bpdevice"',
            '%s'
        ),
        'pws': BASE_TEMPLATE % ('{"number":"%s","name":"%s","city":"","water_source":%s,"notes":""}', '"webapp.pws"', '%s'),
        'letter': BASE_TEMPLATE % ('{"already_sent":true,"site":%s,"letter_type":%s,"date":"%s","user":%s}', '"webapp.letter"', '%s'),
        'test': BASE_TEMPLATE % (
            '{"outlet_sov_leaked":%s,"rv_psi1":%s, "rv_psi2":%s, "cv2_cleaned": "%s",\
            "cv2_retest_gauge_pressure": %s, "cv_retest_psi": %s, \
            "air_inlet_retest_psi": %s,"cv2_leaked": %s, "cv_held_pressure": %s, \
            "cv2_gauge_pressure": %s, "pvb_cleaned": "%s", "tester": %s,\
            "cv1_cleaned": "%s", "paid": true, "air_inlet_opened": %s, "air_inlet_psi": %s,"user": %s, \
            "test_result": %s, "cv1_retest_gauge_pressure": %s, "cv1_gauge_pressure": %s,\
            "rv_opened": %s, "cv1_leaked": %s, "bp_device": %s, "cv_leaked": %s, "notes": "%s", \
            "test_date": "%s", "rv_cleaned": "%s", "test_kit": %s, "tester_cert": %s}',
            '"webapp.test"',
            '%s'
        ),
        'test_kit': BASE_TEMPLATE % ('{"user":%s,"test_serial":"%s","test_manufacturer":%s,"test_last_cert":"%s"}', '"webapp.testkit"', '%s'),
        'tester_cert': BASE_TEMPLATE % ('{"user":%s,"cert_number":"%s"}', '"webapp.testercert"', '%s'),
    }
    SQL_STRS = {
        'dump_sites': 'select PWS, connect_date, address1, address2, street_number, apt, city, state, zip, site_use, site_type, floors, ic_point, \
meter_number, meter_size, meter_reading, route, potable, fire, irrigation, is_due_install, is_backflow, \
AccountNumber, CustomerName, Code, CustAddress1, CustAddress2, CustApt, CustCity, CustState, CustZip, \
LastSurveyDate, NextSurveyDate, ID from ALL_SITES',
        'dump_surveys': 'select site, service_type, survey_date, surveyor, metered, pump_present, additives_present, cc_present, protected, aux_water, detector_manufacturer, detector_model, detector_serial, special, notes, \'hph\', ID from ALL_SURVEYS',
        'dump_pwss': 'select Number, Name, WaterSource, ID from ALL_PWS',
        'dump_hazards': 'select site, service_type, hazard_type, assembly_status, bp_type_required, bp_device, ID from ALL_HAZARDS',
        'dump_devices': 'select assembly_location, installed_properly, installer, install_date, replace_date, orientation, bp_type_present, bp_size, bp_manufacturer, model_no, serial_no, due_install_test_date, ID from ALL_DEVICES',
        'dump_letters': 'select site, lettertype, letterdate, sender, ID from ALL_LETTERS',
        'dump_tests': 'select outlet_sov_leaked, rv_psi1, rv_psi2, cv2_cleaned,\
cv2_retest_pressure, cv_retest_psi, air_inlet_retest_psi, cv2_leaked, cv_held_pressure,\
cv2_gauge_pressure, pvb_cleaned, tester, cv1_cleaned,\
pvb_opened, air_inlet_psi, [user], test_result, cv1_retest_pressure, cv1_gauge_pressure,\
rv_opened, cv1_leaked, bp_device, cv_leaked, notes, test_date, rv_cleaned, test_kit, tester_cert, ID from ALL_TESTS',
        'dump_test_kits':  'select [user], serial, manufacturer, last_cert, ID from ALL_TEST_KITS',
        'dump_tester_certs':  'select [user], cert_number, ID from ALL_TESTer_cerTS',
    }
    DATA_TYPES = [
        'pws',
        'site',
        'survey',
        'hazard',
        'device',
        'letter',
        'test',
        'test_kit',
        'tester_cert'
    ]
    FIELDS_TO_REPLACE = {
        'site': [(9, "webapp.siteuse"),
                 (10, "webapp.sitetype"),
                 (11, "webapp.floorscount"),
                 (12, "webapp.icpointtype"),
                 (24, "webapp.customercode")],
        'survey': [(1, "webapp.servicetype"),
                   (3, "auth.user"),
                   (13, "webapp.special")],
        'hazard': [(1, "webapp.servicetype"),
                   (2, "webapp.hazardtype"),
                   (3, "webapp.assemblystatus")],
        'device': [(0, "webapp.assemblylocation"),
                   (5, "webapp.orientation"),
                   (7, "webapp.bpsize"),
                   (8, "webapp.bpmanufacturer")],
        'pws': [(2, "webapp.sourcetype")],
        'letter': [(1, "webapp.lettertype"),
                   (3, "auth.user")],
        'test': [(3, "test.maintenance"),
                 (10, "test.maintenance"),
                 (11, "auth.user"),
                 (12, "test.maintenance"),
                 (15, "auth.user"),
                 (25, "test.maintenance")],
        'test_kit': [(0, 'auth.user'),
                     (2, "webapp.testmanufacturer")],
        'tester_cert': [(0, 'auth.user')],
    }

    def __init__(self):
        #formatter = Formatter()
        #formatter.prepare_db()
        self.jsoner = Jsoner()
        self._connect()
        self._connect_another()

    def dump(self):
        for data_type in self.DATA_TYPES:
            row_c = 0
            f = codecs.open("raw_data_%s_0.json" % data_type, 'w', 'utf-8')
            f.write('[')
            print "=== Starting %s dump ===" % data_type
            try:
                file_count = 0
                sql_str = self.SQL_STRS["dump_%ss" % data_type]
                template = self.TEMPLATES[data_type]
                self.cursor.execute(sql_str)
                row = self.cursor.fetchone()
                data = self.replace_nones(template % tuple(self.replace_fields(row, data_type)))
                f.write('\n' + data)
                row = self.cursor.fetchone()
                row_c = 1;
                delim = ',\n'
                while row:
                    data = self.replace_nones(template % tuple(self.replace_fields(row, data_type)))
                    f.write(delim + data)
                    row = self.cursor.fetchone()
                    row_c += 1;
                    delim = ',\n'
                    if row_c > 4999:
                        row_c = 0
                        f.write('\n]')
                        f.close()
                        file_count += 1
                        f = codecs.open("raw_data_%s_%s.json" % (data_type, file_count), 'w', 'utf-8')
                        f.write('[')
                        delim = '\n'
            except Exception as e:
                print row
                print
                print row_c
                print unicode(e)
                print
            f.write('\n]')
            f.close()
            print "=== Finished %s dump ===" % data_type
        self._disconnect()
        self._disconnect_another()

    def _get_hazards_for_survey(self, survey_id):
        sql_str = 'select ID from ALL_HAZARDS where ALL_HAZARDS.survey = \'%s\';' % survey_id
        self.cursor2.execute(sql_str)
        hazard_ids = []
        row = self.cursor2.fetchone()
        while row:
            hazard_ids.append(str(row[0]))
            row = self.cursor2.fetchone()
        return ",".join(hazard_ids)

    def replace_nones(self, string):
        return string.replace("None", "null").replace("False", "false").replace("True", "true").replace('"null"', 'null')

    def replace_fields(self, row, data_type):
        for index, model in self.FIELDS_TO_REPLACE[data_type]:
            if row[index]:
                row[index] = self.jsoner.models[model][row[index]]
            else:
                row[index] = "null"
        # replace letter date, remove time part
        if data_type == "letter" and row[1]:
            row[1] = ('%s' % row[1])[:10]
        # and for survey
        if data_type == "survey" and row[2]:
            row[2] = ('%s' % row[2])[:10]
            row[15] = self._get_hazards_for_survey(row[16])
        # and replacing blank values on site.meter_reading with Nulls
        if data_type == "site" and row[13] == "":
            row[13] = 'null'
        return row

    def dump_testers(self):
        print "====== Dumping Testers ======"
        f = codecs.open("raw_data_testers_0.json", 'w', 'utf-8')
        f.write('[')
        self.cursor.execute('select distinct tester from all_tests')
        rows = self.cursor.fetchall()
        last_row = rows.pop(-1)
        for row in rows:
            f.write(self.get_tester(row))
        f.write(self.get_tester(last_row))
        f.write('\n]')
        f.close()

    def get_tester(self, row):
        template = """
{
  "fields": {
    "username": "%s",
    "first_name": "%s",
    "last_name": "%s",
    "is_active": true,
    "is_superuser": false,
    "is_staff": false,
    "last_login": "2015-04-07T08:56:00Z",
    "groups": [
      [
        "Testers"
      ]
    ],
    "user_permissions": [],
    "password": "pbkdf2_sha256$12000$bZ6VGUBnh5rh$dpAdMMyiWajKfBeYTH1axbt7u0ychcgOoJMIRe8inbM=",
    "email": "",
    "date_joined": "2015-03-09T08:27:26Z"
  },
  "model": "auth.user",
  "pk": %s
},
{
  "fields": {
    "city": "",
    "pws": [],
    "zip": "",
    "phone2": "",
    "company": "",
    "phone1": "",
    "state": null,
    "user": [
      "%s"
    ],
    "address": ""
  },
  "model": "webapp.employee",
  "pk": %s
},"""
        first_name, last_name, username = self.handle_tester_names(row[0])
        tester_pk = self.jsoner.models['auth.user'][row[0]]
        tester = template % (username, first_name, last_name, tester_pk, username, tester_pk)
        tester.replace('"null"', 'null')
        return tester

    def handle_tester_names(self, names):
        names = names.split()
        first_name = names[0]
        if len(names) < 2:
            last_name = ""
            username = (first_name[0] + first_name).lower()
        else:
            last_name = names[1]
            username = (first_name[0] + last_name).lower()
        return first_name, last_name, username
                

if __name__ == '__main__':
    dumper = Dumper()
    dumper.dump_testers()
    dumper.dump()
