## Preqrequisites

Install azure cli:

```bash
brew update && brew install azure-cli
```

Login to azure:

```bash
az login
```

Install azure functions core tools:

```bash
brew tap azure/functions
brew install azure-functions-core-tools@4
```


## Image Background Remover
### Create a function app
Create a new function app using the Azure Functions Core Tools:
```bash
func init serverless-coursework --python
```

### Develop Image Background Remover function & test it locally
1. Create a new function - Here, we are creating a new function with the name `image_bg_remover` using the `HTTP trigger` template
    ```bash
    func new --name image_bg_remover --template "HTTP trigger"
    ```

    > We will use the same command to create new functions for the rest of the functions in the app. There are different kind of triggers available for creating new functions. For example, `Blob trigger`, `Queue trigger`, `Timer trigger`, etc. Refer [this article](https://www.educative.io/answers/what-are-function-triggers-in-azure)

2. Modify the `image_bg_remover` function in `function_app.py` to include the code for removing the background from an image.

3. Create a new virtual environment and install the necessary dependencies:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

    > The `requirements.txt` file should include the necessary dependencies for the function.

4. Run the function locally using the following command:
    ```bash
    # activate the virtual environment
    source .venv/bin/activate
    
    # start the function app
    func host start
    ```

5. Test the function using `curl` or any other HTTP client:
    ```bash
    curl --location 'http://localhost:7071/api/image_bg_remover' \
        --header 'Content-Type: application/json' \
        --data '{
            "url": "https://imgur.com/Dve9nqu.png"
        }' --output output.png
    ```
    Note: The `output.png` file will be saved in the current directory. Open the file to see the output of the function.

### Deploy the app function to Azure
1. Create a resource group in the UK South region (London):
    ```bash
    az group create --name "serverless-coursework" --location "uksouth"
    ```

2. Create a storage account in the resource group:
    ```bash
    az storage account create --name "serverlesscoursework" --resource-group "serverless-coursework" --location "uksouth" --sku "Standard_LRS"
    ```
    > The storage account will be created with the name `serverless-coursework` in the UK South region.

3. Create an Azure Function App in Azure. You have to provide a globally unique function app name.
    ```bash
    az functionapp create --name "serverless-coursework-assignment" --os-type "Linux" --consumption-plan-location "uksouth" --runtime "python" --functions-version 4 --resource-group "serverless-coursework" --storage-account "serverlesscoursework"
    ```
    > We are creating a python runtime with linux os in the UK South region. Note that we are providing the storage account & resource group that we created earlier.

4. Publish the function app to Azure:
    ```bash
    func azure functionapp publish "serverless-coursework-assignment"
    ```
    > This command will publish the function app to the Azure cloud. Whenever you make changes to the function app, you can run this command to publish the changes to the cloud.

5. [Optional] In this case we have a secret key that we need to use in the function app. We can set the secret key using the following command:
    ```bash
    az functionapp config appsettings set --name "serverless-coursework-assignment" --resource-group "serverless-coursework" --settings "REMOVE_BG_API_KEY=your-secret-key"
    ```

    > The `REMOVE_BG_API_KEY` is the name of the environment variable that we want to set. Replace `your-secret-key` with the actual secret key.


### Testing the Image Background Remover function in Azure
1. 🚨 Fetch the functions key to invoke it remotely
    ```bash
    az functionapp keys list --name "serverless-coursework-assignment" --resource-group "serverless-coursework" | jq -r '.functionKeys.default'
    ```

2. Make a request to the function app using the function key:
    ```bash
    curl --location 'https://serverless-coursework-assignment.azurewebsites.net/api/image_bg_remover' \
        --header 'Content-Type: application/json' \
        --header 'x-functions-key: <function-key>' \
        --data-raw '{
            "url": "https://imgur.com/Dve9nqu.png"
        }' --output output.png
    ```
    > Replace `<function-key>` with the actual function key that you fetched in the previous step.

    The `output.png` file will be saved in the current directory. Open the file to see the output of the function.


## QR Code Generator
1. Create a new function
    ```bash
    func new --name generate_qr_code --template "HTTP trigger"
    ```

2. Modify the `generate_qr_code` function in `function_app.py` to include the code for generating a QR code.

3. Test the function using `curl` or any other HTTP client:
    ```bash
    curl --location 'http://localhost:7071/api/generate_qr_code' \
            --header 'Content-Type: application/json' \
            --data '{
                "url": "https://www.leeds.ac.uk/"
            }' --output qr.png
    ```
    Note: The `qr.png` file will be saved in the current directory. Open the file to see the output of the function.

4. Deploy the function app to Azure:
   ```bash
    func azure functionapp publish "serverless-coursework-assignment"
    ```

5. Test the function in Azure:
   1. Fetch the function key:
        ```bash
        az functionapp keys list --name "serverless-coursework-assignment" --resource-group "serverless-coursework" | jq -r '.functionKeys.default'
        ```
    2. Make a request to the function app using the function key:
        ```bash
        curl --location 'https://serverless-coursework-assignment.azurewebsites.net/api/generate_qr_code' \
            --header 'Content-Type: application/json' \
            --header 'x-functions-key: <function-key>' \
            --data-raw '{
                "url": "https://www.leeds.ac.uk/"
            }' --output qr.png
        ```
        > 🚨 Replace `<function-key>` with the actual function key that you fetched in the previous step 🚨

## Cleanup
1. Delete the resource group:
    ```bash
    az group delete --name "serverless-coursework" --yes --no-wait
    ```

    > The `--no-wait` flag will not wait for the operation to complete. The `--yes` flag will not prompt for confirmation.

2. Delete the storage account:
    ```bash
    az storage account delete --name "serverlesscoursework" --resource-group "serverless-coursework" --yes
    ```

    > The `--yes` flag will not prompt for confirmation.

3. Delete the function app:
    ```bash
    az functionapp delete --name "serverless-coursework-assignment" --resource-group "serverless-coursework" --yes
    ```

    > The `--yes` flag will not prompt for confirmation.

## Docs
[Quickstart: Create a Python function in Azure from the command line](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python)

This quickstart contains the steps to create a new function app, develop a function, and deploy it to Azure.
   

## Relevant Papers
1. [A Literature Review on Serverless Computing](https://ar5iv.labs.arxiv.org/html/2206.12275v4)
2. [Survey on Serverless Computing](https://journalofcloudcomputing.springeropen.com/articles/10.1186/s13677-021-00253-7)