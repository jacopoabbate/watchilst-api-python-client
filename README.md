# Watchlist API Client Library for Python
## Overview

The Watchlist API Client Library for Python was designed to offer a simple and flexible access to the Intercontinental Exchange (ICE) Watchlist API. The library offers a way to programmatically interact with the Watchlist API to submit new Watchlist configuration files, and to retrieve active and deactivated configurations from the server. The functions in this package can be used to create scripts to automate the interaction with the Watchlist API, but at the same time we implemented a convenient command line interface that offers a way to interact with the API in a straightforward manner. The library is designed for Python client-application developers that need to script their interaction with the Watchlist API, but, at the same time, thanks to the CLI, the library can be used also by non-technical roles to interact with the API.

## Background

The Watchlist files are a type of data files that are part of the offering of the ICE DataVault, the cloud-based platform that is used to manage and source historical tick-by-tick data from the ICE Consolidated Feed. The Watchlist files provide tick history and pricing data for a select subset of instruments on specific markets. Instead of downloading all the data produced by a specific market source, the introduction of Watchlist files allowed users to specify a portfolio of instruments of interest for each market source, and download only the data that is needed. 

The Watchlist files are generated on a subscription basis; the users need to specify, on day *t*, the list of market sources they are interested in retrieving the data from and, for each source, the portfolio of instruments that they want to have included in the file. The preferences are specified in a *.csv* or *.txt* configuration file. Based on this configuration file, on *t+1*, a new Watchlist file for each market source is created.

All the operations that have to do with managing the creation of these files, take place on a dedicated API, what from now on we will call the Watchlist API. Through the Watchlist API users can:

- **Submit new configuration files**, in order to update the portfolio of instruments for a specific market source, include a new market source, or deactivate existing market sources.
- **Retrieve an active configuration** to check, at the moment of the API call, what list of market sources and instruments a user is submitted to.
- **Retrieve a deactivated configuration** to check, at a specific point in time, what was the active configuration.

With the Watchlist API Client Library for Python, we modelled all these interactions in a set of functions and a command line interface, to allow users to interact with the API in a convenient way either through Python scripts that leverage the functions in the library, or through the CLI, that uses the functions in the backend, and expose a simple and straightforward interface to the users.

## Features

- Submits Watchlist configuration files.
- Validates the formatting of the configuration file against the file specifications.
- Supports saving in a JSON file the summary of the actions resulting from submitting the new configuration file
- Retrieves active and deactivated Watchlist configurations.
- Saves the retrieved configuration in a csv file according to the specification of Watchlist files
- Supports the specification of the Onyx credentials used to access the Watchlist API in dedicated environment variables.

## Setup Instructions

### Requirements/Pre-requisites

#### Software Requirements

This software requires to have Python 3.6 or above installed.

#### Access Requirements

In order to operate the program you need to have an account with the Intercontinental Exchange (ICE) that gives you access to the ICE DataVault platform.

### Installation

#### Cloning the Repository

To use Watchlist API Python Client, first clone the repository on your device using the command below:

```shell
# If using the ssh endpoint
$ git clone git@github.comgit@github.com:jacopoabbate/watchilst-api-python-client.git

# If using the https endpoint
$ git clone https://github.com/jacopoabbate/watchilst-api-python-client.git

cd watchlist-api-python-client
```

This creates the directory *watchlist-api-python-client* and clones the content of the repository.

#### Installing Within a Virtualenv

We always recommend to create and use a dedicated environment when installing and running the application.

You will need to have at least Python 3.6.1 installed on your system.

##### Unix/Mac OS with virtualenv

```shell
# Create a virtual environment
# Use an ENV_DIR of your choice. We will use ~/virtualenvs/watchlist-api-client-prod
# Any parent directories should already exist
python3 -m venv ~/virtualenvs/watchlist-api-client-prod

# Activate the virtualenv
. ~/virtualenvs/watchlist-api-client-prod/bin/activate

# Install the dependencies
python -m pip install -r requirements-prod.txt

# Install watchlist-config-generator
python -m pip install .
```

At this point you should be able to import `watchlist_api_client` from your locally built version:

