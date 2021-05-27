class RecognizeCustomForms(object):

    def recognize_custom_forms(self):
        form_output  = {}

        path_to_sample_forms ="test10.jpeg"
        # [START recognize_custom_forms]
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.formrecognizer import FormRecognizerClient

        endpoint = "https://formfeedback.cognitiveservices.azure.com/"
        key = "5d3f9679d8e84d33b89e326f60865132"
        model_id = "0d596d11-d48d-408c-9ca6-d2f295ea978f"

        form_recognizer_client = FormRecognizerClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        # Make sure your form's type is included in the list of form types the custom model can recognize
        with open(path_to_sample_forms, "rb") as f:

          poller = form_recognizer_client.begin_recognize_custom_forms(
                model_id=model_id, form=f, include_field_elements=True
            )
        # form_url = "https://storage123indexer.blob.core.windows.net/container2/New Directory/formdocument.jpeg"
        # poller = form_recognizer_client.begin_recognize_custom_forms_from_url(model_id=model_id, form_url=form_url)

        forms = poller.result()
        type(forms)
        print(forms)
        print('#'* 30)
        for idx, form in enumerate(forms):
            print("--------Recognizing Form #{}--------".format(idx+1))
            print("Form has type {}".format(form.form_type))
            print("Form has form type confidence {}".format(form.form_type_confidence))
            print("Form was analyzed with model with ID {}".format(form.model_id))
            for name, field in form.fields.items():
                # each field is of type FormField
                # label_data is populated if you are using a model trained without labels,
                # since the service needs to make predictions for labels if not explicitly given to it.
                if field.label_data:
                    print("...Field '{}' has label '{}' with a confidence score of {}".format(
                        name,
                        field.label_data.text,
                        field.confidence
                    ))

                print("...Label '{}' has value '{}' with a confidence score of {}".format(
                    field.label_data.text if field.label_data else name, field.value, field.confidence
                ))
                form_output[field.label_data.text if field.label_data else name]=field.value
                
                
                


            # iterate over tables, lines, and selection marks on each page
            for page in form.pages:
                for i, table in enumerate(page.tables):
                    print("\nTable {} on page {}".format(i+1, table.page_number))
                    for cell in table.cells:
                        print("...Cell[{}][{}] has text '{}' with confidence {}".format(
                            cell.row_index, cell.column_index, cell.text, cell.confidence
                        ))
                print("\nLines found on page {}".format(page.page_number))
                for line in page.lines:
                    print("...Line '{}' is made up of the following words: ".format(line.text))
                    for word in line.words:
                        print("......Word '{}' has a confidence of {}".format(
                            word.text,
                            word.confidence
                        ))
                if page.selection_marks:
                    print("\nSelection marks found on page {}".format(page.page_number))
                    for selection_mark in page.selection_marks:
                        print("......Selection mark is '{}' and has a confidence of {}".format(
                            selection_mark.state,
                            selection_mark.confidence
                        ))
            return form_output
            print("-----------------------------------")
        # [END recognize_custom_forms]
if __name__ == "__main__":
    sample = RecognizeCustomForms()
    output =sample.recognize_custom_forms()
    print(output)