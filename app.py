from flask import Flask, jsonify
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)
@app.route("/")

def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api.v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end<br/>"
    )
@app.route ("/api/v1.0/precipitation")
def precipitation():
	session = Session(engine)
	
	results= session.query(Measurement.date, Measurement.prcp).all()
	
	session.close()
	
	prcp_dict = dict(results)
	
	return jsonify(prcp_dict)
	
@app.route ("/api/v1.0/stations")
def stations():
	session = Session(engine)
	
	results = session.query(Station.station).all()
	results_list= list(np.ravel(results))
	
	session.close()
	
	return jsonify(results_list)
	

@app.route ("/api/v1.0/tobs")
def temp():
	session= Session(engine)
	
	max_date=session.query(func.max(Measurement.date)).all()[0][0]
	year=int(max_date[0:4])
	month=int(max_date[5:7])
	day=int(max_date[8:])
	last_date=dt.date(year, month, day)
	year_ago= last_date - dt.timedelta(days=365)
	results=session.query(Measurement.tobs).filter(Measurement.date >= year_ago).all()
	
	session.close()
	return jsonify(results)


@app.route ("/api/v1.0/start")
def tempstart():
	session= Session(engine)
	
	start_date= session.query(func.min(Measurement.date)).all()[0][0]
	sel= [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
	temp_lstuple = session.query(*sel).filter(Measurement.date >= start_date).all()
	
	session.close()
	
	temp_pram_list= list(np.ravel(temp_lstuple))
	
	temp_list=[]
	for temp in temp_lstuple:
		temp_dict = {}
		temp_dict["Min temp after Start Date 2010-01-01"]=temp_pram_list[0]
		temp_dict["Avg temp after Start Date 2010-01-01"]=temp_pram_list[1]
		temp_dict["Max temp after Start Date 2010-01-01"]=temp_pram_list[2]
		temp_list.append(temp_dict)
		
	return jsonify(temp_list)

	
@app.route ("/api/v1.0/startend")
def tempstartend():

	session= Session(engine)
	start_date= session.query(func.min(Measurement.date)).all()[0][0]
	date_format= dt.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:]))
	end_date= date_format + dt.timedelta(weeks = 60)
	sel= [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
	temp_lstuple = session.query(*sel).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
	
	session.close()
	
	temp_pram1_list= list(np.ravel(temp_lstuple))
	
	temp_list=[]
	for temp in temp_lstuple:
		temp_dict = {}
		temp_dict["Min temp between 2010-01-01 and 2011-02-25"]=temp_pram1_list[0]
		temp_dict["Avg temp between 2010-01-01 and 2011-02-25"]=temp_pram1_list[1]
		temp_dict["Max temp between 2010-01-01 and 2011-02-25"]=temp_pram1_list[2]
		temp_list.append(temp_dict)
		
	return jsonify(temp_list)
	

if __name__ == '__main__':
    app.run(debug=True)