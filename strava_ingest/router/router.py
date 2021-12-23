from fluent import sender, event
import os, base64
from flask import Flask, render_template, url_for, request, redirect
from stravalib import Client, client, unithelper
import dateutil.parser

sender.setup('router', host='fluentd-service', port=24224)

app = Flask(__name__)
strava_client_id = os.environ.get('STRAVA_CLIENT_ID')
strava_client_id = base64.b64decode(strava_client_id)

strava_client_secret = os.environ.get('STRAVA_CLIENT_SECRET')
strava_client_secret = base64.b64decode(strava_client_secret)

@app.route('/')
def hello():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    c = Client()
    url = c.authorization_url(client_id=strava_client_id, redirect_uri=url_for(
        '.logged_in', _external=True), approval_prompt='auto')
    return render_template('login.html', authorize_url=url)


@app.route('/strava-oauth')
def logged_in():
    """
    Method called by Strava (redirect) that includes parameters.
    - state
    - code
    - error
    """
    error = request.args.get('error')
    state = request.args.get('state')
    if error:
        return render_template('login_error.html', error=error)
    else:
        code = request.args.get('code')
        client = Client()
        access_token = client.exchange_code_for_token(client_id=strava_client_id,
                                                      client_secret=strava_client_secret,
                                                      code=code)
        strava_athlete = client.get_athlete()
        activities = client.get_activities(after="2021-01-01T00:00:00Z", limit=365)
        for activity in activities:
            print(activity.moving_time)
            event.Event('strava', {
                'athlete_id': strava_athlete.id,
                'athlete_name': strava_athlete.firstname + " " + strava_athlete.lastname,
                'activity_id': activity.id,
                'activity_name': activity.name,
                'time': str(dateutil.parser.parse(str(activity.start_date_local)).isoformat()) ,
                'type': activity.type,
                'distance_m': unithelper.meters(activity.distance).num,
                'elevation_m': unithelper.meters(activity.total_elevation_gain).num,
                'moving_time_s': activity.moving_time.seconds,
                'elapsed_time_s': activity.elapsed_time.seconds,
            })

        return render_template('login_results.html', athlete=strava_athlete, access_token=access_token)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
