import csv

class DataHandler(object):
    def __init__(self, depth_file: str, production_file: str) -> None:
        self.MAX_DEPTH = 300
        self.load_depth(depth_file)
        self.load_production(production_file)

    def open_file(self, filename: str) -> list:
        with open(filename, u'r') as gov_file:
            return gov_file.read().split(u'\n')

    def load_depth(self, filename: str) -> None:
        self.depth = {lease[0:7]: lease[149:154] for lease in self.open_file(filename)}

    def load_production(self, filename: str) -> None:
        prod = self.open_file(filename)

        self.prod = list()
        for line, entry in enumerate(prod):
            try:
                self.prod.append(self.get_data(entry))

            except ValueError:
                import sys
                import traceback

                traceback.print_exc()

                print(f'Error found on line: {line}')
                sys.exit()

    def get_data(self, lease: str) -> dict:
        return {
            u'lease_number':     lease[0:7],      #NEED
            # u'completion_name':  lease[7:13],
            u'production_date':  lease[13:19].strip(),         #NEED
            u'production_days':  int(lease[19:21].strip()),    #NEED
            # u'product_code':     lease[21],
            u'monthly_oil':      int(lease[22:31].strip()),    #NEED
            u'monthly_gas':      int(lease[31:40].strip()),    #NEED
            u'monthly_water':    int(lease[40:49].strip()),    #NEED
            u'api_well_number':  lease[49:61].strip(),         #NEED
            # u'well_status_code': lease[61:63],
            # u'area_code':        lease[63:65],
            # u'block_number':     lease[65:71],
            u'bottom_area_code': lease[71:73] + u' ' + lease[73:79].strip(),         #NEED
            # u'bottom_block':     lease[73:79].strip(),
            # u'operator_number':  lease[79:84],
            # u'operator_name':    lease[84:129],
            # u'field_name':       lease[129:137],
            # u'injection_volume': int(lease[137:146]),
            u'prod_interval':    lease[146:149].strip(),       #NEED
            # u'date':             lease[149:158],
            # u'unit_agreement':   lease[158:]

            u'WellZone': lease[49:61] + lease[146:149]
        }
            # u'WellZone': lease[49:61] + lease[146:149]

    def prepare_data(self, production_type: str) -> None:
        self.data = dict()
        self.dates = list()

        for entry in self.prod:
            if entry[u'lease_number'] in self.depth.keys():
                if int(self.depth[entry[u'lease_number']]) >= self.MAX_DEPTH:
                    if entry[u'WellZone'] not in self.data.keys():
                        self.data[entry[u'WellZone']] = {
                            u'WellZone': entry[u'WellZone'],
                            u'BlockNum': entry[u'bottom_area_code'],
                            u'API':      entry[u'api_well_number'],
                            u'Int':      entry[u'prod_interval'],
                            u'Production': {entry[u'production_date']: entry[production_type]}}

                    else:
                        self.data[entry[u'WellZone']][u'Production'][entry[u'production_date']] = entry[production_type]

                    if int(entry[u'production_date']) not in self.dates:
                        self.dates.append(int(entry[u'production_date']))

            else:
                pass
                # print(u'This lease is kinda fucked up...')

        self.dates.sort()

    def prepare_monthly_production_data(self) -> None:
        self.data = dict()
        self.dates = list()

        for entry in self.prod:
            if entry[u'lease_number'] in self.depth.keys():
                if int(self.depth[entry[u'lease_number']]) >= self.MAX_DEPTH:
                    if entry[u'WellZone'] not in self.data.keys():
                        self.data[entry[u'WellZone']] = {
                            u'WellZone': entry[u'WellZone'],
                            u'BlockNum': entry[u'bottom_area_code'],
                            u'API':      entry[u'api_well_number'],
                            u'Int':      entry[u'prod_interval'],
                            u'Production': {entry[u'production_date']: entry[u'production_days']}}

                    else:
                        self.data[entry[u'WellZone']][u'Production'][entry[u'production_date']] = entry[u'production_days']

                    if int(entry[u'production_date']) not in self.dates:
                        self.dates.append(int(entry[u'production_date']))

            else:
                pass
                # print(u'This lease is kinda fucked up...')

        self.dates.sort()

def create_csv(content, production_type) -> None:
    body = list()
    header = [u'BlockNum', u'API', u'Int', u'WellZone'] + [str(year)[4:] + u'/' + str(year)[:4] for year in content.dates]
    for well in content.data.keys():
        row = [content.data[well][u'BlockNum'], content.data[well][u'API'], content.data[well][u'Int'], content.data[well][u'WellZone']]
        for month in content.dates:
            if str(month) in content.data[well][u'Production'].keys():
                row.append(content.data[well][u'Production'][str(month)])

            else:
                row.append(0)

        body.append(row)

    with open(production_type + u'.csv', u'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect=u'excel')
        csvwriter.writerow(header)
        for row in body:
            csvwriter.writerow(row)

# PRODUCTION_TYPES = [u'monthly_oil', u'monthly_water', u'monthly_gas']
# ANNUM = [u'1947', u'1968', u'1989', u'2010']

# for YEAR in ANNUM:
#     print(u'The year was', YEAR)
#     data = DataHandler(depth_file = u'LSETAPE.DAT', production_file = YEAR + u'.DAT')
 
#     for p_type in PRODUCTION_TYPES:
#         print(u'Working on some:', p_type)
#         data.prepare_data(p_type)
#         create_csv(data, f'{YEAR}/{p_type}')

#     print(u'Getting days worked')
#     data.data = dict()
#     data.prepare_monthly_production_data()
#     create_csv(data, f'{YEAR}/days')
def get_data_2(lease: str) -> list:
    return [
        lease[0:7],
        lease[7:13],
        lease[13:19],
        lease[19:21],
        lease[21],
        lease[22:31],
        lease[31:40],
        lease[40:49],
        lease[49:61],
        lease[61:63],
        lease[63:65],
        lease[65:71],
        lease[71:73],
        lease[73:79],
        lease[79:84],
        lease[84:129],
        lease[129:137],
        lease[137:146],
        lease[146:149],
        lease[149:158],
        lease[158:]]


def csv_2(data):
    for year in data.keys():
        with open(u'output/{year}.csv'.format(year = year), u'w') as csvfile:
            csvwriter = csv.writer(csvfile, dialect=u'excel')
            for row in data[year]:
                csvwriter.writerow(row)



YEARS = ['1947', '1968', '1989', '2010']

for annum in YEARS:
    print(u'Reformatting {annum}'.format(annum = annum))
    organized_data = dict()

    with open(u'{annum}.DAT'.format(annum = annum), u'r') as text_file:
        data = text_file.read().split(u'\n')

    for i in data:
        entry = get_data_2(i)
        year = str((((int(entry[2][:4]) - int(annum)) // 5) * 5) + int(annum))
        try:
            organized_data[year].append(entry)

        except KeyError:
            organized_data[year] = [entry]

    csv_2(organized_data)

# print(clean_data[:3])

# print(len(data))