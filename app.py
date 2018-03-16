from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
import meetup.api

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = 'foobar'

toolbar = DebugToolbarExtension(app)


def get_names():
    client = meetup.api.Client("1ef7629661b777c76a4f136b7b1d1")

    rsvps = client.GetRsvps(event_id='235484841', urlname='_ChiPy_')
    member_id = ','.join([str(i['member']['member_id']) for i in rsvps.results])
    members = client.GetMembers(member_id=member_id)

    foo = {}
    for member in members.results:
        try:
            foo[member['name']] = member['photo']['thumb_link']
        except:
            pass # ignore those who do not have a complete profile
    return foo

# import pdb; pdb.set_trace()

member_rsvps = get_names()

@app.route('/rsvps')
def rsvps():
    return render_template('rsvps.html', rsvps=member_rsvps)


@app.route('/teams', methods=['GET', 'POST'])
def teams():
    results = request.form.to_dict()
    teams = [[]]
    current_team_index = 0
    for member in results:
        import pdb; pdb.set_trace()
        if len(teams[current_team_index]) == 4:
            current_team_index += 1
            teams.append([])
        teams[current_team_index].append(member)

    # import pdb; pdb.set_trace()
    return render_template(
        'teams.html',
        teams=teams,
        member_rsvps=member_rsvps
    )


if __name__ == '__main__':
    app.run(debug=True)
