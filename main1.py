from ariadne.asgi import GraphQL
from flask_cors import CORS
from flask import Flask, request, jsonify
from ariadne import gql, QueryType, make_executable_schema, graphql_sync
import pickle
import preprocessed
# Define type definitions (schema) using SDL
type_defs = gql(
   """
   type Query {
       question(argument: String!,qts:String!): question}
   type question {
       score: String!
       response: String!
       question: String!
       }  
   """)
# Initialize query
query = QueryType()
# Define resolvers
@query.field("question")
def question(*_,argument,qts):
    reponse=preprocessed.preprocess(argument)
    question=preprocessed.preprocess(qts)
    print(question)
    feature=[[question,reponse]]
    print(feature)
    X_train_list = [str(item) for item in feature]
    fileAlgorithme = 'EntrainementSVM.sav'
    # ---Méthode de prédiction des données de test du Dataset ---
    algorithme = pickle.load(open(fileAlgorithme, 'rb'))
    print(algorithme.predict(X_train_list))

    return  { "score": algorithme.predict(X_train_list)[0], "response": argument, "question": qts}
# Create executable schema
schema = make_executable_schema(type_defs, query)

# Create ASGI application
app = GraphQL(schema)
# initialize flask app
app = Flask(__name__)
CORS(app, resources={r"/graphql": {"origins": "http://localhost:4200"}})


# Create a GraphQL endpoint for executing GraphQL queries
@app.route("/graphql", methods=["POST"])
def graphql_server():
   data = request.get_json()
   success, result = graphql_sync(schema, data, context_value={"request": request})
   print(request)
   status_code = 200 if success else 400
   return jsonify(result), status_code

# Run the app
if __name__ == "__main__":
   app.run(debug=True)