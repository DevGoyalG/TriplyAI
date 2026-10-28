from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from backend import run_travel_agent

# Test web search for travel-related information
# res=tavily_search("Best hotels in Delhi, India")
# print(res)

# Test flight search for a Japan trip originating from India
# res = search_flights("Plan a 7 days Japan trip from India")
# print(res)

# Test Travel Agent to display the final travel planning response
user_input = input("Enter travel request: ")

response = run_travel_agent(
    user_input=user_input,
    thread_id="test_user"
)

print("\nFINAL RESPONSE:\n")
print(response["answer"])