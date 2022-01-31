# Importing all required modules
import os
import sys
from tkinter import *
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class WorkSpace:
    def __init__(self):
        # Base App
        self.root = Tk()
        # App Title
        self.root.title("WorkSpace Automater")
        # Set the window to unmaximisable
        self.root.resizable(False, False)

        # App dimensiosn and screen dimesnions
        self.app_width, self.app_height = 455, 300
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(
        ), self.root.winfo_screenheight()

        # Set app geometry
        self.root.geometry(
            f"{self.app_width}x{self.app_height}+{(self.screen_width-self.app_width)//2}+{(self.screen_height-self.app_height)//2}")

        # Set app heading
        self.heading = Label(self.root, text="WorkSpace Automater")
        self.heading.config(font=("Segoe UI", 24))
        self.heading.pack()

        # Set app username
        self.usernameLabel = Label(
            self.root, text="Github Username", font=("Courier", 10, "bold"))
        self.username = Entry(self.root, width=40)
        self.usernameLabel.place(x=30, y=67)
        self.username.place(x=160, y=70)

        # Set app password
        self.passwordLabel = Label(
            self.root, text="Github Password", font=("Courier", 10, "bold"))
        self.password = Entry(self.root, width=40, show='*')
        self.passwordLabel.place(x=30, y=107)
        self.password.place(x=160, y=110)

        # Set app repository
        self.repoLabel = Label(
            self.root, text="Repository Name", font=("Courier", 10, "bold"))
        self.repo = Entry(self.root, width=40)
        self.repoLabel.place(x=30, y=147)
        self.repo.place(x=160, y=150)

        # Set app path
        self.pathLabel = Label(
            self.root, text="Folder Path", font=("Courier", 10, "bold"))
        self.path = Entry(self.root, width=35)
        self.pathLabel.place(x=30, y=187)
        self.path.place(x=130, y=190)

        # Get destination folder
        self.folderSelect = Button(
            self.root, text="Choose Folder", command=self.select)
        self.folderSelect.place(x=350, y=187)

        # Create enter button
        self.button = Button(self.root, text="Enter", command=self.Automate)
        self.button.place(x=self.app_width//2-20, y=225)

        # Set app copyright
        self.copyright = Label(self.root, text="Copyright-2022 by Hardik Jaiswal",
                               font=("Times New Roman", 10, "italic"), relief=SUNKEN)
        self.copyright.place(x=130, y=270)

    def Automate(self):
        # Get values from all text inputs
        self.usrname = self.username.get()
        self.passw = self.password.get()
        self.repoName = self.repo.get()
        self.folderpath = self.path.get()

        # Set driver and go to github.com
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.get("https://www.github.com")

        # Click login
        loginElem = self.driver.find_element(
            By.XPATH, '/html/body/div[1]/header/div/div[2]/div[2]/div[2]/a')
        loginElem.click()

        # Enter username
        usernameElem = self.driver.find_element(By.XPATH,
                                                '//*[@id="login_field"]')
        usernameElem.send_keys(self.usrname)

        # Enter password
        passwordElem = self.driver.find_element(
            By.XPATH, '//*[@id="password"]')
        passwordElem.send_keys(self.passw)

        # Click login again
        loginButton = self.driver.find_element(By.XPATH,
                                               '//*[@id="login"]/div[4]/form/div/input[12]')
        loginButton.click()

        # Wait for 6 sec
        self.driver.implicitly_wait(6)

        # Click on new repository
        newButton = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '//*[@id="repos-container"]/h2/a')))
        newButton.click()

        # Enter the repository name
        repositoryName = self.driver.find_element(
            By.XPATH, '//*[@id="repository_name"]')
        repositoryName.send_keys(self.repoName)

        # Wait for 6 sec again
        self.driver.implicitly_wait(6)

        # Click on enabled create button
        createButton = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '//*[@id="new_repository"]/div[4]/button')))
        createButton.click()

        # Copy the remote file origin url
        copyButton = self.driver.find_element(
            By.XPATH, '//*[@id="repo-content-pjax-container"]/git-clone-help/div[1]/div/div[4]/div/span/span/clipboard-copy')
        copyButton.click()

        # Get the remote origin file url
        self.remoteFile = self.root.clipboard_get()

        # Push the code to github
        os.mkdir(f"{self.folderpath}/{self.repoName}")
        os.chdir(f"{self.folderpath}/{self.repoName}")
        os.system(f'echo # {self.repoName} >> README.md')
        os.system("git init")
        os.system('git add README.md')
        os.system('git commit -m "first commit"')
        os.system('git branch -M main')
        os.system(f'git remote add origin {self.remoteFile}')
        os.system('git push -u origin main')

        # Refresh the repository
        refreshButton = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
            (By.XPATH, '//*[@id="repository-container-header"]/div[1]/div/h1/strong/a')))
        refreshButton.click()

        # Open VS Code
        os.system('code .')

        # Exit program
        sys.exit()

    def select(self):
        # Ask for directory
        folder_path = filedialog.askdirectory()
        self.path.delete(0, END)
        self.path.insert(0, folder_path)

    def run(self):
        # run the app
        self.root.mainloop()


if __name__ == '__main__':
    # Run the app finally
    WorkSpace().run()
