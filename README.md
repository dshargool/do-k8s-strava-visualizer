# do-k8s-log-monitor



## Steps to setting up
1) Learn about the EFK (Elasticsearch Fluentd Kibana) stack and the components it comprises of.
	- Elasticsearch powers the search engine so we can find what we're looking for in our data
	- Logstash is a data processing pipeline that transforms our logs into searchable data
	- Kibana is the webserver that let's us see our beautiful data.
2) Decide what data we want to ingest.
  - It's not logs but it'd be useful to log my physical activities and see their stats on a webpage.
  - We can just have a python script run to ingest the data from Strava's API (I guess) and ingress into Fluentd
3) Build our log capturing code
  - [x] Strava Authentication on a Flask WebApp
  - [x] Log all of our authenticated users data to fluentd
  - [x] Set up docker container to host Flask app that will process our data (should we have a worker that does this instead?)
4) Deploy the stack locally
  - [x] Use docker to deploy small scale locally so we understand the information flow
    - [x] ElasticSearch (Issue with not enough memory on computer so it just errors out with Error 137)
    - [x] Fluentd
    - [x] Kibana
4) Deploy to DigitalOcean!
  - [ ] Set up our webpage pods that allow users to interact
  - [ ] Set up fluentd to capture the logs from our webpage pods
    - What services do we need in kubernetes to allow chatter?
  - [ ] Set up Elasticsearch so there's somewhere for the data to go
  - [ ] Set up Kibana so we can see the data
5) Success!

## Resources
- https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes
- https://smirnov-am.github.io/running-flask-in-production-with-docker/
