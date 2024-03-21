#-----------------------------------------------------------------------
# runserver.py
# Authors: Roger Weng, Vishva Ilavelan
#-----------------------------------------------------------------------


import sys
import argparse
import server

def inputhelper():
    parser = argparse.ArgumentParser(
        description="The registrar application")
    parser.add_argument('port', type=int,
    help="the port at which the server should listen")
    args = parser.parse_args()

    return args.port
def main():
    port = inputhelper()
    try:
        server.app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(sys.argv[0] + ":", ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
