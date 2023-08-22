# Unit Test Helper app

from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import *
import os, sys, shutil

# Main Class
class MainWindow(QMainWindow):
    def __init__(self):
            super(MainWindow, self).__init__()
            uic.loadUi("Main.ui", self)
            self.show()
            
            # File -> About action
            self.actionAbout.triggered.connect(self.ActionAbout)
            
            # File -> Exit action
            self.actionExit.triggered.connect(self.ActionExit)
            
            # Edit -> Reset Data action
            self.actionReset_Data.triggered.connect(self.ResetData)
        
            # Register button actions
            self.pb_CreateTestVcxproj.clicked.connect(self.CreateTestVcxprojFile)
            self.pb_BrowseVcxprojFile.clicked.connect(self.BrowseVcxProjFile)
            self.pb_ModifyVcxprojFile.clicked.connect(self.ModifyTestVcxProjFile)
            self.pb_CreateTestPackagesConfig.clicked.connect(self.CreateTestPackagesConfig)
             
    def ActionAbout(self):
        about_text = """
        Application to automate the creation of a Unit Test project for UltraTax.
        Version: 1.0
        Author: Vishal Patel (vishal.patel@thomsonreuters.com)
        """
        QMessageBox.about(self, "About", about_text)
    
    def ActionExit(self):
        QApplication.quit()
        
    def ResetData(self):
        self.le_vcxprojPath.clear()
        self.le_vcxprojFileName.clear()
        self.le_testvcxprojPath.clear()
        self.le_TestPackagesConfigFileName.clear()
        self.le_CalcPackagesConfigFileName.clear()
    
    def BrowseVcxProjFile(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select .vcxproj File", "C:\\", "Visual Studio Project Files (*.vcxproj))")
            if file_path:
                file_name = os.path.basename(file_path)
                self.le_vcxprojPath.setText(file_path)
                self.le_vcxprojFileName.setText(file_name)
        except:
            QMessageBox.critical(self, "Error", "Something went wrong. Please try again.")
              
    def CreateTestVcxprojFile(self):
        if self.le_vcxprojFileName.text():
            source_path = self.le_vcxprojPath.text()
            # Getting the calc directory
            calc_dir = os.path.dirname(source_path)
            # Creating test vcxproj file name
            test_vcxproj_fileName = "__" + self.le_vcxprojFileName.text().split(".")[0] + "_test.vcxproj"
            # Destination path will be same as the calc path
            destination_path = calc_dir + "/" + test_vcxproj_fileName
            try:
                # Copy the file to the destination with the new name. In case the test proejct is already present, it will override that file
                shutil.copy2(source_path, destination_path)
                self.le_testvcxprojPath.setText(destination_path)
                QMessageBox.information(self, "Info", "Created a new " + test_vcxproj_fileName + " successfully!")
            except:
                QMessageBox.critical(self, "Error", "Something went wrong. Please try again.")
        else:
            QMessageBox.warning(self, "vcxproj file not found", "Please select the correct vcxproj file.")
    
    def CreateTestPackagesConfig(self):
        if self.le_vcxprojFileName.text():
            vcxprojPath = self.le_vcxprojPath.text()
            calc_dir = os.path.dirname(vcxprojPath)
            source_path = calc_dir + "/" + "packages.config"
            test_packagesconfig_fileName = "packages." + self.le_vcxprojFileName.text().split(".")[0] + "_test.config"
            destination_path = calc_dir + "/" + test_packagesconfig_fileName
            try:
                # Copy the file to the destination with the new name
                shutil.copy2(source_path, destination_path)
                self.le_TestPackagesConfigFileName.setText(test_packagesconfig_fileName)
                # Rename the calc packages.config
                new_pck_name = "packages." + self.le_vcxprojFileName.text().split(".")[0] + ".config"
                os.rename(source_path, calc_dir + "/" + new_pck_name)
                self.le_CalcPackagesConfigFileName.setText(new_pck_name)
                QMessageBox.information(self, "Info", "Created a new " + test_packagesconfig_fileName + " and renamed calc packages.config successfully!")
            except:
                QMessageBox.critical(self, "Error", "This step has already been completed or packages.config file does not exists.")
        else:
            QMessageBox.warning(self, "Unable to proceed", "Please complete the step 1 to proceed.")
    
    def ModifyTestVcxProjFile(self):
        file_path = self.le_testvcxprojPath.text()
        calc_file_path = self.le_vcxprojPath.text()

        # Check if the file and package path exists
        if os.path.exists(file_path) and self.le_CalcPackagesConfigFileName.text():
            try:
                # Specify the line to be inserted
                insert_line = '</Import>\n<Import Project="$(wincsi_prodcomRootDir)inc\\comcalcs_src\\test.targets">'
                # Specify the target line after which the new line should be inserted
                target_line = '<Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets">'
                # Newly inserted line for verification
                test_target_line = '<Import Project="$(wincsi_prodcomRootDir)inc\\comcalcs_src\\test.targets">\n'

                # Read the contents of the file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Find the index of the target line
                target_line_index = -1
                for i, line in enumerate(lines):
                    if target_line in line:
                        target_line_index = i
                        break
                    
                # Check of the insert_line already present
                insert_line_index = -1
                for i, line in enumerate(lines):
                    if test_target_line in line:
                        insert_line_index = i
                        break
                
                # If the target line is found, insert the new line after it
                if target_line_index != -1 and insert_line_index == -1:
                    lines.insert(target_line_index + 1, insert_line + '\n')

                    # Write the modified contents back to the file
                    with open(file_path, 'w') as file:
                        file.writelines(lines)
                    file.close()
                else:
                    QMessageBox.warning(self, "Warning", "test.targets import already present. Continuing with renaming packages.config")
            except:
                QMessageBox.critical(self, "Error", "Error adding test.target content to the test vcxproj file.")

            try:
                # Modify test vcxprofj file
                old_filename = 'packages.config'
                # New filename 'packages.__XSSclc_test.config'
                new_filename = self.le_TestPackagesConfigFileName.text()
                # Calc packages.config file rename
                new_calc_packageConfig_filename = self.le_CalcPackagesConfigFileName.text()
                
                # Check of the changes are already present
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    
                packages_config_index = -1
                for i, line in enumerate(lines):
                    if old_filename in line:
                        packages_config_index = i
                        break
                    file.close()
                if packages_config_index != -1:
                    # Modify the lines with the new filename
                    with open(file_path, 'r') as tfile:
                        tlines = tfile.readlines()
                        
                    updated_lines = [tline.replace(old_filename, new_filename) for tline in tlines]
                    tfile.close()

                    with open(file_path, 'w') as tfile:
                        tfile.writelines(updated_lines)
                    tfile.close()
                    
                    # Modify calc vcxprofj file
                    with open(calc_file_path, 'r') as cfile:
                        clines = cfile.readlines()
                        
                    cupdated_lines = [cline.replace(old_filename, new_calc_packageConfig_filename) for cline in clines]
                    cfile.close()
                    
                    with open(calc_file_path, 'w') as cfile:
                        cfile.writelines(cupdated_lines)
                    cfile.close()
                    
                    QMessageBox.information(self, "Info", f"Modified {file_path} and {calc_file_path} successfully!")
                else:
                    QMessageBox.warning(self, "Warning", "packages.config already modified. Please proceed to the next step")
            except:
                QMessageBox.critical(self, "Error", "Something went wrong. Please try again.")
        else:
            QMessageBox.warning(self, "Unable to proceed", "Please complete the previous two steps to proceed.")

# Entry point of the application
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())