```shell
$ python  # start an interpreter
>>> import watchlist_api_client
>>> print(watchlist_api_client.__version__)
1.0.0
```

##### Windows

Below is brief overview on how to set-up a virtual environment with PowerShell under Windows. For further details, please refer to the [official virtualenv user guide](https://virtualenv.pypa.io/en/latest/).

```shell
# Create a virtual environment
# Use an ENV_DIR of your choice. Use %USERPROFILE% fro cmd.exe
python -m venv $env:USERPROFILE\virtualenvs\watchlist-api-client-prod

# Activate the virtualenv. User activate.bat for cmd.exe
~\virtualenvs\watchlist-api-client-prod\Scripts\Activate.ps1

# Install the package dependencies
python -m pip install -r requirements-prod.txt

# Install watchlist-config-generator
python -m pip install .
```

## Usage

After installing the Watchlist API Client Library for Python, you can decide whether you use the functions in the library to write Python scripts, or you can interact with the Watchlist API via the CLI provided by the package.

In the following section, we will document the usage of the command line interface.

### The `watchlist` Command

When installing the Watchlist API Client Library, a `setuptools` script generates executable wrappers that make possible to directly call the `watchlist` command from your terminal or command prompt. If working on Unix, the `watchlist` command can be called without the need of activating the virtual environment in which the package was originally installed; in Windows, on the other hand, the first step to use the `watchlist` command is to activate the virtual environment.

The `watchlist` help prompt can be invoked by running:

```shell
watchlist --help
```

 This will return:

```
Usage: watchlist [OPTIONS] COMMAND [ARGS]...

  watchlist is a tool to interact with the Watchlist API.

Options:
  --help  Show this message and exit.

Commands:
  retrieve  Retrieves a Watchlist API configuration.
  submit    Submits a configuration file to the Watchlist API server.
```

 As shown by the help prompt, the `watchlist` command groups two other sub-commands:

- The `retrieve` command, that is used to retrieve an active or deactivated Watchlist configuration.
- The  `submit` command, that is used to submit a new configuration file.

### Using the `submit` Command

The `submit` command is invoked by running:

```shell
watchlist submit CONFIG_FILE [OPTIONS]
```

where `CONFIG_FILE` is the full path to the Watchlist API configuration file location.

The `submit` command accepts the following options:

- `-u` or `--username` to specify the Onyx username used to access the Watchlist API.
- `-p` or `--password` to specify the Onyx password used to access the Watchlist API.
- `-q` or `--quiet` to mute the output of the command (in this case, upon completion of the submission of the configuration file, the command will return an exit code 0 without showing the summary of the action resulting from submitting the new configuration file to the Watchlist server).
- `--json` to save the summary of the actions resulting from submitting the new configuration file to the Watchlist server to a JSON file.
- `-w` or `--write-to` to specify the path to the location where the JSON file containing the request summary is to be saved. This option is normally used in combination with `--json`, however it can also be omitted and, in that case, the JSON file will be written in the current working directory.

An example of a typical usage of the `submit` command is the following:

```shell
watchlist submit ~/configurations/watchlist_config_20201125.csv -u user -p pwd 
```

This will return, in case of a successful submission of the configuration file, a human readable version of the summary of the actions performed as a result of the submission of the configuration file. An example of this output is:

```shell
Wed, 25 Nov 2020 14:24:11 GMT

Actions performed as a result of the request:
  - 2 new sources have been activated
  - 2 existing sources have been updated
  - 2 sources have failed
  - 2 existing sources have been deactivated
  
The following sources have been activated: 676, 680
The following sources have been updated: 207, 673
The following sources have failed: 596, 686
The following sources have been deactivated: 684, 748
```

The  output will depend on the content of the configuration file submitted, and on the user's account entitlements.

Alternatively, the same command run with the `--json` option:

```shell
watchlist submit ~/configurations/watchlist_config_20201125.csv -u user -p pwd --json
```

will create a JSON file with the content structured as follows:

```json
{
  "nbCreated": 2,
  "nbUpdated": 2,
  "nbFailed": 2,
  "nbDeactivated": 2,
  "created": ["676", "680"],
  "updated": ["207", "673"],
  "failed": ["596", "686"],
  "deactivated": ["684", "748"]
}
```

### Using the `retrieve` Command

The `retrieve` command is invoked by running:

```shell
watchlist retrieve [OPTIONS]
```

The `submit` command accepts the following options:

- `-u` or `--username` to specify the Onyx username used to access the Watchlist API.
- `-p` or `--password` to specify the Onyx password used to access the Watchlist API.
- `-t`  or `--timestamp` to specify a UTC date and time expressed according the ISO 8601 standard (*YYYY-MM-DDThh:m​m:ssZ*). This command is used whenever the user wants to retrieve a deactivated configuration.
- `-w` or `--write-to` to specify the path to the location where the csv file containing the retrieved configuration is to be saved. If omitted, the csv file will be written in the current working directory.

An example of a typical usage of the `retrieve` command is the following:

```shell
watchlist retrieve -u user -p pwd 
```

Since no `--timesamp` option is used, the `retrieve` command will return the active configuration at the time of the API call. In this case, not having used the `-w` option, the retrieved configuration will be written in the current working directory. The file produced at the end of the retrieval operation is structured according to the specifics of the Watchlist configuration files. An example of one such a file is the following:

```
sourceId,RTSsymbol
207,F:FDAX\H21
207,F:FDAX\Z20
207,F:FESX\Z20
```

To retrieve the active configuration on the 24th of November 2020 at 16:30, we would run:

```shell
watchlist retrieve -u user -p pwd -t 2020-11-24T16:30:00Z
```

If a configuration was active on the date passed with the `--timestamp` option, the `retrieve` function will save the retrieved configuration according to the previously shown format. If, instead, no active configuration is found, will inform that the server returned a 404 status code and will inform the user that the error code corresponds to a missing configuration for the date and time passed, before exiting the program with a status code 1.

### Using Environment Variables to Configure Access Credentials 

In alternative to passing every time that a command is run, the credentials to access the Watchlist API through the `--username` and `--password` options, the CLI of the Watchlist API Client Library allows for credentials to be stored as environment variables.  

The Watchlist API Client library supports the following environment variables:

- `ICE_API_USERNAME`: specifies the username used to access the Watchlist API.
- `ICE_API_PASSWORD`: specifies the password used to access the Watchlist API.

#### Setting Access Credentials as Environment Variables in Windows

If the Windows command prompt is used, the environment variables are set as follows:

```shell
C:\> setx ICE_API_USERNAME <your-username>
C:\> setx ICE_API_PASSWORD <your-password>
```

Using `setx` to set the environment variables, changes the value used in both the current command prompt session and all command prompt sessions that you create <u>after</u> running the command. It does not affect other command shells that are already running at the time you run the command. Alternatively, if you want to affect only the current command prompt session, you can use the `set` command instead of `setx`.

Alternatively, you can set the environment variables through PowerShell as:

```powershell
PS C:\> $Env:ICE_API_USERNAME="<your-username>"
PS C:\> $Env:ICE_API_PASSWORD="<your-password>"
```

This will save the value only for the duration of the current session. To set the variables such that they are accessible to all the future PowerShell sessions, you can add them to your PowerShell profile as explained in the [PowerShell documentation](https://docs.microsoft.com/en-gb/powershell/module/microsoft.powershell.core/about/about_environment_variables?view=powershell-7.1).

Finally, to make the environment variable setting persistent across all Command Prompt and PowerShell sessions, you can store them by using the System application in the Control Panel.

#### Setting Access Credentials as Environment Variables in Linux or macOS

To set the environment variables in Linus or macOS, you can run:

```shell
$ export ICE_API_USERNAME=<your-username>
$ export ICE_API_PASSWORD=<your-password>
```

By setting the environment variables in this way, the two environment variables will be persisted until the end of the shell session, or until the variables are set to a different value.

To persist the environment variables across future sessions, simply set them in the shell's start-up script.

## License

Copyright (c) Jacopo Abbate

Distributed under the terms of the MIT license, Watchlist API Python Client is free and open source software.

## Credits

Watchlist API Client Library for Python is developed and maintained by [Jacopo Abbate](mailto:jacopo.abbate@gmail.com "jacopo.abbate@gmail.com").
