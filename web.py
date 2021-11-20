from flask import Flask, request, Response, redirect, url_for
import aurionAPI
from datetime import date, timedelta

app = Flask(__name__)




@app.route('/')
def landing_page():
    loginForm = f"""
    <h1>Entrez vos identifiants Aurion</h1>
    <h5> Cela créera un token pour utiliser l'API Aurion Mobile enac qui sera stocké localement sous forme de cookie, les login/mots de passe sont envoyés directement dans une requête et ne sont pas stockés par le site</h5>
    <form method='post' action = {url_for('fetch_store_token')}>
        <label>Username : </label>   
        <input type="text" placeholder="Enter Username" name="username" required>  
        <label>Password : </label>   
        <input type="password" placeholder="Enter Password" name="password" required>  
        <button type="submit">Login</button>   
    </form>
    """
    return loginForm

@app.route('/fetch_store_token', methods = ['POST'])
def fetch_store_token():

    if request.method == 'POST':
        login, pwd = request.form['username'], request.form['password']
        token = aurionAPI.get_token(login, pwd)
        return redirect(url_for('.display_link', token=token))
    else:
        return "erreur, requête non POST"

@app.route('/display_link')
def display_link():
    token = request.args['token']
    return f"""
    Lien pour télécharger l'ICS des ~30 prochains jours : \n
    {request.url_root[:-1]}{url_for('.get_month_planning')}?token={token}
    """

@app.route('/get_month_planning')
def get_month_planning():
    token = request.args.get('token')
    today = date.today().strftime("%Y-%m-%d")
    days30 = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
    json = aurionAPI.get_planning(token, today, days30)
    ics = aurionAPI.generate_ics(json)
    return Response(ics, mimetype='text/calendar', headers={'Content-Disposition': f'attachment; filename=planning_{today}_{days30}.ics'}, status=201)

if __name__ == '__main__':
    app.run()