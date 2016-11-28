-- MySQL dump
-- Remove LeftHeaderBlock and RightHeaderBlock from Letters Header
UPDATE `webapp_lettertype`
SET `template` = REPLACE(`template`, '<td style="width:25%; vertical-align:top">{LeftHeaderBlock}</td>','');

UPDATE `webapp_lettertype`
SET `template` = REPLACE(`template`, '<td style="width:50%">{PWSLogo}</td>','<td style="width:100%">{PWSLogo}</td>');

UPDATE `webapp_lettertype`
SET `template` = REPLACE(`template`, '<td style="width: 25%; text-align: right; vertical-align:top">{RightHeaderBlock}</td>','');
