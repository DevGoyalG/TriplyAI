from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

# Test web search for travel-related information
# res=tavily_search("Best hotels in Delhi, India")
# print(res)

# Test flight search for a Japan trip originating from India
res = search_flights("Plan a 7 days Japan trip from India")
print(res)