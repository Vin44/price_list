# Price Data Pipe Line

This project is a automated system that extract the price data for vegetables, fruits, rice and fish in economic centers from PDF documents published by CBSL (Central Bank Sri Lanka) and loads those data to a SQL database. 

## Project Structure

*  `main.py` : This is the entry point for the system. This orchestrates the scraping adn downloading the PDFs, extracting data and inserting those in to the SQL database.

*  `webscrp.py` : Contains functions that scrape the CBSL website and downloads the PDFs after identifying the PDF urls.

* `lst.py` : Handles the extraction of tabular data from the downloaded PDFs. Creating different lists of dataframes for each categories (vegeteables, rice, fruits, fish, ...).

* `write_sql.py` : Manages the connection with the SQL database and insert the processed data to the relative table. 

* `dockerfile` : Defines the docker image for containerizing the system. 

* `.env` : This file stores the environment variables, like the SQL database Connection string. 

## Execution

### **Local Setup**

You can run this programme locally. Follow these steps:

#### Prerequisities
* Python 3.11
* Python Package Installer (`pip`)
* SQL Server or compatible database
* ODBC Driver for SQL Server

#### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_name>
```
#### 2. Install the Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

Create a new `.env` file in the root directory of the project and add your SQL server connection string:
```
CONNECTION_STRING=DRIVER={ODBC Driver 18 for SQL Server};
    SERVER=<your_server_name>;
    DATABASE=<your_database_name>;
    UID=<your_username>;
    PWD=<your_password>;
    Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;

```

#### 4. Run the Pipeline
Execute the `main.py`:
```bash
python main.py
```
This will perform the following actions:
1. **Download PDFs** - Scrape the CBSL webstie and download the PDFs to the `data` directory.
2. **Process Data** - Readd the downloaded PDFs, extract data for Vegetables, Fish, Rice, ... and convert them in to DataFrames.
3. **Insert into SQL Database** - Connect with you SQL database and writes the processed data in to the relevent tables.

### **Automation With Azure Cloud**
This Project can be automated with the Azure Container Instances (ACI) by containarize the system with Docker and scheduling it's execution.

#### Prerequisities for Azure Deployment

* Azure Subscription
* Docker Desktop

#### 1. Push Docker Image To the Azure Container Registry (ACR) using GitHub

The Docker image is built and pushed to Azure Container Registry using a GitHub Actions workflow defined in `docker-publish 1.yml`.

First update the `docker-publish 1.yml`.

![alt text](<photos/Screenshot 2025-06-09 112622.png>)

Here, in the line 13 the `login-server` is your ACR. You have to update it and do the same thing with the line 20. Also change the `pricelist1:v1` with name what you want for your docker image.

Then in the repo settings under Secrets and Variables add repository secrets, `REGISTRY_USERNAME` and `REGISTRY_USERNAME`.

Those two must obtain the username and password from the Access Key section of the ACR. (ACR > 'your-registry' > Settings > Access Keys)

Then push to the repo and in the Actions section of the repository run the workflow.

![alt text](<photos/Screenshot 2025-06-09 142602.png>)

This performs the following steps:  
1. **Chekout Code:** Checks the content of the repository.
2. **Azure Login:** Logs into the Azure Container Registry using provided GitHub Secrets for username and password.
3. **Build and Tage Image:** Builds the Docker image from the dockerfile and tags it as what you typed as the `IMAGE_TAG` in the `docker-publish 1.yml`.
4. **Push Image:** Pushes the tagged Docker image to `vinprice.azurecr.io`.



#### 2. Deploy and Schedule with Azure Functions and Azure Container Instances (ACI)

The containerized application is running on Azure Container Instances, and its execution is managed and scheduled by an Azure Function.

1. **Edit `execute_containers.py`:** Update the `containers_to_monitor` array within the `execute_containers.py` file to specify the container instances you want to manage. 

2. **Create Azure Functions Resource:** Create an Azure Functions resource in the Azure Portal. After creation, add the environmental variables `AZURE_SUBSCRIPTION_ID` and `RESOURCE_GROUP_NAME`. The `SCM_DO_BUILD_DURING_DEPLOYMENT` key is not needed.

3. **Create Azure Functions App with VS Code:** Create an Azure Functions app project using VS Code. Add the `execute_containers.py` file to that project directory.

4. **Consider UTC for Timer Trigger:** Remember to account for UTC when configuring the timer trigger for your Azure Function.

5. **Deploy using VS Code:** Deploy your Azure Function app using VS Code.

You can download the `execute_containers.py` [<u>here.</u>](https://github.com/Vin44/ACI_EX)