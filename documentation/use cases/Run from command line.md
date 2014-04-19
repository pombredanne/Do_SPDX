1. **Title**: Run the do_spdx executable for a command line use
2. **Primary Actor**: Command line user
3. **Goal in Context**: To create an SPDX document based on the path to a package given by the configuration file.
4. **Stakeholders and Interests**: 
   1. **Original code writers**:
      1. To communicate the licensing information for the code that is going to be scanned.
   1. **Consumers of the upstream source**:
      1. To receiver accurate and clear information of licensing of upstream source
      2. To be able to comply easily with licenses for upstream source
5. **Preconditions**:
   1. Command line user has decided on a package to scan
6. **Main Success Scenario**: The command line user successfully received an SPDX document for the given package and the database cache updates so the document may be accessed by the SPDX Dashboard.
7. **Failed End Conditions**:
   1. The command line user gives a bad path to the file to scan.
   2. The command line user doesn’t provide correct information for the configuration file.
   3. There is an internet issue that interferes with the communication between do_spdx and a scanning tool and/or database.
8. **Trigger**
   1. Running the executable do_spdx function
9. **Notes**: N/A