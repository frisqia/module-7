from flask import request
from connectors.mysql_connector import connection
from models.review import Review
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from functools import wraps

from flask_login import login_user,logout_user, login_required, current_user

#chek connection
def get_test():
   return 'test'


#fetchiing data
def fetch_review():
    review_query = select(Review)
    Session = sessionmaker(connection)
    with Session() as s:
        result = s.execute(review_query)
        for row in result.scalars():
            print(f'ID: {row.id}, Description: {row.description} Email: {row.email}, Rate: {row.rating}' )
        return "fetch sucsess"
    
#search data

def search_review_data():
   Session= sessionmaker(connection)
   s= Session()
   try:
    review_query = select(Review)
    search_keyword = request.args.get('query')
    if search_keyword!= None:
       review_query = review_query.where(Review.rating.like(f"%{search_keyword}%"))
       
    reviews = s.execute(review_query)
    review=[]
    for row in reviews.scalars():
         review.append({
            'ID' : row.id,
            'Description' : row.description,
            'Email' : row.email,
            'Rate': row.rating
         })
         print(f'ID: {row.id}, Description: {row.description} Email: {row.email}, Rate: {row.rating}' )
    return{
       'review': review,
      #  'message': "Hello" + current_user.username
    }
   except Exception as c:
      print(c)
      return{'message':'unexpected error'}, 500
   #return {'message':'sucsess fetch review data'},200

#insert data
# @login_required
def review_insert():
   Session = sessionmaker(connection)
   s= Session()
   s.begin()
   try:
      NewReview = Review(
         description = request.form['description'],
         email = request.form['email'],
         rating = request.form['rating']
      )
      s.add(NewReview)
      s.commit()
      
   except Exception as c:
      s.rollback()
      return{'message': 'fail to insert data'},500

   return {'message':'success insert data'},200

#update review
# @login_required
def review_update(id):
   Session = sessionmaker(connection)
   s = Session()
   s.begin()
   try:
      review = s.query(Review).filter(Review.id == id).first()
      
      review.description = request.form['description']
      review.email = request.form['email']
      review.rating = request.form['rating']

      s.commit()
   except Exception as e:
      s.rollback()
      return{'message':'fail to update'},500

   return {'message':'success update review'},200

#delete data
# @login_required
def review_delete(id):
   Session = sessionmaker(connection)
   s = Session()
   s.begin()
   try:
      review = s.query(Review).filter(Review.id == id).first()
      s.delete(review)
      s.commit()
   except Exception as e:
      s.rollback()
      return{'message':'fail to delete'},500

   return {'message':'success delete'},200