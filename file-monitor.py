import os,hashlib,json

def snapshot(abs_directory:str):
    snapshot_data = {}
    files_no = 0

    #use os.walk() to get dirpaths and files, makes hashes for each file and stores in snapshot_data
    for dirpath,dirs,files in os.walk(abs_directory):
         if files:
            for filename in files:
                with open(f'{dirpath}/{filename}', 'rb') as file:
                    file_hash = hashlib.sha256(file.read()).hexdigest()
                    snapshot_data[f'{dirpath}/{filename}'] = file_hash
                    files_no += 1
                    
    return snapshot_data, files_no

def assign():
    while True:
        directory = input('Enter directory name to monitor: ') #directory input
        abs_directory = os.path.abspath(directory) # turning it into absolute directory

        if os.path.isdir(abs_directory): #check if it is a valid directory
            snapshot_data,scanned_files_no = snapshot(abs_directory)
            json_data = {'monitored_directory':abs_directory, 'data': snapshot_data}


            snapshot_file = f"{os.path.basename(abs_directory)}-snapshot.json"

            #check if there was previous snapshot saved
            prev_snapshot_check = os.path.exists(snapshot_file)


            #write all data to snapshot.json            
            with open(snapshot_file,'wt') as file:
                json.dump(json_data,file)


            #print output
            print('========== DIRECTORY ASSIGNMENT ==========\n')  
            print(f'Monitoring Directory:\n{abs_directory}\n\nFiles Scanned: {scanned_files_no}\n')
            if prev_snapshot_check:
                print('Previous snapshot found. Snapshot updated successfully')
            else:
                print('No previous snapshot found.')
            print('Future scans will compare against this snapshot')
            break
        else:
            print('Directory does not exist.Please try again')           
        
def compare():
    while True:
        directory = input('Which assigned directory would you like to compare?: ')
        try:
            abs_directory = ''
            old_snapshot_data = {}
            snapshot_file = f'{os.path.basename(directory)}-snapshot.json'
            with open(snapshot_file) as file:
                try:
                    json_data = json.load(file)
                    abs_directory =json_data["monitored_directory"]
                    old_snapshot_data = json_data["data"]
                except(json.JSONDecodeError):
                    print("Snapshot corrupted")
                    break
            new_snapshot_data,new_snapshot_file_no = snapshot(abs_directory)
            new_filepaths = new_snapshot_data.keys()
            old_filepaths = old_snapshot_data.keys()
            modified = []
            added = []
            deleted = []
            #Modified = filepath is same; hash is not same
            #Added = filepath not there before; is now
            #Deleted = filepath there before; is not now
            for i in new_filepaths:
                if i in old_filepaths:
                    if new_snapshot_data[i] != old_snapshot_data[i]:
                        modified.append(os.path.basename(i))
                else:
                    added.append(os.path.basename(i))
            for i in old_filepaths:
                if i not in new_filepaths:
                    deleted.append(os.path.basename(i))
            print(f'========== SCAN RESULTS ==========\n\nMonitoring Directory:\n{abs_directory}\n\nFiles Scanned: {new_snapshot_file_no}\n\n')
            print('========== ADDED FILES ==========\n')
            if len(added):
                for i in added:
                    print(i)
            else:
                print('No added files')
            print('\n\n========== DELETED FILES ==========\n')
            if len(deleted):
                for i in deleted:
                    print(i)
            else:
                print('No deleted files')
            print('\n\n========== MODIFIED FILES ==========\n')
            if len(modified):
                for i in modified:
                    print(i)
            else:
                print('No modified files')
            print('\n\n========== SUMMARY ==========\n')
            print(f'Added:    {len(added)}\nDeleted:  {len(deleted)}\nModified: {len(modified)}\n\n')
            if len(added) or len(modified) or len(deleted):
                print('Status: WARNING - File changes detected.')
            else:
                print('Status: No changes detected.\n')
            print('Scan Complete.')
            break
        except(FileNotFoundError):
            print('Entered directory does not exist or is not currently being monitored. Please try again.')

print('========== FILE INTEGRITY MONITOR ==========\n')
while True:
    print('Choose action:\n1.Assign directory to monitor/update snapshot\n2.Compare an assigned directory to last snapshot')
    choice = input('Your choice: ')
    if choice == '1':
        assign()
        break
    elif choice == '2':
        compare()
        break
    else:
        print('Invalid choice. Please try again.')