from google.adk.tools import GoogleSearchTool

google_search = GoogleSearchTool()

def search_web(query):

    return google_search.run(query)