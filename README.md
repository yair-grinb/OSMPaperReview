# OSMPaperReview
A repository for analyzing OSM-related publications from the years 2016-2019, as presented in the paper "Bridges and Barriers: An Exploration of Engagements of the Research Community with the OpenStreetMap Community" by A. Yair Griberger, Marco Minghini, Godwin Yeboah, Levente Juhász, and Peter Mooney (submitted to the ISPRS International Journal of Geo-Information). 

**data:** the dataset is publicly available for download at https://zenodo.org/record/4474588#.YBJP-OgzZPZ

**analyze_review.py:** reads the initial data file into a pandas DataFrame, produces a summary table, prints out some discriptive statistics, and produces additional files used to produce alluvial diagrams using https://rawgraphs.io/.

**osm_review_figures.Rmd:** reads the initial data file into a data frame, corrects country names, generates the study area continents columns, and produces three figures: map of authors' home locations (# papers per country), map of study area locations (# papers per country), circular chord diagram connecting author locations and study areas by number of papers at the continental level.
