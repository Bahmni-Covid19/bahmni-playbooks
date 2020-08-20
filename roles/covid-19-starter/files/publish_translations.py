#!/usr/bin/env python
import unittest
import re
import sys
import os
import json


def extract_form_names(form_json):
    result = {}
    for translation in form_json["translations"]:
        result[translation["locale"]] = translation["formName"]
    return result


def extract_translations(form_json):
    result = {}
    for translation in form_json["translations"]:
        result[translation["locale"]] = {"concepts": translation["concepts"], "labels": translation["labels"]}
    return result


def generate_filename(form_name):
    return re.sub(r"[^a-zA-Z0-9-]", "_", form_name) + "_1.json"


if __name__ == '__main__':
    forms_folder = sys.argv[1]
    translations_folder = sys.argv[2]
    for form_file in [file for file in os.listdir(forms_folder) if file.endswith(".json")]:
        with open(os.path.join(forms_folder, form_file), "r") as form_file_obj:
            form_json = json.load(form_file_obj)
            translations = extract_translations(form_json)
            form_names = extract_form_names(form_json)
            for locale in translations:
                with open(os.path.join(translations_folder, generate_filename(form_names[locale])),
                          "w") as translation_file:
                    translation_file.write(json.dumps({locale: translations[locale]}))


    class PublishTranslationsTest(unittest.TestCase):

        def test_extract_translations(self):
            mock_data = {"translations": [
                {
                    "locale": "en",
                    "labels": {
                        "BOOLEAN_NO": "No",
                        "BOOLEAN_YES": "Yes"
                    },
                    "concepts": {
                        "COVID-19-STARTER,_NUMBER_OF_DAYS_IN_ISOLATION_2": "COVID-19-Starter, Number of days in isolation"
                    }
                    ,
                }
            ]}
            self.assertEqual({"en": {
                "labels": {
                    "BOOLEAN_NO": "No",
                    "BOOLEAN_YES": "Yes"
                },
                "concepts": {
                    "COVID-19-STARTER,_NUMBER_OF_DAYS_IN_ISOLATION_2": "COVID-19-Starter, Number of days in isolation"
                }
            }}, extract_translations(mock_data))

        def test_extract_form_names(self):
            mock_data = {"translations": [
                {
                    "locale": "en",
                    "formName": "ABC"
                },
                {
                    "locale": "es",
                    "formName": "DEF"
                }
            ]}
            self.assertEqual({"en": "ABC", "es": "DEF"}, extract_form_names(mock_data))

        def test_generate_filename(self):
            self.assertEqual("COVID-19-Starter-Set__Home_Quarantine_Screening_1.json",
                             generate_filename("COVID-19-Starter-Set, Home Quarantine Screening"))
