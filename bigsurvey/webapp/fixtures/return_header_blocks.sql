-- MySQL dump
-- Return LeftHeaderBlock and RightHeaderBlock
UPDATE `webapp_lettertype`
SET `template` = REPLACE(`template`, '<td style="width:100%">{PWSLogo}</td>','<td style="width:25%; vertical-align:top">{LeftHeaderBlock}</td><td style="width:50%">{PWSLogo}</td><td style="width: 25%; text-align: right; vertical-align:top">{RightHeaderBlock}</td>');
