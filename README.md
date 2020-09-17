## Deploy
```
gcloud auth login
gcloud config list
gcloud config set project [PROJECT_ID]
```

最初
```
gcloud functions deploy fm802-analysis --entry-point fm802_onair_info --runtime python37 --trigger-http --allow-unauthenticated --env-vars-file env.yaml
```

二回目以降
```
gcloud functions deploy fm802-analysis --trigger-http --env-vars-file env.yaml
```
