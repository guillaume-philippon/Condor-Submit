# Condor-Tools
A set of python script to interact with HTCondor cluster

## csub
csub is a submit script. It allow user to avoid .sub file creation to submit job to HTCondor.
The simplest usage of csub it's job the name of the binary you want launch

    user@machine> csub /path/to/script

All options are available with the command --help

    user@machine> csub --help
    usage: csub [-h] [--args ARGUMENTS] [--group GROUP] [--machine MACHINE]
                [--input INPUT_FILES] [--output OUTPUT_FILES] [--cpus CPUS]
                script

    Condor submit wrapper to improve user experience

     positional arguments:
     script                /path/to/script you want run

    optional arguments:
      -h, --help            show this help message and exit
      --args ARGUMENTS      Arguments for your script
      --group GROUP         Condor group you want to use (based on Unix group)
      --machine MACHINE     Define a specific machine you want use (should be the
                            full hostname of the machine)
      --input INPUT_FILES   A list of input file
      --output OUTPUT_FILES
                            A list of output file
      --cpus CPUS           Number of CPUs you need
