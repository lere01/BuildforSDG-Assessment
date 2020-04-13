import math

def estimator(data):
    # initialize data holders
    impact = {}
    severeImpact = {}

    # retrieve important info from input data
    reported = data['reportedCases']

    # estimate currently infected
    impact['currentlyInfected'] = reported * 10
    severeImpact['currentlyInfected'] = reported * 50

    # estimate infections based on requested time
    # assume that the number of cases will double every two days
    period_type = data['periodType'].lower()
    time_frame = data['timeToElapse']

    if period_type == "days":
        num_of_days = time_frame
    elif period_type == "weeks":
        num_of_days = time_frame * 7
    elif period_type == "months":
        num_of_days = time_frame * 30

    multiple_of_three = math.floor(num_of_days / 3)
    factor = math.pow(2, multiple_of_three)

    impact['infectionsByRequestedTime'] = impact['currentlyInfected'] * factor
    severeImpact['infectionsByRequestedTime'] = severeImpact['currentlyInfected'] * factor

    # estimate number of severe positve cases
    # assume that 15% of projected cases will be severe
    impact['severeCasesByRequestedTime'] = impact['infectionsByRequestedTime'] * 0.15
    severeImpact['severeCasesByRequestedTime'] = severeImpact['infectionsByRequestedTime'] * 0.15

    # estimate available number of hospital beds for severe cases
    # expect that maximum of 35% of total bede spaces will be available
    available = math.floor(data['totalHospitalBeds'] * 0.35)

    if impact['severeCasesByRequestedTime'] <= available:
        impact['hospitalBedsByRequestedTime'] = available
    else:
        impact['hospitalBedsByRequestedTime'] = available - \
            impact['severeCasesByRequestedTime']

    if severeImpact['severeCasesByRequestedTime'] <= available:
        severeImpact['hospitalBedsByRequestedTime'] = available
    else:
        severeImpact['hospitalBedsByRequestedTime'] = available - \
            severeImpact['severeCasesByRequestedTime']

    # estimate severe cases that would need ICU care
    # This is expected to be 5% of infectionsByRequestedTime
    impact['casesForICUByRequestedTime'] = impact['infectionsByRequestedTime'] * 0.05
    severeImpact['casesForICUByRequestedTime'] = severeImpact['infectionsByRequestedTime'] * 0.05

    # estimate number of positive cases to require ventilators
    # This is expected to be 2% of infectionsByRequestedTime
    impact['casesForVentilatorsByRequestedTime'] = impact['infectionsByRequestedTime'] * 0.02
    severeImpact['casesForVentilatorsByRequestedTime'] = severeImpact['infectionsByRequestedTime'] * 0.02

    # estimate economic impact to the region based on number infections by requested time
    ave_income = data['region']['avgDailyIncomeInUSD']
    ave_income_pop = data['region']['avgDailyIncomePopulation']

    impact['dollarsInFlight'] = (
        impact['infectionsByRequestedTime'] * ave_income_pop) * ave_income * num_of_days
    severeImpact['dollarsInFlight'] = (
        severeImpact['infectionsByRequestedTime'] * ave_income_pop) * ave_income * num_of_days

    # construct output object
    result = {'data': data, 'impact': impact, 'severeImpact': severeImpact}

    # return output
    return result
