from fluent import sender, event

from flask import Flask, render_template, url_for, request, jsonify
from stravalib import Client, unithelper

sender.setup('router', host='fluentd', port=24224)

app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS')

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/login')
def login():
    c = Client()
    url = c.authorization_url(client_id=app.config['STRAVA_CLIENT_ID'], redirect_uri=url_for(
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
        access_token = client.exchange_code_for_token(client_id=app.config['STRAVA_CLIENT_ID'],
                                                      client_secret=app.config['STRAVA_CLIENT_SECRET'],
                                                      code=code)
        strava_athlete = client.get_athlete()
        activities = client.get_activities(after="2021-01-01T00:00:00Z", limit=5)
        for activity in activities:
            event.Event('strava', {
                'athlete_id': strava_athlete.id,
                'athlete_name': strava_athlete.firstname + " " + strava_athlete.lastname,
                'activity_id': activity.id,
                'activity_name': activity.name,
                'type': activity.type,
                'distance_m': str(unithelper.meters(activity.distance)),
                'elevation_m': str(unithelper.meters(activity.total_elevation_gain)),
                'moving_time': str(activity.moving_time),
                'elapsed_time': str(activity.elapsed_time),
            })

        return render_template('login_results.html', athlete=strava_athlete, access_token=access_token)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
