# Langchain Google Calendar Tools

## Installation

```console
pip install langchain-google-calendar-tools
```

For local development:

```console
pip install -e .
```

## How to use

- Create Google Cloud project and enable Google Calendar API.
- Get Oauth credentials for Desktop app, please refer <https://developers.google.com/calendar/api/guides/overview> for detail.
- Download credentials file to ./notebooks and rename to `credentials.json`. If you want to keep its original file name, please replace the value of `client_secrets_file` in  [demo.ipynb](notebooks/demo.ipynb) with valid path which point to credentials file.
- Run this notebook to perform the listed functions

## Limitations

Due to the short development time, some of the following parts have not been completed and will be improved in the future:

- Timezone: Currently being fixed to Vietnam's timezone, in the future it will be taken from the user's Calendar or from the system
- Update recurring events: currently there are no event updates available
- Functions related to inviting others and responding to invitations have not been implemented

## License

`langchain-google-calendar-tools` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
