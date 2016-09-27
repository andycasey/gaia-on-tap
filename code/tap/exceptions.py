
""" Custom exceptions for dealing with responses from the TAP server """

__all__ = ["TAPQueryException", "TAPUploadException"]


class TAPQueryException(Exception):

    def __init__(self, response, message=None):

        # Try parsing out an error message.
        if message is None:
            try:
                message = response.text\
                    .split('<INFO name="QUERY_STATUS" value="ERROR">')[1]\
                    .split('</INFO>')[0].strip()

            except:
                message = "{} code returned".format(response.status_code)

        super(TAPQueryException, self).__init__(message)

        self.errors = response
        return None



class TAPUploadException(Exception):

    def __init__(self, response, message=None):

        # Try parsing out an error message.
        if message is None:
            try:
                message = response.text\
                    .split('<b>Message: </b>')[1]\
                    .split('</li>')[0].strip()

            except:
                message = "{} code returned".format(response.status_code)

        super(TAPUploadException, self).__init__(message)

        self.errors = response
        return None