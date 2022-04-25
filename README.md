# Entity Extraction

## Table of Contents 
1. [Overview](#overview)
2. [Get Code](#getcode)
3. [Google Credentials Setup](#googlecredsetup)
4. [Application Setup](#appsetup)
    1. [Manually Setup](#setup)
    2. [Automatic Setup](#setupbymakefile)
5. [Application Setup via Docker Container](#appsetupdocker)
    1. [Manually Setup](#docker)
    2. [Automatic Setup](#dockersetupbymakefile)
6. [Setup and run via PyInvoke](#pyinvoke)
7. [Example Usage](#example)

<a name="overview"></a>

## Overview

Entity Extraction is designed to fetch the desired fields from the uploaded documents using Google DLP and Google Vision. Following attributes which are present in the documents uploaded are extracted from it: Complete Name, First Name, Last Name, Street Address and Email Address.

<br>
<a name="getcode"></a>

## Get Code

  You can get code from GitHub with this link: https://github.com/naveentechnolive10/entity-extraction
  Either by download zip file or by run following command on your terminal:
    ```
      git clone https://github.com/naveentechnolive10/entity-extraction.git
    ```

<a name="googlecredsetup"></a>

## Google Credentials Setup

  ### - Setup `google_cred.json` file
    You can get/create `google_cred.json` by following procedure: https://cloud.google.com/docs/authentication/getting-started

    Note: Put your `google_cred.json` into your root directory of application ex.```entity-extration```. 
    Once you get `google_cred.json` then either copy below command to your `~/.bash_profile` and run `source ~/.bash_profile` or just run below command on terminal. 
    
    You'll need to run this command on your OS terminal:
      ```
        export GOOGLE_APPLICATION_CREDENTIALS="<path of your google_cred.json>"
      ```
    You can verify by run this command on your OS terminal for MacOS/Linux users:
      ```
        echo $GOOGLE_APPLICATION_CREDENTIALS
      ```
    You can verify by run this command on your OS terminal for Windows users:
      ```
        echo %GOOGLE_APPLICATION_CREDENTIALS%
      ```
    Above will show absolute path of you `google_cred.json` file if not follow above procedure again.
  
  ### - Google Project-ID Setup
    
    Do it by modifying your `src/settings.py`.
    You can get/create `GOOGLE_PROJECT_ID` by following procedure: https://cloud.google.com/resource-manager/docs/creating-managing-projects
    
    You'll need to set the following:
      ```src/settings.py
      GOOGLE_PROJECT_ID: str = "<project_id>"
      ```
  ### - Enable Google DLP API
    
    Before using API you must enable it by following: https://console.cloud.google.com/apis/api/dlp.googleapis.com

<br>
<a name="appsetup"></a>

## Application Setup
**Note: During setup/run application we recommend to use Python 3.7.4 version.
  <a name="setup"></a>

  ### - Setup by manually
    1. Create a virtual environment by command:  ```python3 -m venv venv```
    2. Activate the virtual env: ```source venv/bin/activate```. For Windows user: ```venv\Scripts\activate.bat```.
    3. Install python packages by command: ```pip --no-cache-dir install -r requirements.txt```

  <a name="setupbymakefile"></a>

  ### - Setup and run by Makefile

    Before run below commands make sure you did set GOOGLE_APPLICATION_CREDENTIALS variable in .bash_profile file.
    - For complete setup and run application: ```make local_make```.

Note: If make utility is not supporting by your Operating System (Windows) then install/setup and run application by [PyInvoke](#pyinvoke) as mentioned below.

<a name="appsetupdocker"></a>

## Application Setup via Docker Container

  <a name="docker"></a>

  ### - Manually Setup
    1. Run `docker build -t entity-extraction` from the project's root directory to
    build the docker image
    2. Run `docker run -d -p 5000:5000 --env-file .env entity-extraction` to run the docker image. To run
    in the background add `-d` 

  <a name="dockersetupbymakefile"></a>

  ### - Setup and run by Makefile
    Before run below commands make sure you did set GOOGLE_APPLICATION_CREDENTIALS variable in .bash_profile file.
    - For complete setup, build image and run: ```make local_make_docker```. 
    - For setup only: ```make docker_install```.
    - For building docker image only: ```make docker_build```.
    - For running container only: ```make local_docker_run```.

<a name="pyinvoke"></a>

## Application Setup via PyInvoke
  All the setup for the service can also be done via PyInvoke. There are multiple tasks 
  that have been added for the setup and development.

  - To start using PyInvoke, firstly it needs to be installed inside the virtual env. follow the steps 
    below for installation
    1. Create a virtual environment by command:  ```python3 -m venv venv```
    2. Activate the virtual env: ```source venv/bin/activate```. For Windows user: ```venv\Scripts\activate.bat```.
    3. Install PyInvoke via pip. ```pip install invoke```.
    4. For complete setup and run application: ```invoke local-dev```.

    
  - After the installation below commands can be used to list and invoke any tasks.
    1. List all the tasks/commands. ```invoke --list```
    2. Help regarding any command. ``` invoke <command> --help```
    3. To run any task. ``` invoke <command>  --<options>=value```

## Example screenshot

![plot](./templates/Image1.png)

