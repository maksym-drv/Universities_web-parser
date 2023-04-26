from django.test import TestCase

# Create your tests here.
import pandas as pd

# Example data
regions = [
    {
        'region_name': 'Region 1',
        'universities': [
            {
                'university_name': 'University 1',
                'specialities': [
                    {
                        'speciality_name': 'Speciality 1',
                        'marks': {'English': 90, 'Math': 85, 'Science': 95}
                    },
                    {
                        'speciality_name': 'Speciality 2',
                        'marks': {'English': 92, 'Math': 88, 'Science': 96}
                    }
                ]
            },
            {
                'university_name': 'University 2',
                'specialities': [
                    {
                        'speciality_name': 'Speciality 3',
                        'marks': {'English': 88, 'Math': 89, 'Science': 92}
                    },
                    {
                        'speciality_name': 'Speciality 4',
                        'marks': {'English': 91, 'Math': 87, 'Science': 94}
                    }
                ]
            }
        ]
    },
    {
        'region_name': 'Region 2',
        'universities': [
            {
                'university_name': 'University 3',
                'specialities': [
                    {
                        'speciality_name': 'Speciality 5',
                        'marks': {'English': 89, 'Math': 84, 'Science': 90}
                    },
                    {
                        'speciality_name': 'Speciality 6',
                        'marks': {'English': 90, 'Math': 86, 'Science': 92}
                    }
                ]
            },
            {
                'university_name': 'University 4',
                'specialities': [
                    {
                        'speciality_name': 'Speciality 7',
                        'marks': {'English': 87, 'Math': 88, 'Science': 91}
                    },
                    {
                        'speciality_name': 'Speciality 8',
                        'marks': {'English': 89, 'Math': 87, 'Science': 93}
                    }
                ]
            }
        ]
    }
]

# Create empty DataFrames for regions, universities, specialities, and marks
regions_df = pd.DataFrame(columns=['Region', 'University', 'Speciality', 'Subject', 'Marks'])
universities_df = pd.DataFrame(columns=['Region', 'University', 'Speciality', 'Subject', 'Marks'])
specialities_df = pd.DataFrame(columns=['Region', 'University', 'Speciality', 'Subject', 'Marks'])
marks_df = pd.DataFrame(columns=['Region', 'University', 'Speciality', 'Subject', 'Marks'])

writer = pd.ExcelWriter("data.xlsx")

# Loop through the data and populate the DataFrames
for region in regions:
    region_name = region['region_name']
    universities = region['universities']
    for university in universities:
        university_name = university['university_name']
        specialities = university['specialities']
        for speciality in specialities:
            speciality_name = speciality['speciality_name']
            marks = speciality['marks']
            for subject, mark in marks.items():
                # Append data to the respective DataFrames
                regions_df = regions_df.concat({'Region': region_name, 'University': university_name, 'Speciality': speciality_name, 'Subject': subject, 'Marks': mark}, ignore_index=True)
                universities_df = universities_df.concat({'Region': region_name, 'University': university_name, 'Speciality': speciality_name, 'Subject': subject, 'Marks': mark}, ignore_index=True)