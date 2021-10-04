# Tellor Dispute Discord Alert Bot
Simple bot for scraping etherscan for new and tallied disputes.

## Running

The simplest way to get up and running would be with docker-compose

You will first need to copy the .env-sample to .env, and add your own etherscan api key + Discord webhook url.

Once you've set your .env run
```
docker-compose --file docker-compose.yaml up
```

For running without docker, you'll need to setup Postgres yourself.