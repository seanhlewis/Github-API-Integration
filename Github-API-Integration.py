# Simple Github API Script Integration by Sean Lewis
# Uses PyGithub

from github import Github

'''
IMPORTANT INFORMATION
Github Access Token is necessary for API Requests.
It can be found under Settings / Developer Settings / Personal Access Tokens / Fine-Grained Tokens

The token must have the following permissions:
    If you want ability to create/delete repos:
        - Set Repository Access to "All Repositories"
        - Set Permissions: Administration to "Read and Write"
    
    If you want ability to create/delete files:
        [1] For only one repo:
            - Set Repository Access to "Only Select Repositories" and select the repo you want to access
            - Set Permissions: Contents to "Read and Write"
        [2] For all repos:
            - Set Repository Access to "All Repositories"
            - Set Permissions: Contents to "Read and Write"

Once you have setup the permissions, generate the token and paste it into "ACCESS_TOKEN" below.
'''

ACCESS_TOKEN = ""

git = Github(ACCESS_TOKEN)
user = git.get_user()

print("Successfully logged in as {}".format(user.login))

print("--------------------------------------------")

print("Github user: {}".format(user.login))
print("Github user name: {}".format(user.name))
print("Github user public repos: {}".format(user.public_repos))

print("--------------------------------------------")

def createRepo():
    repo_name = input("Enter the name of the repo you want to create: ")
    repo_desc = input("Enter the description of the repo you want to create: ")
    print("Creating Repo with name", '"' + repo_name + '"', "and description", '"' + repo_desc + '"')
    user.create_repo(name=repo_name,description=repo_desc)
    print("Successfully created Repo. This repo is available at", "https://github.com/" + user.login + "/" + repo_name)

def deleteRepo():
    query = "deletion"
    while query != "":
        try:
            repo_name = input("Enter the name of the repo you want to delete: ")
            if repo_name == "":
                break
            # Double Check to make sure the user wants to delete the repo, and not just hit enter by accident-
            check = input("Are you sure you want to delete the repo named '" + repo_name + "' ? (y/n): ")
            if check == "y":
                # Triple Check to make sure the user wants to delete the repo, who knows what could happen...
                check = input("Are you REALLY sure you want to delete the repo named '" + repo_name + "' ? (y/n): ")
                if check == "y":
                    # Quadruple Check to make sure the user wants to delete the repo, are you sure you're sure that you're sure?
                    check = input("Are you REALLY REALLY sure you want to delete the repo named '" + repo_name + "' ? (y/n): ")
                    if check == "y":
                        # Quintuple Check to make sure the user wants to delete the repo, can never be too careful with deleting repos!
                        check = input("Are you REALLY REALLY REALLY sure you want to delete the repo named '" + repo_name + "' ? (y/n): ")
                        if check == "y":
                            print("Deleting Repo with name", '"' + repo_name + '"')
                            repo = user.get_repo(repo_name)
                            repo.delete()
                            print("Successfully deleted Repo.")
                            break
            if check == "n":
                break
        except Exception as e:
            print(e)

def uploadFile():
    repo_name = input("Enter the name of the repo you want to upload to: ")
    print("Uploading file to Repo with name", '"' + repo_name + '"')
    repo = user.get_repo(repo_name)
    all_files = []
    
    try:
        # Getting all files in the repo so we can see if we have to "update" or "create"
        try:
            contents = repo.get_contents("")
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    file = file_content
                    all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
        except:
            print("Repository is currently empty, creating first file")

        # Opening the file we want to upload, and reading it into Github-supported bytesarray
        with open('image.png', 'rb') as file:
            content = file.read()
            image_data = bytearray(content)
            print("File successfully opened and contents read in.")

        # Uploading the file to Github
        git_prefix = repo_name + "/"
        git_file = git_prefix + "image.png" # <--- This points to a local file with the name "image.png" located in the same directory as this script

        # Updating the file if it already exists
        if git_file in all_files:
            print("Updating a file inside", repo_name)
            contents = repo.get_contents(git_file)
            repo.update_file(contents.path, "Updated file", bytes(image_data), contents.sha, branch="master")
            print(git_file + ' UPDATED')

        # Creating the file if it doesn't exist
        else:
            print("Creating a new file inside", repo_name)
            repo.create_file(git_file, "committing files", bytes(image_data), branch="master")
            print(git_file + ' CREATED')

        print("Succesfully uploaded file to Repo. This file is available at", "https://github.com/" + user.login + "/" + repo_name + "/blob/master/" + git_file)

    except Exception as e:
        print(e)

def deleteFile():
    repo_name = input("Enter the name of the repo you want to delete from: ")
    print("Deleting file from Repo with name", '"' + repo_name + '"')
    repo = user.get_repo(repo_name)
    all_files = []
    
    try:
        # Reading all files in the repo
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file = file_content
                all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
        
        # Deleting the file from Github
        git_prefix = repo_name + "/"
        git_file = git_prefix + "image.png" # <--- This points to a local file with the name "image.png" located in the same directory as this script

        # Deleting the file if it already exists
        if git_file in all_files:
            print("Deleting a file inside", repo_name)
            contents = repo.get_contents(git_file)
            repo.delete_file(contents.path, "Deleted file", contents.sha, branch="master")
            print(git_file + ' DELETED')
            print("Succesfully deleted file from Repo.")
        
        # File does not exist, so we can't delete it
        else:
            print("File does not exist in repo")

    except Exception as e:
        print(e)

def listContents():
    repo_name = input("Enter the name of the repo you want to list the contents of: ")
    
    try:
        repo = user.get_repo(repo_name)
    except:
        if repo_name == "":
            return
        print("Please enter a valid repository")
        listContents()
        return
    print("Listing contents of Repo with name", '"' + repo_name + '"')
    all_files = []
    
    try:
        # Reading all files in the repo
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file = file_content
                all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
        
        # Listing the contents of the repo
        print("Contents of repo", '"' + repo_name + '"', "are:")
        if all_files == []:
            print("EMPTY")
        for file in all_files:
            print(file)

    except Exception as e:
        print(e)

def listRepos():
    print("Listing all repos of user", '"' + user.login + '"')
    all_repos = []
    
    try:
        # Reading all repos of the user
        for repo in user.get_repos():
            all_repos.append(repo.name)
        
        # Listing the repos of the user
        print("Repos of user", '"' + user.login + '"', "are:")
        for repo in all_repos:
            print(repo)

    except Exception as e:
        print(e)

def main():
    choice = "selection"
    while choice != "":
        choice = input("Enter the number of program to run\n[1] Create Repo\n[2] Delete Repo\n[3] Upload File to Repo\n[4] Delete File from Repo\n[5] List Contents of Repo\n[6] List Repos of User\n")
        options = {1 : createRepo, 2 : deleteRepo, 3 : uploadFile, 4 : deleteFile, 5 : listContents, 6 : listRepos}
        try:
            options[int(choice)]()
        except:
            if choice == "":
                print("Exiting program")
            else:
                print("Please enter a valid number\n")
            continue
main()