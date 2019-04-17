# Census RM Print File Generator
A set of scripts for generating print files directly from a sample file

This repo contains two python scripts
 * [process_sample_file.py](/process_sample_file.py) ingests the sample file, generating ID's and fetching IAC codes and outputting a processed sample file containing the extra data
 * [generate_print_files.py](/generate_print_files.py) ingests a processed sample file and outputs initial contact letter print files 

## Usage

### Dependencies
`pipenv` is used for dependency management, install dependencies with
```bash
pipenv install --dev
```

The process sample file script also needs to call an IAC service. 
You can run it locally with the docker-compose file with 
```bash
docker-compose up -d
```

Or against the docker dev IAC service. For these options the included .env configuration should work without any changes.

If you're running IAC service anywhere else you will need to set `IAC_URL`, `IAC_USERNAME` and `IAC_PASSWORD` in your environment.
### Process Sample File
Run the process_sample_file.py script with pipenv using
```bash
pipenv run python process_sample_file.py <path_to_sample_file.csv> <path_to_write_output.csv>
```

### Generate Print Files
Having produced a processed sample file using the script above, you can generate the print files with
```bash
pipenv run python generate_print_files.py <path_to_processed_sample_file.csv> <path_to_directory_to_write_print_files/>
```

This should write 2 files, one of England treatment codes and one for Wales codes with file names in the format `<PRODUCTPACK_CODE>_<ISO8601-datetime>.csv`

### Tests
Run the unit tests with pytest
```bash
pipenv run pytest
```

Lint with flake8
```bash
pipenv run flake8
```
