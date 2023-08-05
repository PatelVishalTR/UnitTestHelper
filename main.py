# Unit Test Helper app

from PyQt6 import uic
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
            self.pb_CreateVcxproj.clicked.connect(self.CreateVcxprojFile)
            self.pb_BrowseVcxprojFile.clicked.connect(self.BrowseVcxProjFile)
            self.pb_ModifyVcxprojFile.clicked.connect(self.ModifyTestVcxProjFile)
            self.pb_AddtoSln.clicked.connect(self.AddtoSln)
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
              
    def CreateVcxprojFile(self):
        if self.le_vcxprojFileName.text():
            source_path = self.le_vcxprojPath.text()
            calc_dir = os.path.dirname(source_path)
            test_vcxproj_fileName = "__" + self.le_vcxprojFileName.text().split(".")[0] + "_test.vcxproj"
            destination_path = calc_dir + "/" + test_vcxproj_fileName
            try:
                # Copy the file to the destination with the new name
                shutil.copy2(source_path, destination_path)
                self.le_testvcxprojPath.setText(destination_path)
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Created a new " + test_vcxproj_fileName + " successfully!")
                msg.setWindowTitle("Info")
                msg.exec()
            except shutil.Error as e:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("Error! Please try again")
                msg.setWindowTitle("Error")
                msg.exec()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Please select the correct vcxproj file ")
            msg.setWindowTitle("Invalid vcxproj file")
            msg.exec()
    
    def CreateTestPackagesConfig(self):
        if self.le_vcxprojFileName.text():
            vcxprojPath = self.le_vcxprojPath.text()
            calc_dir = os.path.dirname(vcxprojPath)
            source_path = calc_dir + "/" + "packages.config"
            test_packagesconfig_fileName = "packages.__" + self.le_vcxprojFileName.text().split(".")[0] + "_test.config"
            destination_path = calc_dir + "/" + test_packagesconfig_fileName
            try:
                # Copy the file to the destination with the new name
                shutil.copy2(source_path, destination_path)
                self.le_TestPackagesConfigFileName.setText(test_packagesconfig_fileName)
                # Rename the calc packages.config
                new_pck_name = "packages." + self.le_vcxprojFileName.text().split(".")[0] + ".config"
                os.rename(source_path, calc_dir + "/" + new_pck_name)
                self.le_CalcPackagesConfigFileName.setText(new_pck_name)
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Created a new " + test_packagesconfig_fileName + " and renamed calc packages.config successfully!")
                msg.setWindowTitle("Info")
                msg.exec()
            except:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("Error! Please try again")
                msg.setWindowTitle("Error")
                msg.exec()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Please select the correct vcxproj file ")
            msg.setWindowTitle("Invalid vcxproj file")
            msg.exec()
    
    def ModifyTestVcxProjFile(self):
        file_path = self.le_testvcxprojPath.text()
        calc_file_path = self.le_vcxprojPath.text()
        # Specify the line to be inserted
        insert_line = '</Import>\n<Import Project="$(wincsi_prodcomRootDir)inc\\comcalcs_src\\test.targets">'
        # Specify the target line after which the new line should be inserted
        target_line = '<Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets">'
        
        # Pattern to match the old filename 'packages.config'
        old_filename = 'packages.config'
        # New filename 'packages.__XSSclc_test.config'
        new_filename = self.le_TestPackagesConfigFileName.text()
        # Calc packages.config file rename
        new_calc_packageConfig_filename = self.le_CalcPackagesConfigFileName.text()
        # Check if the file exists
        if os.path.exists(file_path):
            try:
                # Read the contents of the file
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                # Find the index of the target line
                target_line_index = -1
                for i, line in enumerate(lines):
                    if target_line in line:
                        target_line_index = i
                        break

                # If the target line is found, insert the new line after it
                if target_line_index != -1:
                    lines.insert(target_line_index + 1, insert_line + '\n')

                    # Write the modified contents back to the file
                    with open(file_path, 'w') as file:
                        file.writelines(lines)
                    file.close()
                else:
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.setText("Error modifying the file")
                    msg.setWindowTitle("Error")
                    msg.exec()
            except:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText(f"Error adding test.target content to the file")
                msg.setWindowTitle("Error")
                msg.exec()
            try:
                # Modify the lines with the new filename
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                updated_lines = [line.replace(old_filename, new_filename) for line in lines]
                with open(file_path, 'w') as file:
                    file.writelines(updated_lines)
                file.close()
                # Modify calc vcxprofj file
                with open(calc_file_path, 'r') as cfile:
                    clines = cfile.readlines()
                cupdated_lines = [cline.replace(old_filename, new_calc_packageConfig_filename) for cline in clines]
                with open(calc_file_path, 'w') as cfile:
                    cfile.writelines(cupdated_lines)
                cfile.close()
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText(f"Modified {file_path} and {calc_file_path} successfully")
                msg.setWindowTitle("Info")
                msg.exec()
            except:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText(f"Error renaming packages.config file:")
                msg.setWindowTitle("Error")
                msg.exec()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Please select the correct vcxproj file ")
            msg.setWindowTitle("Invalid vcxproj file")
            msg.exec()
    
    def AddtoSln(self):
        if self.le_vcxprojFileName.text() and self.le_testvcxprojPath.text():
            # Read the solution file
            # solution_path = self.le_slnPath.text()
            input_string = self.le_vcxprojFileName.text()
            sln_fileName = input_string.replace("CLC.vcxproj", ".sln")
            source_path = self.le_vcxprojPath.text()
            calc_dir = os.path.dirname(source_path)
            sln_dir = os.path.dirname(calc_dir) + "/" + sln_fileName
            project_path = self.le_testvcxprojPath.text()
            with open(sln_dir, 'r') as solution_file:
                solution_content = solution_file.read()
                
            # Check if the project is already added to the solution
            if project_path in solution_content:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText(f"The project '{project_path}' is already added to the solution.")
                msg.setWindowTitle("Info")
                msg.exec()
                print(f"The project '{project_path}' is already added to the solution.")
                return
            
            # Get the solution directory
            solution_dir = os.path.dirname(sln_dir)
            
            # Get the relative path of the project
            relative_project_path = os.path.relpath(project_path, solution_dir)
            
            # Construct the project entry to be added to the solution
            project_entry = f'Project("{{{os.urandom(16).hex()}}}") = "{os.path.basename(project_path)}", "{relative_project_path}", "{{{os.urandom(16).hex()}}}"\nEndProject'
            
            # Add the project entry to the solution
            solution_content += f'\n{project_entry}\n'
            
            # Write the updated solution file
            with open(sln_dir, 'w') as solution_file:
                solution_file.write(solution_content)
            
            solution_file.close()
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(f"The project '{project_path}' has been added to the solution '{sln_fileName}'.")
            msg.setWindowTitle("Info")
            msg.exec()

        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Please select the correct sln file ")
            msg.setWindowTitle("Invalid sln file")
            msg.exec()
      
# Entry point of the application
def main():
    pass

if __name__ == '__main__':
    # main()
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())