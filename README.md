## Energy Dashboard

This project is designed to fetch data from the Octopus Energy API, calculate the cost of energy usage for different
tariffs, store this data in InfluxDB, and display it on a Grafana dashboard. This allows you to compare the cost of
different tariffs and make an informed decision about which one is best for you.
Currently, the project supports the Octopus Energy flexible and tracker tariffs, but it can be easily extended to
support other tariffs as well in the near future.

## Overview

The project uses Python to interact with the Octopus Energy API and fetch tariff data. It calculates the cost of energy
usage for each tariff and stores this data in InfluxDB. The data is then visualized on a Grafana dashboard,
which displays the standing charges, unit rates, and cost of usage for each tariff.

## Features

- Fetches tariff data from the Octopus Energy API.
- Calculates the cost of energy usage for each tariff.
- Stores data in InfluxDB.
- Displays data on a Grafana dashboard.

## Setup

1. Clone the repository.
2. Open the `.env` file and replace the placeholder values with your actual environment variables. More information in
   the [Docker Environment Variables](#docker-environment-variables) section.
3. Configure the Grafana datasource in the `grafana/provisioning/datasources/datasources.yml` file. More information in
   the [Grafana Datasource](#grafana-datasource) section.
4. Run the Docker Compose command to start all the services.
5. You can access the Grafana dashboard at `http://localhost:3000`.
6. You can also access the InfluxDB UI at `http://localhost:8086`.

## Configuration Options

## Python Script

The `config.json` file contains various configuration options that are used by the Python script to interact with the
Octopus Energy API and InfluxDB.
Here's a brief explanation of each configuration option:

- `API_KEY`: Your Octopus Energy API key.
- `BASE_64_API_KEY`: The base64 encoded version of your Octopus Energy API key.
- `GAS_MPRN`: The MPRN (Meter Point Reference Number) of your gas meter.
- `GAS_SERIAL_NUMBER`: The serial number of your gas meter.
- `ELECTRICITY_MPAN`: The MPAN (Meter Point Administration Number) of your electricity meter.
- `ELECTRICITY_SERIAL_NUMBER`: The serial number of your electricity meter.
- `OCTOPUS_FLEXIBLE_TARIFF_NAME`: The name of the Octopus Energy flexible tariff.
- `OCTOPUS_FLEXIBLE_TARIFF_CODE`: The code of the Octopus Energy flexible tariff.
- `OCTOPUS_TRACKER_TARIFF_NAME`: The name of the Octopus Energy tracker tariff.
- `OCTOPUS_TRACKER_TARIFF`: The code of the Octopus Energy tracker tariff.
- `OCTOPUS_ELECTRICITY_FUEL_TYPE`: The fuel type of the electricity tariff.
- `OCTOPUS_GAS_FUEL_TYPE`: The fuel type of the gas tariff.
- `OCTOPUS_TARIFF_GSP`: The code of the GSP (Grid Supply Point) for the tariff (your region).
- `OCTOPUS_PAYMENT_METHOD_FLEXIBLE`: The payment method for the flexible tariff.
- `OCTOPUS_PAYMENT_METHOD_TRACKER`: The payment method for the tracker tariff.
- `INFLUXDB_HOST`: The URL of your InfluxDB instance.
- `INFLUXDB_TOKEN`: Your InfluxDB token.
- `INFLUXDB_ORG`: Your InfluxDB organization.
- `INFLUXDB_BUCKET`: The name of your InfluxDB bucket.

## Docker Environment Variables

The `docker-compose.yml` file uses environment variables to configure the Docker containers for InfluxDB and Grafana.

### Application Configuration

- `CONFIG_PATH`: Path to the application configuration file. Set to `/app/config.json`.

### InfluxDB Initialization

- `DOCKER_INFLUXDB_INIT_MODE`: Initial setup mode for the InfluxDB Docker container.
- `DOCKER_INFLUXDB_INIT_ORG`: Name of the organization to be created during the initial setup.
- `DOCKER_INFLUXDB_INIT_BUCKET`: Name of the bucket to be created during the initial setup.
- `DOCKER_INFLUXDB_INIT_USERNAME`: Username of the user to be created during the initial setup.
- `DOCKER_INFLUXDB_INIT_PASSWORD`: Password of the user to be created during the initial setup.
- `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`: Token to be associated with the admin user during the initial setup.

### Grafana Admin User

- `GF_SECURITY_ADMIN_USER`: Username for the admin user of the Grafana Docker container.

  These environment variables are used to configure the Docker containers for InfluxDB and Grafana, as well as to
  specify the path to the configuration file for your application.

## Grafana Datasource

- `name`: The name of the datasource. This is how you will refer to the datasource in Grafana.
- `type`: The type of the datasource. In this case, it should be `influxdb`.
- `url`: The URL of your InfluxDB instance.
- `access`: The method used to access the data source. It should be set to `proxy`.
- `default`: Whether this datasource should be the default datasource. It should be set to `true`.
- `secureJsonData.token`: Your InfluxDB token.
- `jsonData.organization`: Your InfluxDB organization.
- `jsonData.version`: The version of InfluxDB you are using. It should be set to `Flux`.
- `jsonData.defaultBucket`: The name of your InfluxDB bucket.

## Obtaining Tariff Names, Codes and GSP

To obtain the tariff names, codes and GSP (Grid Supply Point), you can make a request to the Octopus Energy API
using `curl`:
More information can be found [here](https://developer.octopus.energy/docs/api/)

```bash
curl --location 'https://api.octopus.energy/v1/products/'
```

Please replace the placeholders in the `config.json` file with your actual data.

## Grafana Dashboard

The Grafana dashboard displays the following information:

- Standing charges for each tariff.
- Unit rates for each tariff.
- Cost of usage for each tariff.

The dashboard is updated in real-time as new data is fetched and stored in InfluxDB.

## Technologies Used

- Python
- Octopus Energy API
- InfluxDB
- Grafana
- Docker

## Disclaimer

This project is purely for educational purposes. The author is not responsible for any misuse of the information provided,
or any actions taken based on the information provided in this project. I have no affiliation with Octopus Energy

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)