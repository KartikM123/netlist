import sys, getopt
from commands.AddCommand import AddCommand
from commands.ListCommand import ListCommand
from commands.ReadCommand import ReadCommand
from commands.PingCommand import PingCommand

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
    command = ListCommand(args, opts)
    if (target == "add"):
        command = AddCommand(args, opts)
    elif(target == "list"):
        command = ListCommand(args, opts)
    elif(target == "read"):
        command = ReadCommand(args, opts)
    elif(target == "ping"):
        command = PingCommand(args, opts)
    command.execute()
    return

if __name__ == "__main__":
    main(len(sys.argv[1:]), sys.argv[1:])