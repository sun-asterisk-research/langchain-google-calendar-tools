# Langchain Google Calendar Tools

This repo walks through connecting to the Google Calendar API.

## Installation

```console
pip install langchain-google-calendar-tools
```

For local development:

```console
pip install -e .
```

## How to use

- Create a Google Cloud project and enable Google Calendar API.
- To get Oauth credentials for the Desktop app, please refer <https://developers.google.com/calendar/api/guides/overview> for detail.
- Download the credentials file to `./notebooks` and rename it to `credentials.json`. If you want to keep its original file name, please replace the value of `client_secrets_file` in [demo.ipynb](notebooks/demo.ipynb) with the valid path which points to the credentials file.
- Run this notebook to perform the listed functions

## Limitations

Due to the short development time, some of the following parts have not been completed and will be improved in the future:

- Timezone: Currently being fixed to Vietnam's timezone, it will be taken from the user's Calendar or the system in the future
- Update recurring events:  has not been implemented yet
- Functions related to inviting others and responding to invitations have not been implemented

## License

`langchain-google-calendar-tools` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
