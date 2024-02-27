import time
import requests
import datetime
import json
from influxdb_client import InfluxDBClient
import sched
from influxdb_client.client.write_api import SYNCHRONOUS

s = sched.scheduler(time.time, time.sleep)


def load_config():
    """
    Load the configuration from a file.
    :return: The configuration as a dictionary.
    """
    try:
        with open("config.json") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"An exception occurred at load_config: {e}")


def fetch_usage(gas_mprn, gas_serial_number, electricity_mpan, electricity_serial_number, period_to, period_from,
                config):
    """
    Fetch usage data from the Octopus API.
    :param gas_mprn: The MPRN of the gas meter.
    :param gas_serial_number: The serial number of the gas meter.
    :param electricity_mpan: The MPAN of the electricity meter.
    :param electricity_serial_number: The serial number of the electricity meter.
    :param period_to: The period to get the usage data for.
    :param period_from: The period from get the usage data for.
    :param config: The configuration.
    :return: Electricity usage, gas usage
    """
    try:
        headers = {'Authorization': 'Basic ' + config['BASE_64_API_KEY']}
        params = {'period_from': period_from, 'period_to': period_to}
        response_gas = requests.get(
            f'https://api.octopus.energy/v1/gas-meter-points/{gas_mprn}/meters/{gas_serial_number}/consumption/',
            headers=headers, params=params)
        response_electricity = requests.get(
            f'https://api.octopus.energy/v1/electricity-meter-points/{electricity_mpan}/meters/{electricity_serial_number}/consumption/',
            headers=headers, params=params)
        gas_data = response_gas.json()
        electricity_data = response_electricity.json()
        return electricity_data['results'], gas_data['results']
    except Exception as e:
        print(f"An exception occurred at fetch_usage: {e}")


def fetch_tariff(tariff_code, electricity_fuel_type, gas_fuel_type, fuel_type_code, payment_method):
    """
    Fetch tariff data from the Octopus API.
    :param tariff_code: The code of the tariff to fetch.
    :param electricity_fuel_type: The fuel type of the electricity tariff.
    :param gas_fuel_type: The fuel type of the gas tariff.
    :param fuel_type_code: The code of the fuel type.
    :param payment_method: The payment method.
    :return: Electricity unit rate, electricity standing charge, gas unit rate, gas standing charge
    """
    try:
        response = requests.get(f'https://api.octopus.energy/v1/products/{tariff_code}/')
        tariff = response.json()
        electricity_standing_charge = tariff[electricity_fuel_type][fuel_type_code][payment_method][
            'standing_charge_inc_vat']
        electricity_unit_rate = tariff[electricity_fuel_type][fuel_type_code][payment_method][
            'standard_unit_rate_inc_vat']
        gas_standing_charge = tariff[gas_fuel_type][fuel_type_code][payment_method]['standing_charge_inc_vat']
        gas_unit_rate = tariff[gas_fuel_type][fuel_type_code][payment_method]['standard_unit_rate_inc_vat']
        return electricity_unit_rate, electricity_standing_charge, gas_unit_rate, gas_standing_charge
    except Exception as e:
        print(f"An exception occurred at fetch_tariff: {e}")


def calculate_cost(usage, unit_rate, standing_charge):
    """
    Calculate the cost of energy usage.
    :param usage: The amount of energy used in kWh.
    :param unit_rate: The unit rate of the energy in pence.
    :param standing_charge: The standing charge of the energy in pence.
    :return: The cost of the energy usage in pence.
    """

    try:
        return usage * unit_rate + standing_charge
    except Exception as e:
        print(f"An exception occurred at calculate_cost: {e}")


