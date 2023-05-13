def get_categories(csv_files):
    """Extracts category values from CSV filenames and returns them as a dictionary."""
    categories = {'season_filter': set(), 'city_filter': set(), 'tournament_filter': set(),
                  'hill_filter': set(), 'gender_filter': set(), 'team_filter': set()}
    for csv_file in csv_files:
        file_name = csv_file.split('_')
        categories['season_filter'].add(file_name[0])
        categories['city_filter'].add(file_name[1].split('(')[0])
        categories['tournament_filter'].add(file_name[3])
        categories['hill_filter'].add(file_name[4])
        categories['gender_filter'].add(file_name[5])
        categories['team_filter'].add(file_name[6].split('.')[0])

    categories = {key: sorted(list(val), reverse=key in ['season_filter', 'hill_filter'])
                  for key, val in categories.items()}

    return categories


def files_by_year(csv_files):
    """
        Group a list of CSV files by year.

        Args:
        csv_files (list): A list of CSV filenames.

        Returns:
        dict: A dictionary where the keys are the years found in the filenames
              and the values are lists of filenames for each year.
        """
    file_year_dict = {}
    for file in csv_files:
        year = file.split('-')[0]
        if year in file:
            if year in file_year_dict:
                file_year_dict[year].append(file)
            else:
                file_year_dict[year] = [file]
    file_year_dict = dict(sorted(file_year_dict.items(), reverse=True))

    return file_year_dict


def files_by_season(csv_files):
    seasons_dict = {}
    for file in csv_files:
        file_year = file.split('-')[0]
        file_month = file.split('-')[1]

        t_type = file.split('_')[-3]

        if t_type == 'WC' and file_month in [10, 11, 12]:
            season = file_year + 1
        else:
            season = file_year

        if season in file:
            if season in seasons_dict:
                seasons_dict[season].append(file)
            else:
                seasons_dict[season] = [file]

    seasons_dict = dict(sorted(seasons_dict.items(), reverse=True))

    return seasons_dict


def get_four_hills_files(csv_files):

    four_hills_list = []
    for file in csv_files:
        city = file.split('_')[1].split('(')[0]
        comp_date = file.split('_')[0].split('-')[1]
        comp_day = file.split('_')[0].split('-')[2]
        gender = file.split('_')[-2]
        hill = file.split('_')[-3]

        if city in ['Oberstdorf', 'Garmisch-Partenkirchen', 'GarmischPartenkirchen', 'Innsbruck', 'Bischofshofen']\
                and comp_date in ['12', '01']\
                and gender == 'M'\
                and hill == 'LH':
            four_hills_list.append(file)

    return four_hills_list


def get_raw_air_files(csv_files):
    raw_air_list = []
    for file in csv_files:
        city = file.split('_')[1].split('(')[0]
        comp_year = int(file.split('_')[0].split('-')[0])

        if city in ['Oslo', 'Lillehammer', 'Trondheim', 'Vikersund']\
                and comp_year >= 2016:
            raw_air_list.append(file)

    return raw_air_list
