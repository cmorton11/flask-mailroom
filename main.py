import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation 

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)
    

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.jinja2')

    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['name']).get()
            donation = Donation(value=int(request.form['value']), donor=donor)
            donation.save()

            return redirect(url_for('home'))
        except Donor.DoesNotExist:
            return render_template('create.jinja2', error="Donor not found.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