def fetch_and_prepare_data(last_timestamp, config):
    """
    Fetch the data from the Octopus API and prepare it for InfluxDB.
    :param last_timestamp: The last timestamp the data was fetched.
    :param config: The configuration.
    :return: The data prepared for InfluxDB.
    """

    try:
        # Fetch the tariff data for the flexible
        flex_electricity_unit_rate, flex_electricity_standing_charge, \
            flex_gas_unit_rate, flex_gas_standing_charge = fetch_tariff(
            config['OCTOPUS_FLEXIBLE_TARIFF_CODE'], config['OCTOPUS_ELECTRICITY_FUEL_TYPE'],
            config['OCTOPUS_GAS_FUEL_TYPE'], config['OCTOPUS_TARIFF_GSP'],
            config['OCTOPUS_PAYMENT_METHOD_FLEXIBLE'])

        # Fetch the tariff data for the tracker
        tracker_electricity_unit_rate, tracker_electricity_standing_charge, \
            tracker_gas_unit_rate, tracker_gas_standing_charge = fetch_tariff(
            config['OCTOPUS_TRACKER_TARIFF'], config['OCTOPUS_ELECTRICITY_FUEL_TYPE'],
            config['OCTOPUS_GAS_FUEL_TYPE'], config['OCTOPUS_TARIFF_GSP'],
            config['OCTOPUS_PAYMENT_METHOD_TRACKER'])

        # Fetch the usage data
        electricity_usage, gas_usage = fetch_usage(config['GAS_MPRN'], config['GAS_SERIAL_NUMBER'],
                                                   config['ELECTRICITY_MPAN'], config['ELECTRICITY_SERIAL_NUMBER'],
                                                   datetime.datetime.now().isoformat(),
                                                   last_timestamp, config)

        electricity_cost_measurements = []
        electricity_usage_measurements = []
        gas_cost_measurements = []
        gas_usage_measurements = []

        # For each usage data, calculate the cost of the energy usage for the flexible and tracker tariffs
        if len(electricity_usage) != 0:
            for i in range(len(electricity_usage)):
                flex_electricity_cost = calculate_cost(electricity_usage[i]['consumption'],
                                                       flex_electricity_unit_rate,
                                                       flex_electricity_standing_charge)

                tracker_electricity_cost = calculate_cost(electricity_usage[i]['consumption'],
                                                          tracker_electricity_unit_rate,
                                                          tracker_electricity_standing_charge)

                electricity_cost_measurement = {
                    "measurement": "electricity_cost",
                    "time": electricity_usage[i]['interval_end'],
                    "fields": {
                        "flexible_tariff_cost": flex_electricity_cost,
                        "tracker_tariff_cost": tracker_electricity_cost
                    }
                }

                electricity_usage_measurement = {
                    "measurement": "electricity_usage",
                    "time": electricity_usage[i]['interval_end'],
                    "fields": {
                        "usage": electricity_usage[i]['consumption']
                    }
                }

                electricity_cost_measurements.append(electricity_cost_measurement)
                electricity_usage_measurements.append(electricity_usage_measurement)

        if len(gas_usage) != 0:
            for i in range(len(gas_usage)):
                flex_gas_cost = calculate_cost(gas_usage[i]['consumption'],
                                               flex_gas_unit_rate,
                                               flex_gas_standing_charge)

                tracker_gas_cost = calculate_cost(gas_usage[i]['consumption'],
                                                  tracker_gas_unit_rate,
                                                  tracker_gas_standing_charge)

                gas_cost_measurement = {
                    "measurement": "gas_cost",
                    "time": electricity_usage[i]['interval_end'],
                    "fields": {
                        "flexible_tariff_cost": flex_gas_cost,
                        "tracker_tariff_cost": tracker_gas_cost
                    }
                }

                gas_usage_measurement = {
                    "measurement": "gas_usage",
                    "time": electricity_usage[i]['interval_end'],
                    "fields": {
                        "usage": gas_usage[i]['consumption']
                    }
                }

                gas_cost_measurements.append(gas_cost_measurement)
                gas_usage_measurements.append(gas_usage_measurement)

        flexible_tariff = {
            "measurement": "flexible_tariff",
            "time": datetime.datetime.now().isoformat(),
            "fields": {
                "electricity_standing_charge": flex_electricity_standing_charge,
                "gas_standing_charge": flex_gas_standing_charge,
                "electricity_unit_rate": flex_electricity_unit_rate,
                "gas_unit_rate": flex_gas_unit_rate
            }
        }

        tracker_tariff = {
            "measurement": "tracker_tariff",
            "time": datetime.datetime.now().isoformat(),
            "fields": {
                "electricity_standing_charge": tracker_electricity_standing_charge,
                "gas_standing_charge": tracker_gas_standing_charge,
                "electricity_unit_rate": tracker_electricity_unit_rate,
                "gas_unit_rate": tracker_gas_unit_rate
            }
        }

        # Return the data prepared for InfluxDB as a list
        json_body = [flexible_tariff, tracker_tariff] + \
                    electricity_cost_measurements + gas_cost_measurements + \
                    electricity_usage_measurements + gas_usage_measurements

        return json_body
    except Exception as e:
        print(f"An exception occurred at fetch_and_prepare_data: {e}")


def store_data(config):
    """
    This function fetches the usage and tariff data from the Octopus API and stores it in InfluxDB.
    """

    try:
        client = InfluxDBClient(url=config['INFLUXDB_HOST'], token=config['INFLUXDB_TOKEN'], org=config['INFLUXDB_ORG'])

        # Fetch the latest ingestion timestamp from InfluxDB in the electricity_usage measurement or gas_usage measurement
        # whichever one is the latest
        try:
            query_api = client.query_api()
            query = f'from(bucket: "{config["INFLUXDB_BUCKET"]}") ' \
                    f'|> range(start: -24h) ' \
                    f'|> filter(fn: (r) => r["_field"] == "usage") ' \
                    f'|> filter(fn: (r) => r._measurement == "electricity_usage" or r._measurement == "gas_usage") ' \
                    f'|> sort(columns: ["_time"], desc: true) ' \
                    f'|> limit(n: 1)'
            tables = query_api.query(query)
            last_timestamp = tables[0].records[0].get_time().isoformat()
        except Exception as e:
            print(f"An exception occurred at store_data: {e}")
            print("Using default timestamp which is 365 days ago")
            last_timestamp = datetime.datetime.now() - datetime.timedelta(days=365)


        json_body = fetch_and_prepare_data(last_timestamp, config)

        write_api = client.write_api(write_options=SYNCHRONOUS)

        write_api.write(config['INFLUXDB_BUCKET'], config['INFLUXDB_ORG'], json_body)

        print(f"Data stored at {datetime.datetime.now().isoformat()}")

        s.enter(1800, 1, store_data, argument=(config,))

        print(f"Next call scheduled at {datetime.datetime.now() + datetime.timedelta(seconds=1800)}")
    except Exception as e:
        print(f"An exception occurred at store_data: {e}")


def main():
    config = load_config()
    store_data(config)
    s.run()


if __name__ == '__main__':
    """
    The main entry point for the program.
    """
    main()
