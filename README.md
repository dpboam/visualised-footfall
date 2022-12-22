# visualised-footfall

- This project builds upon [previous Open Innovations work](https://github.com/open-innovations/traffic-growth) processing and visualising Leeds City Centre footfall data.
- The Script 'collate.py' pulls [data](https://github.com/open-innovations/traffic-growth/tree/main/data/leeds) from this repo which has been processed from the original format to a simpler form. 
- It then uses parameters which can be set in a yaml file to further process this data for visualisations.
- Parameters include which sensors to use, what times of day and months of the year should be filtered, and what time period should the data be grouped by.
- The script will save the newly processed data as a csv (name/path can be specified in the  parameters)
- It was also use mathplotlib.plyplot to create a chart using the data (type can be specified in the  parameters)
- From inside the repo run `python src/collate.py CONFIG_FILE_PATH`
- If no config file is specified `config_template.yml` will be used.