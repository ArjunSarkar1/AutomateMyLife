from files import organizePath, fileTypes
import shutil
import os

def organizeDirectory():
    for file in os.listdir(organizePath):
        currFilePath = os.path.join(organizePath, file)
        
        if os.path.isfile(currFilePath):
            fileExtension = os.path.splitext(file)[1].lower()
            for folder, extensions in fileTypes.items():
                if fileExtension in extensions:
                    destFolder = os.path.join(organizePath, folder)
                    
                    os.makedirs(destFolder, exist_ok=True)
                    
                    destPath = os.path.join(destFolder, file)
                    shutil.move(currFilePath, destPath)
    
        # List directories in organizePath and sort them by name
    allDirs = [d for d in os.listdir(organizePath) if os.path.isdir(os.path.join(organizePath, d))]
    
    # Sort the directories alphabetically
    allDirs.sort()

def sortDirectory(currDir):
#     for dir in fileTypes.keys():
    folderPath = os.path.join(currDir)
    print(folderPath)
    if os.path.exists(folderPath):
        currDirFiles = []
        # print(os.listdir(folderPath))
        for file in os.listdir(folderPath):
            currFilePath = os.path.join(folderPath, file)
            print(currFilePath)
            if os.path.isfile(currFilePath):
                # print(file)
                currDirFiles.append(file)

        currDirFiles.sort()
                # Now rename files to enforce the order (or move them to another directory)
        for index, file in enumerate(currDirFiles):
            src = os.path.join(folderPath, file)
            # Generate new name to reflect sorted order (optional)
            new_name = f"{index+1}_{file}"  # Adding index number for order
            dst = os.path.join(folderPath, new_name)
            shutil.move(src, dst)  # Rename to enforce order

            print(f"Renamed {file} to {new_name}")

def filesOutDirectory(currDir):
    if not os.path.exists(currDir):
        print(f"Directory: {currDir} doesn't exist")
        return

    outFiles = []
    for file in os.listdir(currDir):
        currFilePath = os.path.join(currDir, file)
        if os.path.isfile(currFilePath):
            outFiles.append(file)

    outerDir = os.path.dirname(currDir)

    for file in outFiles:
        shutil.move(os.path.join(currDir, file), os.path.join(outerDir, file))

def moveFilesOut():
    for dir in fileTypes.keys():
        folderPath = os.path.join(organizePath, dir)
        if os.path.exists(folderPath):
            print(folderPath)
            filesOutDirectory(folderPath)
    
    removeEmptyDirectories(organizePath)
    
def removeEmptyDirectories(currDir):
    for dir in fileTypes.keys():
        folderPath = os.path.join(currDir, dir)
        if os.path.exists(folderPath) and not os.listdir(folderPath):
            os.rmdir(folderPath)

# organizeDirectory()
# sortDirectory(organizePath)
# moveFilesOut()