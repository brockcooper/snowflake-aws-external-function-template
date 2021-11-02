# Snowflake External Function Template for Deploying to AWS with Github Actions

### Purpose

This repo contains a template to deploy a lambda function using Github Actions to AWS and be used for an external function in Snowflake.

### Example Complete External Function Repo

[This repo](https://github.com/brockcooper/translate-text-snowflake-external-function) is an example of a complete AWS Lambda function that is used as an Extneral Function.

### How to Deploy

1. Set up Template in your own Github account

Click the "Use this Template" button in Github and create a new repo using this template

2. Write your Python code in the `external_function.py` file

Do this on a feature branch (see below) to ensure you aren't prematurely deploying something to production

3. Update your Unittests in the `tests.py` file

It's always important to add tests to your work, so add some specfiic tests to test out your code.

4. Set up Github Repo Settings

In your Github repo, go to settings, Secrets, and add 4 secrets with their respective credentials. You will want to use a user that has the appropriate role to deploy a Lambda function and API Gateway using a CloudFormation template.:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_DEFAULT_REGION`
* `SNOWFLAKE_IAM_ROLE`: This should be the IAM role that you are allowing Snowflake to use. If you don't provide this then the code defaults to using `SnowflakeExternalFunctionsRole` as the role name

You should also protect your `main` and `dev` branches to not allow for deletion, directly pushing to those branches without a Pull Request, and to require the right permissions to only certain users to approve Pull Requests.

5. Push API Gateway and Lambda function to AWS

This repo has a built in CI/CD pipeline using Github Actions found in `.github/workflows/deploy.yml`. All developement branches should be built off the `dev` branch. Once the branch is pushed to the Github repo, a small amount of tests will run to ensure the code is working as intended. When the development branch gets merged into the `dev` branch, Github will deploy a dev version of the API Gateway and Lambda to AWS, with a naming convention of `dev` added to the name. Finally, when `dev` is merged into `main` the true production version of the application will be available for use.

The branches should look similar to this flow:

```
           < feature_branch_1
           < feature_branch_2
main < dev < feature_branch_3
           < feature_branch_4
           < feature_branch_5
```

3. Create the API Integration in Snowflake

This repo is primarily intended to deploy the API Gateway and Lambda to AWS. All other set up will need to take place in Snowflake. You will want to follow the [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/external-functions-creating-aws-common-api-integration.html) describing the API Integration and the AWS IAM policy and role that is needed.

4. Create the Snowflake External Function in Snowflake

Here is an example of creating and calling the external function in Snowflake:

```SQL
create or replace external function translate_from_english(english_text varchar, languages variant)
    returns variant
    api_integration = <your_api_integration_name>
    as 'https://abc123ef5.execute-api.us-west-2.amazonaws.com/prod/translate/from_english';

select translate_from_english('This is an example english text', array_construct('es','fr', 'ja'));

```

### Explanation of Files
* `.github/workflows/deploy.yml`: Uses Github Actions for the CI/CD pipeline
* `requirements.txt`: Lists the required packages needed to run the code locally and deploy to Lambda. You can run `pip install -r requirements.txt` on your local environment to download the required packages for your local development use
* `serverless.yml`: Uses the serverless framework to deploy API Gateway and Lambda to AWS. See `.github/workflows/deploy.yml` for the code that runs to deploy with serverless.
* `tests.py`: Unittests that must pass before the code gets deployed
* `translate_from_english.py`: This is the actual Python code that will run on the Lambda function


