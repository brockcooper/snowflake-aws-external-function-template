import json
import boto3

translate = boto3.client('translate')


def handler(event, context, local=False):
    translated = []

    if local:
        body = event["body"]
    else:
        body = json.loads(event["body"])

    for row in body["data"]:
        text_list = []
        for language in row[2]:
            try:
                translated_text = translate.translate_text(
                    Text=row[1],
                    SourceLanguageCode='en',
                    TargetLanguageCode=language)["TranslatedText"]
                text_list.append({"language": language,
                                  "translated_text": translated_text,
                                  "status": 'success'})
            except Exception as e:
                print(e)
                # status code of 400 implies an error
                text_list.append({"language": language,
                                  "text_error": row[1],
                                  "status": 'fail',
                                  "error_message": e})
        translated.append([row[0], text_list])

    json_compatible_string_to_return = json.dumps({"data": translated})
    # return data according to Snowflake's specified result format
    return {
        'body': json_compatible_string_to_return
    }


# For local testing. Just run python translate_to_english.py for local testing
if __name__ == '__main__':
    event = {"body": {
                "data": [
                    [0, "Hello", ["es", "fr"]],
                    [1, """All other supported data types are serialized
                        as JSON strings.""", ["es", "fr"]],
                    [2, """Examples of extracting data are included in the
                        documentation for creating a remote service
                        on each platform""", ["es", "fr"]]
                ]
            }}
    print(handler(event, 'context', local=True))
