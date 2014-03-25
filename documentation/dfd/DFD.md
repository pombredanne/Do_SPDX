Label:
Cache Checker

Description:
This process determines which files already have SPDX segments in the database.

Decomposition:
1. RECEIVE Path to File/Package from Command Line User
2. PARSE Path to File/Package to retrieve File Names
3. BEGIN LOOP
	1. FOREACH File Name in Package from Path to file
		1. READ Files from package_files Table using File Names (Query)
		2. RECEIVE Key from query
		3. BEGIN IF
			1. IF Key < 0
			2. THEN
				1. GROUP Local File into Unmatched Files
			3. ELSE
				1. GROUP Query Result into File License Information
			4. ENDIF
		4. ENDIF
	2. END LOOP
4. END LOOP
5. BEGIN IF
	1. IF Unmatched Files != NULL
	2. THEN
		1. SEND Unmatched FIles to Scanner Calling Utility
	3. ENDIF
6. ENDIF
7. SEND Path to File to SPDX Creation
______________________________________________________________________

Label:
	Scanner Calling Utility

Description:
This process takes files not found in the database and sends them to the scanning utility desired, in our case FOSSology, in order to get file information about licenses.

Decomposition:
1. RECEIVE Unmatched Files from Cache Checker
2. PACKAGE Unmatched Files to Files (Tarball)
3. SEND Files (JSON) to FOSSology
4. END
______________________________________________________________________

Label:
Cache Updater for Files

Description:
This process takes information received from the FOSSology scan and inserts the information into the database.

Decomposition:
1. RECEIVE File Information from FOSSology
2. BEGIN LOOP
	1. FOREACH File in File Information
		1. INSERT Individual File Information into package_files Table
	2. END LOOP
3. END LOOP
4. SEND File License Information to SPDX Creation
______________________________________________________________________

Label:
	SPDX Creation

Description:
This process will be given a path to a file and will retrieve all information needed from the database in order to create an SPDX document. It will then send this to Cache Updater for SPDX to update the database with the new document.

Decomposition:
1. RECEIVE Path to File from Cache Checker and Cache Updater for Files
2. BEGIN LOOP
	1. FOREACH File in Package from Path to file
		1. READ Files from package_files Table  using File Names (Query)
		2. GROUP Database File into Document Information
	2. END LOOP
3. END LOOP
4. CREATE SPDX Document from Document Information
5. SEND SPDX Document to Command Line User