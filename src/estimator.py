import math

def estimator(data):
    # initialize data holders
    impact = {}
    severeImpact = {}

    # retrieve important info from input data
    reported = data['reportedCases']

    ######################  CHALLENGE ONE   ###########################
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

    multiple_of_three = num_of_days // 3
    factor = math.pow(2, multiple_of_three)

    impact['infectionsByRequestedTime'] = impact['currentlyInfected'] * factor
    severeImpact['infectionsByRequestedTime'] = severeImpact['currentlyInfected'] * factor
    ##################################################################################################

    ############################    CHALLENGE TWO   ##############################################
    # estimate number of severe positve cases
    # assume that 15% of projected cases will be severe
    impact['severeCasesByRequestedTime'] = math.trunc(impact['infectionsByRequestedTime'] * 0.15)
    severeImpact['severeCasesByRequestedTime'] = math.trunc(severeImpact['infectionsByRequestedTime'] * 0.15)
    
    # estimate available number of hospital beds for severe cases
    # expect that maximum of 35% of total bede spaces will be available
    available = math.trunc(data['totalHospitalBeds'] * 0.35)

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

    ##########################################################################################


    ############################    CHALLENGE THREE  ###########################################
    # estimate severe cases that would need ICU care
    # This is expected to be 5% of infectionsByRequestedTime
    impact['casesForICUByRequestedTime'] = math.floor(impact['infectionsByRequestedTime'] * 0.05)
    severeImpact['casesForICUByRequestedTime'] = math.floor(severeImpact['infectionsByRequestedTime'] * 0.05)

    # estimate number of positive cases to require ventilators
    # This is expected to be 2% of infectionsByRequestedTime
    impact['casesForVentilatorsByRequestedTime'] = math.floor(impact['infectionsByRequestedTime'] * 0.02)
    severeImpact['casesForVentilatorsByRequestedTime'] = math.floor(severeImpact['infectionsByRequestedTime'] * 0.02)

    # estimate economic impact to the region based on number infections by requested time
    ave_income = data['region']['avgDailyIncomeInUSD']
    ave_income_pop = data['region']['avgDailyIncomePopulation']

    impact['dollarsInFlight'] = math.ceil((
        impact['infectionsByRequestedTime'] * ave_income_pop) * ave_income * num_of_days)
    severeImpact['dollarsInFlight'] = math.ceil((
        severeImpact['infectionsByRequestedTime'] * ave_income_pop) * ave_income * num_of_days)
    ##########################################################################################

    # construct output object
    result = {'data': data, 'impact': impact, 'severeImpact': severeImpact}

    # return output
    return result
