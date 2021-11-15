import sys, getopt
from commands.AddCommand import AddCommand

def main (argc, argv):
    if (argc == 0):
        print("must add option")
        return 1
    try:
        opts, args = getopt.getopt(argv, "h:i", ["--pull"])
    except:
        print("error")
        return 1
    if (args[0] == "add"):
        command = AddCommand(args, opts)
        command.execute()
    return

if __name__ == "__main__":
    main(len(sys.argv[1:]), sys.argv[1:])