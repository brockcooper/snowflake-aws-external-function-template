import json


def handler(event, context, local=False):
    all_results = []

    if local:
        body = event["body"]
    else:
        body = json.loads(event["body"])

    for row in body["data"]:
        try:
            # Write code to manipulate a row here:
            row_result = {"result": row[1][::-1],
                          "status": 'success'}
        except Exception as e:
            # Write code to handle a failure here:
            print(e)
            row_result = {"text_error": row[1],
                          "status": 'fail',
                          "error_message": e}
        all_results.append([row[0], row_result])

    json_compatible_string_to_return = json.dumps({"data": all_results})
    # return data according to Snowflake's specified result format
    return {
        'body': json_compatible_string_to_return
    }


# For local testing. Just run python lambda_function.py for local testing
if __name__ == '__main__':
    event = {"body": {
                "data": [
                    [0, "Test 0"],
                    [1, "Test 1"],
                    [2, "Test 2"],
                ]
            }}

    print(handler(event, 'context', local=True))
