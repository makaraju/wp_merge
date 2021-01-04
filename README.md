# wp_merge

## Prerequisites
Make sure you have installed all of the following prerequisites on your development machine:
* python3 & pip3
* Git - [Download & Install Git](https://git-scm.com/downloads). OSX and Linux machines typically have this already installed.

### Cloning The GitHub Repository
The recommended way to get wp_merge is to use git to directly clone the wp_merge repository:

```bash
$ git clone https://github.com/makaraju/wp_merge.git wp_merge
$ cd wp_merge
$ pip3 install -r requirements.txt
```

## Merge Accounts

This application merges accounts from two sources. It merges data from API end point http://interview.wpengine.io/v1/accounts/{account_id} for each account into the CSV account data provided in the input.

The CSV file is the absolute truth of source, meaning if there are no accounts in CSV even though there are accounts in API end point, the result is an empty output file.

## Testing Your wp_merge

You can test the merge program by running it as below:
 ```bash
$ ./wpe_merge.sh test
 ```

## Invoke wp_merge

You can invoke the merge program by invoking it as below: 

```bash
$ ./wpe_merge.sh input.csv output.csv
```

Here, input.csv is the path of the input CSV file, and output is the path of the output file. Path is relative to the root of the project.

Both the input and output file names are mandatory