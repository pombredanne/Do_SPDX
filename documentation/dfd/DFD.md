Label:
Cache Checker

Description:
This process determines which files already have SPDX segments in the database.

Decomposition:
RECEIVE Path to File/Package from Command Line User
PARSE Path to File/Package to retrieve File Names
BEGIN LOOP
	FOREACH File Name in Package from Path to file
		READ Files from package_files Table using File Names (Query)
		RECEIVE Key from query
		BEGIN IF
			IF Key < 0
			THEN
				GROUP Local File into Unmatched Files
			ELSE
				GROUP Query Result into File License Information
			ENDIF
		ENDIF
	END LOOP
END LOOP
BEGIN IF
	IF Unmatched Files != NULL
	THEN
		SEND Unmatched FIles to Scanner Calling Utility
	ENDIF
ENDIF
SEND Path to File to SPDX Creation
______________________________________________________________________

Label:
	Scanner Calling Utility

Description:
This process takes files not found in the database and sends them to the scanning utility desired, in our case FOSSology, in order to get file information about licenses.

Decomposition:
RECEIVE Unmatched Files from Cache Checker
PACKAGE Unmatched Files to Files (Tarball)
SEND Files (JSON) to FOSSology
END
______________________________________________________________________

Label:
Cache Updater for Files

Description:
This process takes information received from the FOSSology scan and inserts the information into the database.

Decomposition:
RECEIVE File Information from FOSSology
BEGIN LOOP
	FOREACH File in File Information
		INSERT Individual File Information into package_files Table
	END LOOP
END LOOP
SEND File License Information to SPDX Creation
______________________________________________________________________

Label:
	SPDX Creation

Description:
This process will be given a path to a file and will retrieve all information needed from the database in order to create an SPDX document. It will then send this to Cache Updater for SPDX to update the database with the new document.

Decomposition:
RECEIVE Path to File from Cache Checker and Cache Updater for Files
BEGIN LOOP
	FOREACH File in Package from Path to file
		READ Files from package_files Table  using File Names (Query)
		GROUP Database File into Document Information
	END LOOP
END LOOP
CREATE SPDX Document from Document Information
SEND SPDX Document to Command Line User