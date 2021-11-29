import sys, getopt
from commands.AddCommand import AddCommand
from commands.ListCommand import ListCommand
from commands.ReadCommand import ReadCommand
from commands.PingCommand import PingCommand
from commands.SearchCommand import SearchCommand
from commands.DcountCommand import DcountCommand
from commands.SummarizeCommand import SummarizeCommand
import shutil
import json
def testValidFile():
    with open('db/network.json', 'r+') as outfile:
        #load fileData
        try:
            file_data = json.load(outfile)
            file_data["network"]
        except:
            shutil.copy('db/template.json','db/network.json')
def main (argc, argv):
    if (argc == 0):
        print("must add option")
        return 1
    try:
        opts, args = getopt.getopt(argv, "h:i", ["--pull"])
    except:
        print("error")
        return 1
    target = args[0]
    if (target == "init"):
        target = "h"
        while(target == "h"):
            target = raw_input("What command do you want?")
            if (target == "h"):
                with open('help.md', 'r') as f:
                    print(f.read())
    testValidFile()
    command = ListCommand(args, opts, "")
    if (target == "add"):
        command = AddCommand(args, opts)
    elif(target == "list"):
        command = ListCommand(args, opts, "")
    elif(target == "read"):
        command = ReadCommand(args, opts)
    elif(target == "ping"):
        command = PingCommand(args, opts)
    elif(target == "search"):
        command = SearchCommand(args, opts, "", True, "")
    elif(target == "dcount"):
        command = DcountCommand(args, opts, "")
    elif(target == "summary"):
        command = SummarizeCommand(args,opts)
    else:
        print("No valid command detected. Check out these options! ")
        with open('help.md', 'r') as f:
            print(f.read())
        return
    command.execute()
    return

if __name__ == "__main__":
    main(len(sys.argv[1:]), sys.argv[1:])