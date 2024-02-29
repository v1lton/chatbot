import typesense

# Create a client to connect to the Typesense server
client = typesense.Client({
    'nodes': [{
        'host': 'yq1596od2mxi47vhp-1.a1.typesense.net',
        'port': '443',
        'protocol': 'https'
    }],
    'api_key': 'k26KOvUUNGPs2LbpWT1cu4sBpoQX7nct',
    'connection_timeout_seconds': 2
})

# Ask for the user to input a question
question = input("What do you want to know about? ")

# Search for the question in the collection
search_parameters = {
  'q'         : question,
  'query_by'  : 'question, answer'
}

# The name of the collection to search in
collection_name = 'questions'
response = client.collections[collection_name].documents.search(search_parameters)

# Print the answer for testing purposes
print("The answer is:")
print(response['hits'][0]['document']['answer'])