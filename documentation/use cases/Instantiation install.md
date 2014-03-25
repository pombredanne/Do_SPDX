1. **Title**: Install the do_spdx executable for use within another function/application
2. **Primary Actor**: System user
3. **Goal in Context**: To install the do_spdx module so it can be used by a calling function/application
4. **Stakeholders and Interests**: 
   1. **System user**:
      1. To provide high quality SPDX documents as a result of using this tool
5. **Preconditions**:
   1. Be on a system with access to the internet for download.
6. **Main Success Scenario**: The command line user downloads the executable files and places it in an accessible directory that can be seen by the calling function, where it can instantiate a Do_Spdx() object.
7. **Failed End Conditions**:
   1. There is an internet issue that interferes with the communication between the given download site and the client computer.
   2. The downloaded utility is not within scope of the calling application so instantiation cannot occur
8. **Trigger**
   1. Clicking the download button on the hosting site of choice
9. **Notes**: N/A