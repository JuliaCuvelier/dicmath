# Azure Speech Key Tutorial

This guide will walk you through the process of obtaining an Azure Speech key for use with the DicMath application. If you prefer to use the official Microsoft documentation, you can find it [here](https://learn.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=speech).

## Prerequisites

Before you begin, you'll need to have a Microsoft Azure account. If you don't have one, you can sign up for a free trial [here](https://azure.microsoft.com/en-us/free/).

## Steps to Get an Azure Speech Key

1. Sign in to the [Azure Portal](https://portal.azure.com/).

2. Click on the "**Create a resource**" button in the left-hand menu.

3. In the search bar, type "**Speech**" and select "**Speech**" from the results.

4. Click on the "**Create**" button to start configuring the Speech service.

5. Fill in the required information:

   - **Subscription**: Choose your Azure subscription.
   - **Resource group**: Create a new resource group or select an existing one.
   - **Region**: Choose a region that's close to your location.
   - **Name**: Give your Speech service a unique name.
   - **Pricing tier**: Select the appropriate pricing tier for your usage.

6. Click on the "**Review + create**" button, and then click on the "**Create**" button to deploy the Speech service.

7. Once the deployment is complete, navigate to the Speech service you just created by clicking on the "**Go to resource**" button or by searching for it in the "**All resources**" section.

8. In the Speech service's "**Overview**" tab, locate the "Keys and Endpoint" section, where you'll find two keys: Key1 and Key2. You can use either of these keys in your DicMath application.

That's it! You now have an Azure Speech key that you can use with the DicMath application.
