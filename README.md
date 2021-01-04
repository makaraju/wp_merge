# wp_merge

### Getting started

To get started, first we need to have python3 installed and install the required packages.

`pip3 install -r requirements.txt`

### Merge Accounts

This application merges accounts from two sources. It merges data from API end point http://interview.wpengine.io/v1/accounts/{account_id} for each account into the CSV account data provided in the input.

The CSV file is the absolute truth of source, meaning if there are no accounts in CSV even though there are accounts in API end point, the result is an empty output file.

### How to test

You can test the merge program by running it as below:
 
`./wpe_merge.sh test`

### How to invoke

You can invoke the merge program by invoking it as below: 

`./wpe_merge.sh input.csv output.csv`

Here, input.csv is the path of the input CSV file, and output is the path of the output file. Path is relative to the root of the project.

Both the input and output file names are mandatory